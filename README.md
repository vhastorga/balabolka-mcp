# Balcon MCP Server 🎙️

Servidor MCP (Model Context Protocol) que expone herramientas de **Text-to-Speech (TTS)** para agentes de IA, utilizando la interfaz de línea de comandos de **Balabolka (`balcon`)** junto con **FFmpeg** para la síntesis de voz y concatenación de audio.

> ⚠️ **Plataforma nativa:** Balcon utiliza la API de voz nativa de Microsoft (SAPI). **Windows es su entorno nativo y recomendado.** En Linux y macOS puede ejecutarse mediante **Wine**, aunque con limitaciones en las voces disponibles de fábrica.

---

## 📑 Tabla de Contenidos

1. [Características](#-características)
2. [Requisitos](#-requisitos)
3. [Instalación de Dependencias](#-instalación-de-dependencias)
   - [Windows (Recomendado)](#-windows-nativo-y-recomendado)
   - [Linux](#-linux)
   - [macOS](#-macos)
4. [Configuración del Cliente MCP](#-configuración-del-cliente-mcp)
5. [Requisitos de Python](#-requisitos-de-python)
6. [Herramientas Disponibles](#-herramientas-disponibles)
7. [Ejemplos de Uso](#-ejemplos-de-uso)
8. [Solución de Problemas](#-solución-de-problemas)

---

## ✨ Características

| Herramienta | Descripción |
|-------------|-------------|
| `list_voices` | Lista todas las voces SAPI instaladas en el sistema. |
| `list_audio_devices` | Lista los dispositivos de salida de audio disponibles. |
| `text_to_speech` | Convierte texto directo a un archivo WAV con una voz específica. |
| `text_file_to_speech` | Convierte un archivo de texto (`*.txt`) a audio WAV. |
| `multi_voice_speech` | Genera audio combinando múltiples segmentos narrados por distintas voces usando FFmpeg. |

---

## 📋 Requisitos

- **Sistema Operativo:** Windows 10/11 (nativo). Linux/macOS vía Wine.
- **Binarios en el `PATH`:**
  - `balcon` — CLI de Balabolka ([Descargar](http://www.cross-plus-a.com/balcon.zip))
  - `ffmpeg` — Para concatenación de audio multi-voz ([Descargar](https://www.gyan.dev/ffmpeg/builds/))
- **Python:** 3.10 o superior.
- **Paquete Python:** `mcp`

---

## 🛠️ Instalación de Dependencias

### 🪟 Windows (Nativo y Recomendado)

#### 1. Instalar FFmpeg

Via gestor de paquetes (recomendado):

```powershell
# Usando winget (incluido en Windows 10/11)
winget install ffmpeg

# O usando Scoop
scoop install ffmpeg
```

> Si prefieres instalación manual: descarga el ZIP desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extráelo y añade la subcarpeta `bin` a las **Variables de entorno del sistema** → `Path`.

#### 2. Instalar Balcon (CLI)

Balcon no requiere instalador formal. Solo descarga y añade al `PATH`:

1. Descarga `balcon.zip` desde [cross-plus-a.com](http://www.cross-plus-a.com/balcon.zip).
2. Extrae su contenido en una ruta permanente, por ejemplo: `C:\balcon\`.
3. Añade esa carpeta al `PATH` del sistema:
   - Presiona la tecla Windows, escribe *"Editar las variables de entorno del sistema"* y ábrelo.
   - Haz clic en **Variables de entorno**.
   - En *Variables del sistema*, busca **Path** y dale a **Editar**.
   - Haz clic en **Nuevo** y pega la ruta: `C:\balcon`
   - Acepta y cierra todas las ventanas.

#### 3. Verificar Instalación

Abre una **nueva** terminal (para refrescar el `PATH`) y ejecuta:

```bash
ffmpeg -version
balcon -l
```

El comando `balcon -l` debe mostrar el listado de voces SAPI instaladas.

---

### 🐧 Linux

#### 1. Instalar FFmpeg y Wine

```bash
sudo apt update
sudo apt install ffmpeg wine unzip
```

#### 2. Instalar Balcon

```bash
# Descargar y extraer
wget http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Crear alias (si usas Bash; cambia a ~/.zshrc si usas Zsh)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.bashrc
source ~/.bashrc
```

#### 3. Verificar Instalación

```bash
ffmpeg -version
balcon -l
```

> **Nota para Linux:** Por defecto, al usar Wine, Balcon solo detectará las voces compatibles con SAPI que instales explícitamente dentro del entorno de tu prefijo de Wine (`~/.wine`).

---

### 🍏 macOS

#### 1. Instalar FFmpeg y Wine

Requiere [Homebrew](https://brew.sh/):

```bash
# Instalar FFmpeg nativo
brew install ffmpeg

# Instalar Wine (necesario para emular el ejecutable de Balcon)
brew install --cask wine-stable
```

#### 2. Instalar Balcon

```bash
# Descargar y extraer
curl -O http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Crear alias (macOS usa Zsh por defecto en versiones modernas)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.zshrc
source ~/.zshrc
```

#### 3. Verificar Instalación

```bash
ffmpeg -version
balcon -l
```

> **Nota para macOS:** Balcon no tendrá acceso a las voces nativas de Apple (Siri, etc.). Solo podrá usar voces emuladas de Windows que instales dentro del entorno de Wine.

---

## ⚙️ Configuración del Cliente MCP

Una vez instaladas las dependencias, conecta el servidor TTS a tu cliente MCP añadiendo la siguiente configuración a tu archivo de ajustes (generalmente `mcp_config.json` o similar):

```json
{
  "mcpServers": {
    "balcon-tts": {
      "command": "python",
      "args": [
        "C:/Users/<TU_USUARIO>/Downloads/balabolka-mcp/balcon_mcp_server.py"
      ]
    }
  }
}
```

> ⚠️ **Importante:**
> - Reemplaza `<TU_USUARIO>` con tu nombre de usuario real del sistema.
> - Ajusta la ruta al archivo `balcon_mcp_server.py` según donde lo hayas ubicado.
> - En los argumentos usa barras normales (`/`) o dobles barras invertidas (`\\`) para evitar problemas de escape en JSON.

---

## 🐍 Requisitos de Python

1. **Verificar Python instalado:**

   ```bash
   python --version
   ```

2. **Instalar el paquete MCP:**

   ```bash
   pip install mcp
   ```

---

## 🔧 Herramientas Disponibles

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `text` | `string` | Texto a sintetizar. |
| `output_file` | `string` | Ruta completa del archivo WAV de salida. |
| `voice` | `string` (opcional) | Nombre exacto de la voz SAPI. Usa `list_voices` para ver opciones. |
| `rate` | `int` (opcional) | Velocidad: `-10` (lento) … `0` (normal) … `10` (rápido). |
| `pitch` | `int` (opcional) | Tono: `-10` (grave) … `0` (normal) … `10` (agudo). |
| `volume` | `int` (opcional) | Volumen: `0` (silencio) … `100` (máximo). |
| `freq_khz` | `int` (opcional) | Frecuencia de muestreo en kHz (`8`–`48`, default `22`). |
| `bit_depth` | `int` (opcional) | Profundidad de bits (`8` o `16`, default `16`). |
| `channels` | `int` (opcional) | Canales (`1`=mono, `2`=estéreo, default `1`). |

---

## 💡 Ejemplos de Uso

### Generar audio simple

```json
{
  "text": "Hola, este es un mensaje de prueba.",
  "output_file": "C:/Users/TU_USUARIO/Desktop/saludo.wav",
  "voice": "Microsoft Helena Desktop",
  "rate": 1,
  "volume": 90
}
```

### Generar audio multi-voz

```json
{
  "segments": "[\n  {\"text\": \"Bienvenidos al tutorial.\", \"voice\": \"Microsoft Sabina Desktop\"},\n  {\"text\": \"Hoy aprenderemos sobre MCP.\", \"voice\": \"Microsoft Helena Desktop\", \"rate\": 1, \"pause_before_ms\": 500}\n]",
  "output_file": "C:/Users/TU_USUARIO/Desktop/tutorial.wav",
  "default_freq_khz": 22,
  "default_bit_depth": 16,
  "default_channels": 1
}
```

---

## 🩺 Solución de Problemas

| Síntoma | Posible Causa | Solución |
|---------|---------------|----------|
| `balcon no se reconoce como comando` | No está en el `PATH` | Añade la carpeta de `balcon.exe` al `Path` del sistema y reinicia la terminal. |
| `ffmpeg falló al concatenar` | Versión incompatible o no instalado | Verifica `ffmpeg -version`. Reinstala si es necesario. |
| `No se encontraron voces` | Sin voces SAPI instaladas | En Windows, instala paquetes de idioma con voz desde Configuración → Hora e idioma. |
| `balcon falló (código X)` | Texto con caracteres especiales no escapados | Asegúrate de que el texto no contenga comillas sin escapar dentro del JSON. |

---

*README disponible también en [inglés](./README_en.md).*
