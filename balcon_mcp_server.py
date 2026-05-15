#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         BALCON MCP SERVER  –  Text-to-Speech para Agentes   ║
║  Usa Balabolka CLI (balcon) + ffmpeg para audio multi-voz   ║
╚══════════════════════════════════════════════════════════════╝

Herramientas expuestas:
  • list_voices          → lista voces SAPI instaladas
  • list_audio_devices   → lista dispositivos de audio
  • text_to_speech       → texto → WAV con una voz
  • text_file_to_speech  → archivo de texto → WAV con una voz
  • multi_voice_speech   → script multi-voz → WAV combinado (ffmpeg)

Requiere:
  - balcon  en el PATH  (Balabolka CLI)
  - ffmpeg  en el PATH  (solo para multi_voice_speech)
  - Python 3.10+
  - pip install mcp
"""

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────
# Inicialización del servidor MCP
# ─────────────────────────────────────────────
app = FastMCP(
    "balcon-tts",
    instructions=(
        "Text-to-Speech usando Balabolka (balcon) CLI. "
        "Genera audio WAV con una o múltiples voces SAPI combinadas."
    ),
)

# Directorio temporal para archivos intermedios
TEMP_BASE = Path(tempfile.gettempdir()) / "balcon_mcp"
TEMP_BASE.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Utilidades internas
# ─────────────────────────────────────────────

def _run(cmd: list[str], timeout: int = 120) -> tuple[int, str, str]:
    """Ejecuta un comando y devuelve (código, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout después de {timeout}s ejecutando: {' '.join(cmd)}"
    except FileNotFoundError as exc:
        return -1, "", f"Ejecutable no encontrado: {exc}"


def _unique_dir() -> Path:
    """Crea y devuelve un directorio temporal único para la sesión."""
    d = TEMP_BASE / f"session_{os.getpid()}_{int(time.monotonic() * 1000)}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _build_balcon_cmd(
    output_wav: str,
    text: Optional[str] = None,
    input_file: Optional[str] = None,
    voice: Optional[str] = None,
    rate: int = 0,
    pitch: int = 0,
    volume: int = 100,
    pause_sentences_ms: int = 0,
    pause_paragraphs_ms: int = 0,
    silence_begin_ms: int = 0,
    silence_end_ms: int = 0,
    freq_khz: int = 22,
    bit_depth: int = 16,
    channels: int = 1,
    encoding: str = "utf8",
) -> list[str]:
    """Construye el array de argumentos para balcon."""
    cmd = ["balcon"]

    # Fuente de texto
    if text is not None:
        cmd += ["-t", text]
    elif input_file is not None:
        cmd += ["-f", input_file, "-enc", encoding]
    else:
        raise ValueError("Debe indicarse 'text' o 'input_file'")

    # Salida
    cmd += ["-w", output_wav]

    # Voz
    if voice:
        cmd += ["-n", voice]

    # Parámetros de síntesis
    cmd += ["-s", str(max(-10, min(10, rate)))]
    cmd += ["-p", str(max(-10, min(10, pitch)))]
    cmd += ["-v", str(max(0, min(100, volume)))]

    # Formato de audio
    cmd += ["-fr", str(max(8, min(48, freq_khz)))]
    cmd += ["-bt", str(bit_depth if bit_depth in (8, 16) else 16)]
    cmd += ["-ch", str(channels if channels in (1, 2) else 1)]

    # Silencios y pausas
    if pause_sentences_ms > 0:
        cmd += ["-e", str(pause_sentences_ms)]
    if pause_paragraphs_ms > 0:
        cmd += ["-a", str(pause_paragraphs_ms)]
    if silence_begin_ms > 0:
        cmd += ["-sb", str(silence_begin_ms)]
    if silence_end_ms > 0:
        cmd += ["-se", str(silence_end_ms)]

    return cmd


def _file_info(path: str) -> str:
    """Devuelve tamaño legible del archivo."""
    try:
        size = Path(path).stat().st_size
        if size > 1_048_576:
            return f"{size / 1_048_576:.1f} MB"
        if size > 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size} bytes"
    except Exception:
        return "tamaño desconocido"


# ══════════════════════════════════════════════════════════════
# HERRAMIENTAS MCP
# ══════════════════════════════════════════════════════════════

@app.tool()
def list_voices() -> str:
    """
    Lista todas las voces SAPI instaladas en el sistema.

    Returns:
        Texto con el listado de voces disponibles para usar en los demás tools.
    """
    code, stdout, stderr = _run(["balcon", "-l"])
    if code != 0:
        return f"❌ Error al listar voces: {stderr}"
    return stdout or "⚠️ No se encontraron voces instaladas."


@app.tool()
def list_audio_devices() -> str:
    """
    Lista los dispositivos de salida de audio disponibles en el sistema.

    Returns:
        Texto con dispositivos indexados, usables con el parámetro -b de balcon.
    """
    code, stdout, stderr = _run(["balcon", "-g"])
    if code != 0:
        return f"❌ Error al listar dispositivos: {stderr}"
    return stdout or "⚠️ No se encontraron dispositivos de audio."


@app.tool()
def text_to_speech(
    text: str,
    output_file: str,
    voice: Optional[str] = None,
    rate: int = 0,
    pitch: int = 0,
    volume: int = 100,
    pause_sentences_ms: int = 0,
    pause_paragraphs_ms: int = 0,
    silence_begin_ms: int = 0,
    silence_end_ms: int = 0,
    freq_khz: int = 22,
    bit_depth: int = 16,
    channels: int = 1,
) -> str:
    """
    Convierte texto a voz y guarda el resultado como archivo WAV.

    Args:
        text:               Texto a sintetizar.
        output_file:        Ruta completa del archivo WAV de salida.
        voice:              Nombre de la voz SAPI (usar list_voices para ver opciones).
                            Si se omite, usa la voz predeterminada del sistema.
        rate:               Velocidad de habla  (-10 = lento … 0 = normal … 10 = rápido).
        pitch:              Tono de voz         (-10 = grave … 0 = normal … 10 = agudo).
        volume:             Volumen             (0 = silencio … 100 = máximo).
        pause_sentences_ms: Pausa entre oraciones en milisegundos.
        pause_paragraphs_ms:Pausa entre párrafos en milisegundos.
        silence_begin_ms:   Silencio al inicio del audio en milisegundos.
        silence_end_ms:     Silencio al final del audio en milisegundos.
        freq_khz:           Frecuencia de muestreo en kHz (8–48, default 22).
        bit_depth:          Profundidad de bits (8 o 16, default 16).
        channels:           Modo de canal (1=mono, 2=estéreo, default 1).

    Returns:
        Mensaje de éxito con la ruta y tamaño del archivo, o descripción del error.
    """
    # Asegurar que el directorio de salida exista
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    cmd = _build_balcon_cmd(
        output_wav=output_file,
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
        pause_sentences_ms=pause_sentences_ms,
        pause_paragraphs_ms=pause_paragraphs_ms,
        silence_begin_ms=silence_begin_ms,
        silence_end_ms=silence_end_ms,
        freq_khz=freq_khz,
        bit_depth=bit_depth,
        channels=channels,
    )

    code, stdout, stderr = _run(cmd)

    if code != 0:
        return f"❌ balcon falló (código {code}): {stderr}"

    if not Path(output_file).exists():
        return f"❌ balcon terminó sin error pero no creó el archivo. stderr: {stderr}"

    return (
        f"✅ Audio generado correctamente.\n"
        f"   Archivo : {output_file}\n"
        f"   Tamaño  : {_file_info(output_file)}\n"
        f"   Voz     : {voice or '(predeterminada)'}\n"
        f"   Rate/Pitch/Vol: {rate} / {pitch} / {volume}"
    )


@app.tool()
def text_file_to_speech(
    input_file: str,
    output_file: str,
    voice: Optional[str] = None,
    rate: int = 0,
    pitch: int = 0,
    volume: int = 100,
    encoding: str = "utf8",
    pause_sentences_ms: int = 0,
    pause_paragraphs_ms: int = 0,
    freq_khz: int = 22,
    bit_depth: int = 16,
    channels: int = 1,
) -> str:
    """
    Convierte un archivo de texto a voz y guarda el resultado como WAV.

    Args:
        input_file:         Ruta al archivo de texto de entrada.
        output_file:        Ruta completa del archivo WAV de salida.
        voice:              Nombre de la voz SAPI (usar list_voices para ver opciones).
        rate:               Velocidad de habla (-10 a 10).
        pitch:              Tono de voz (-10 a 10).
        volume:             Volumen (0 a 100).
        encoding:           Codificación del archivo de texto: ansi | utf8 | unicode.
        pause_sentences_ms: Pausa entre oraciones en milisegundos.
        pause_paragraphs_ms:Pausa entre párrafos en milisegundos.
        freq_khz:           Frecuencia de muestreo en kHz (8–48).
        bit_depth:          Profundidad de bits (8 o 16).
        channels:           Modo de canal (1=mono, 2=estéreo).

    Returns:
        Mensaje de éxito o descripción del error.
    """
    if not Path(input_file).exists():
        return f"❌ Archivo de entrada no encontrado: '{input_file}'"

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    cmd = _build_balcon_cmd(
        output_wav=output_file,
        input_file=input_file,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
        pause_sentences_ms=pause_sentences_ms,
        pause_paragraphs_ms=pause_paragraphs_ms,
        freq_khz=freq_khz,
        bit_depth=bit_depth,
        channels=channels,
        encoding=encoding,
    )

    code, stdout, stderr = _run(cmd)

    if code != 0:
        return f"❌ balcon falló (código {code}): {stderr}"

    if not Path(output_file).exists():
        return f"❌ balcon terminó sin crear el archivo. stderr: {stderr}"

    return (
        f"✅ Audio generado correctamente.\n"
        f"   Entrada : {input_file}\n"
        f"   Salida  : {output_file}\n"
        f"   Tamaño  : {_file_info(output_file)}\n"
        f"   Voz     : {voice or '(predeterminada)'}"
    )


@app.tool()
def multi_voice_speech(
    segments: str,
    output_file: str,
    default_freq_khz: int = 22,
    default_bit_depth: int = 16,
    default_channels: int = 1,
) -> str:
    """
    Crea un audio multi-voz combinando segmentos de texto narrados por diferentes voces.
    Cada segmento se sintetiza individualmente con balcon y luego se concatenan con ffmpeg.

    Args:
        segments:
            JSON con lista de segmentos. Cada segmento acepta:
              - text              (str,  requerido) : Texto a narrar.
              - voice             (str,  opcional)  : Nombre de voz SAPI.
              - rate              (int,  opcional)  : Velocidad -10 a 10  (default 0).
              - pitch             (int,  opcional)  : Tono -10 a 10       (default 0).
              - volume            (int,  opcional)  : Volumen 0 a 100     (default 100).
              - pause_before_ms   (int,  opcional)  : Silencio previo en ms.
              - pause_after_ms    (int,  opcional)  : Silencio posterior en ms.
              - pause_sentences_ms(int,  opcional)  : Pausa entre oraciones en ms.
              - freq_khz          (int,  opcional)  : Frecuencia de muestreo en kHz.
              - bit_depth         (int,  opcional)  : Profundidad de bits (8/16).
              - channels          (int,  opcional)  : Canales (1/2).

            Ejemplo mínimo:
              [
                {"text": "Bienvenidos al programa.", "voice": "Microsoft Sabina Desktop"},
                {"text": "Hoy hablaremos sobre IA.", "voice": "Microsoft Helena Desktop",
                 "rate": 1, "pause_before_ms": 500}
              ]

        output_file:        Ruta completa del archivo WAV final combinado.
        default_freq_khz:   Frecuencia de muestreo por defecto para todos los segmentos.
        default_bit_depth:  Profundidad de bits por defecto.
        default_channels:   Canales por defecto (1=mono, 2=estéreo).

    Returns:
        Resumen del proceso: segmentos OK/fallidos, ruta y tamaño del archivo final.
    """
    # ── 1. Parsear JSON de segmentos ──────────────────────────
    try:
        segment_list: list[dict] = json.loads(segments)
    except json.JSONDecodeError as exc:
        return f"❌ JSON inválido en 'segments': {exc}"

    if not isinstance(segment_list, list) or len(segment_list) == 0:
        return "❌ 'segments' debe ser una lista JSON no vacía."

    # ── 2. Directorio temporal de sesión ──────────────────────
    session_dir = _unique_dir()
    segment_files: list[str] = []
    warnings: list[str] = []

    try:
        # ── 3. Generar cada segmento con balcon ───────────────
        for idx, seg in enumerate(segment_list, start=1):
            text = str(seg.get("text", "")).strip()
            if not text:
                warnings.append(f"Segmento {idx}: texto vacío → omitido.")
                continue

            voice            = seg.get("voice")
            rate             = int(seg.get("rate", 0))
            pitch            = int(seg.get("pitch", 0))
            volume           = int(seg.get("volume", 100))
            pause_before     = int(seg.get("pause_before_ms", 0))
            pause_after      = int(seg.get("pause_after_ms", 0))
            pause_sent       = int(seg.get("pause_sentences_ms", 0))
            freq             = int(seg.get("freq_khz", default_freq_khz))
            depth            = int(seg.get("bit_depth", default_bit_depth))
            ch               = int(seg.get("channels", default_channels))

            seg_wav = str(session_dir / f"seg_{idx:04d}.wav")

            cmd = _build_balcon_cmd(
                output_wav=seg_wav,
                text=text,
                voice=voice,
                rate=rate,
                pitch=pitch,
                volume=volume,
                pause_sentences_ms=pause_sent,
                silence_begin_ms=pause_before,
                silence_end_ms=pause_after,
                freq_khz=freq,
                bit_depth=depth,
                channels=ch,
            )

            code, _, stderr = _run(cmd, timeout=180)

            if code != 0 or not Path(seg_wav).exists():
                warnings.append(
                    f"Segmento {idx} (voz={voice or 'default'}): "
                    f"balcon falló → {stderr or 'sin salida'} → omitido."
                )
                continue

            segment_files.append(seg_wav)

        # ── 4. Validar que haya al menos un segmento OK ───────
        if not segment_files:
            detail = "\n  ".join(warnings)
            return f"❌ Ningún segmento se generó exitosamente.\nDetalles:\n  {detail}"

        # ── 5a. Si hay un solo segmento, simplemente copiarlo ─
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        if len(segment_files) == 1:
            shutil.copy2(segment_files[0], output_file)
            result_msg = (
                f"✅ Audio generado (segmento único).\n"
                f"   Archivo : {output_file}\n"
                f"   Tamaño  : {_file_info(output_file)}"
            )

        else:
            # ── 5b. Concatenar con ffmpeg ─────────────────────
            concat_txt = session_dir / "concat.txt"
            with open(concat_txt, "w", encoding="utf-8") as fh:
                for sf in segment_files:
                    # ffmpeg necesita barras normales
                    safe = sf.replace("\\", "/")
                    fh.write(f"file '{safe}'\n")

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_txt),
                "-c", "copy",
                output_file,
            ]

            code, _, stderr = _run(ffmpeg_cmd, timeout=300)

            if code != 0:
                return (
                    f"❌ ffmpeg falló al concatenar (código {code}): {stderr}\n"
                    f"   Segmentos individuales en: {session_dir}\n"
                    f"   (directorio NO limpiado para diagnóstico)"
                )

            if not Path(output_file).exists():
                return f"❌ ffmpeg terminó sin crear '{output_file}'. stderr: {stderr}"

            result_msg = (
                f"✅ Audio multi-voz generado correctamente.\n"
                f"   Archivo         : {output_file}\n"
                f"   Tamaño          : {_file_info(output_file)}\n"
                f"   Segmentos usados: {len(segment_files)} / {len(segment_list)}"
            )

        # ── 6. Adjuntar advertencias si las hubo ─────────────
        if warnings:
            result_msg += "\n⚠️  Advertencias:\n" + "".join(
                f"   • {w}\n" for w in warnings
            )

        return result_msg

    finally:
        # Limpieza: solo si ffmpeg tuvo éxito (no limpiamos en error de ffmpeg)
        if Path(output_file).exists():
            shutil.rmtree(session_dir, ignore_errors=True)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run()