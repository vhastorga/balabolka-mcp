## ⚙️ Configuración del Cliente MCP

Para conectar el servidor TTS de Balcon a tu cliente MCP, deberás añadir la siguiente configuración al archivo de ajustes de tu cliente (generalmente `mcp_config.json` o similar).

A continuación tienes un ejemplo de configuración. **Recuerda reemplazar `<YOUR_USER>`** con tu nombre de usuario real del sistema y ajustar la ruta hacia donde se encuentre el archivo `balcon_mcp_server.py`.

```json
{
  "mcpServers": {
    "balcon-tts": {
      "command": "python",
      "args": [
        "C:/Users/<TU_USARIO>/.gemini/antigravity/balcon_mcp_server.py"
      ]
    }
  }
}
```

# 🛠️ Guía de Instalación: Dependencias para Balcon MCP

Para que **Balcon MCP** funcione correctamente, tu sistema necesita dos dependencias clave:

1. **FFmpeg**: Para el procesamiento, conversión y manejo del audio.
2. **Balcon**: La interfaz de línea de comandos (CLI) de Balabolka, encargada de la síntesis de voz (Text-to-Speech).

> ⚠️ **Aviso de compatibilidad:** Balcon utiliza la API de voz nativa de Microsoft (SAPI), por lo que **su entorno nativo y recomendado es Windows**. En Linux y macOS no está disponible de forma nativa, pero es posible ejecutarlo mediante **Wine**, aunque con limitaciones en las voces disponibles de fábrica.

A continuación tienes las instrucciones de instalación para cada sistema operativo.

---

## 🪟 Windows (Nativo y Recomendado)

### 1. Instalar FFmpeg

La forma más rápida es a través del gestor de paquetes nativo de Windows. Abre **PowerShell** (recomendado como administrador) y ejecuta:

```powershell
# Usando Winget (Viene por defecto en Windows 10 y 11)
winget install ffmpeg

# O usando Scoop (si lo prefieres):
scoop install ffmpeg
```

*(Si prefieres hacerlo manualmente: descárgalo en [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extrae el ZIP y añade la ruta de la subcarpeta `bin` al `PATH` de Windows).*

### 2. Instalar Balcon (CLI)

Balcon no requiere instalación formal, simplemente se descarga el ejecutable y se añade a las variables de entorno.

1. Descarga el archivo `.zip` oficial desde [Cross+A (balcon.zip)](http://www.cross-plus-a.com/balcon.zip).
2. Extrae su contenido en una ruta permanente, por ejemplo: `C:\balcon\`
3. Añade esa carpeta al **PATH** de tu sistema:
   - Presiona la tecla Windows, escribe *"Editar las variables de entorno del sistema"* y abre esa opción.
   - Haz clic en el botón **Variables de entorno**.
   - En *Variables del sistema*, busca la variable llamada **Path** y dale a **Editar**.
   - Haz clic en **Nuevo** y pega la ruta: `C:\balcon`
   - Acepta y cierra todas las ventanas.

### 3. Verificar instalación

Abre una **nueva** terminal y comprueba que ambos comandos responden:

```bash
ffmpeg -version
balcon -l
```

*(El comando `balcon -l` listará todas las voces SAPI que tengas instaladas en tu Windows).*

---

## 🐧 Linux

### 1. Instalar FFmpeg y Wine

Dado que Balcon es un ejecutable `.exe` de Windows, instalaremos **Wine** para poder correrlo, junto con la dependencia de FFmpeg. En distros basadas en Debian/Ubuntu (como Ubuntu, Mint, Pop!_OS), abre tu terminal y ejecuta:

```bash
sudo apt update
sudo apt install ffmpeg wine unzip
```

### 2. Instalar Balcon

Descargaremos el ejecutable, lo guardaremos en un directorio oculto en tu carpeta de usuario y crearemos un *alias* para que funcione como un comando nativo.

```bash
# Descargar y extraer
wget http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Crear el alias (Asumiendo que usas Bash. Si usas Zsh, cambia .bashrc por .zshrc)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.bashrc
source ~/.bashrc
```

### 3. Verificar instalación

```bash
ffmpeg -version
balcon -l
```

> **Nota para Linux:** Por defecto, al usar Wine, Balcon solo detectará las voces compatibles con SAPI que instales explícitamente dentro del entorno virtual de tu prefijo de Wine (`~/.wine`).

---

## 🍏 macOS

### 1. Instalar FFmpeg y Wine

En macOS utilizaremos el gestor de paquetes [Homebrew](https://brew.sh/). Si no lo tienes, instálalo primero. Luego ejecuta en tu terminal:

```bash
# Instalar FFmpeg nativo
brew install ffmpeg

# Instalar Wine (necesario para emular el .exe de Balcon)
brew install --cask wine-stable
```

### 2. Instalar Balcon

Al igual que en Linux, lo descargaremos y configuraremos un *alias* global:

```bash
# Descargar y extraer
curl -O http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Crear el alias (macOS usa Zsh por defecto en las versiones modernas)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.zshrc
source ~/.zshrc
```

### 3. Verificar instalación

```bash
ffmpeg -version
balcon -l
```

> **Nota para Mac:** Balcon no tendrá acceso a las voces nativas de Apple (Siri, etc.). El motor leerá únicamente las voces emuladas de Windows que logres instalar en el entorno de Wine.



## 🐍 Checklist Final: Requisitos de Python

Dado que este servidor MCP está escrito en Python, asegúrate de cumplir con lo siguiente antes de intentar ejecutarlo:

2. **Python Instalado y en el PATH**: Comprueba que tienes Python instalado en tu sistema y agregado a las variables de entorno (`PATH`). Puedes verificarlo abriendo una terminal y ejecutando.
   
   ```bash
         python --version
   ```

3. **Instalar el paquete MCP**: El servidor necesita la librería oficial de MCP de Python para poder comunicarse. Instálala usando pip con el siguiente comando:
   
   ```bash
   pip install mcp
   ```


