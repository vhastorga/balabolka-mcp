# Balcon MCP Server 🎙️

MCP (Model Context Protocol) server that exposes **Text-to-Speech (TTS)** tools for AI agents, using the **Balabolka CLI (`balcon`)** together with **FFmpeg** for voice synthesis and audio concatenation.

> ⚠️ **Native platform:** Balcon relies on Microsoft's native Speech API (SAPI). **Windows is its native and recommended environment.** On Linux and macOS it can be run through **Wine**, though with limited out-of-the-box voice availability.

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Requirements](#-requirements)
3. [Installing Dependencies](#-installing-dependencies)
   - [Windows (Recommended)](#-windows-native--recommended)
   - [Linux](#-linux)
   - [macOS](#-macos)
4. [MCP Client Configuration](#-mcp-client-configuration)
5. [Python Requirements](#-python-requirements)
6. [Available Tools](#-available-tools)
7. [Usage Examples](#-usage-examples)
8. [Troubleshooting](#-troubleshooting)

---

## ✨ Features

| Tool | Description |
|------|-------------|
| `list_voices` | Lists all SAPI voices installed on the system. |
| `list_audio_devices` | Lists available audio output devices. |
| `text_to_speech` | Converts plain text to a WAV file using a specific voice. |
| `text_file_to_speech` | Converts a text file (`*.txt`) to a WAV audio file. |
| `multi_voice_speech` | Generates combined audio from multiple segments narrated by different voices using FFmpeg. |

---

## 📋 Requirements

- **Operating System:** Windows 10/11 (native). Linux/macOS via Wine.
- **Binaries in `PATH`:**
  - `balcon` — Balabolka CLI ([Download](http://www.cross-plus-a.com/balcon.zip))
  - `ffmpeg` — For multi-voice audio concatenation ([Download](https://www.gyan.dev/ffmpeg/builds/))
- **Python:** 3.10 or higher.
- **Python Package:** `mcp`

---

## 🛠️ Installing Dependencies

### 🪟 Windows (Native & Recommended)

#### 1. Install FFmpeg

Via package manager (recommended):

```powershell
# Using winget (included in Windows 10/11)
winget install ffmpeg

# OR using Scoop
scoop install ffmpeg
```

> If you prefer manual installation: download the ZIP from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin` subfolder to your **System Environment Variables** → `Path`.

#### 2. Install Balcon (CLI)

Balcon does not have a formal installer. Just download it and add it to your `PATH`:

1. Download `balcon.zip` from [cross-plus-a.com](http://www.cross-plus-a.com/balcon.zip).
2. Extract its contents to a permanent folder, for example: `C:\balcon\`.
3. Add that folder to your system `PATH`:
   - Press the Windows key, type *"Environment Variables"* and open it.
   - Click **Environment Variables**.
   - Under *System variables*, find **Path** and click **Edit**.
   - Click **New** and paste the path: `C:\balcon`
   - Click OK and close all windows.

#### 3. Verify Installation

Open a **new** terminal (to refresh the `PATH`) and run:

```bash
ffmpeg -version
balcon -l
```

The `balcon -l` command should display the list of installed SAPI voices.

---

### 🐧 Linux

#### 1. Install FFmpeg and Wine

```bash
sudo apt update
sudo apt install ffmpeg wine unzip
```

#### 2. Install Balcon

```bash
# Download and extract
wget http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Create alias (assuming Bash; change to ~/.zshrc if using Zsh)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.bashrc
source ~/.bashrc
```

#### 3. Verify Installation

```bash
ffmpeg -version
balcon -l
```

> **Note for Linux:** By default, when using Wine, Balcon will only detect SAPI-compatible voices that you explicitly install inside your Wine prefix environment (`~/.wine`).

---

### 🍏 macOS

#### 1. Install FFmpeg and Wine

Requires [Homebrew](https://brew.sh/):

```bash
# Install native FFmpeg
brew install ffmpeg

# Install Wine (required to emulate the Balcon executable)
brew install --cask wine-stable
```

#### 2. Install Balcon

```bash
# Download and extract
curl -O http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Create alias (macOS uses Zsh by default on modern versions)
echo "alias balcon='wine ~/.balcon/balcon.exe'" >> ~/.zshrc
source ~/.zshrc
```

#### 3. Verify Installation

```bash
ffmpeg -version
balcon -l
```

> **Note for macOS:** Balcon will not have access to native Apple voices (like Siri). It will only be able to use Windows-emulated voices that you install inside the Wine environment.

---

## ⚙️ MCP Client Configuration

Once dependencies are installed, connect the TTS server to your MCP client by adding the following configuration to your settings file (usually `mcp_config.json` or similar):

```json
{
  "mcpServers": {
    "balcon-tts": {
      "command": "python",
      "args": [
        "C:/Users/<YOUR_USER>/Downloads/balabolka-mcp/balcon_mcp_server.py"
      ]
    }
  }
}
```

> ⚠️ **Important:**
> - Replace `<YOUR_USER>` with your actual system username.
> - Adjust the path to `balcon_mcp_server.py` according to where you placed it.
> - In the `args` array, use forward slashes (`/`) or double backslashes (`\\`) to avoid JSON escaping issues.

---

## 🐍 Python Requirements

1. **Verify Python is installed:**

   ```bash
   python --version
   ```

2. **Install the MCP package:**

   ```bash
   pip install mcp
   ```

---

## 🔧 Available Tools

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `string` | Text to synthesize. |
| `output_file` | `string` | Full path to the output WAV file. |
| `voice` | `string` (optional) | Exact name of the SAPI voice. Use `list_voices` to see available options. |
| `rate` | `int` (optional) | Speed: `-10` (slow) … `0` (normal) … `10` (fast). |
| `pitch` | `int` (optional) | Pitch: `-10` (low) … `0` (normal) … `10` (high). |
| `volume` | `int` (optional) | Volume: `0` (mute) … `100` (maximum). |
| `freq_khz` | `int` (optional) | Sample rate in kHz (`8`–`48`, default `22`). |
| `bit_depth` | `int` (optional) | Bit depth (`8` or `16`, default `16`). |
| `channels` | `int` (optional) | Audio channels (`1`=mono, `2`=stereo, default `1`). |

---

## 💡 Usage Examples

### Simple audio generation

```json
{
  "text": "Hello, this is a test message.",
  "output_file": "C:/Users/YOUR_USER/Desktop/greeting.wav",
  "voice": "Microsoft Zira Desktop",
  "rate": 1,
  "volume": 90
}
```

### Multi-voice audio generation

```json
{
  "segments": "[\n  {\"text\": \"Welcome to the tutorial.\", \"voice\": \"Microsoft David Desktop\"},\n  {\"text\": \"Today we will learn about MCP.\", \"voice\": \"Microsoft Zira Desktop\", \"rate\": 1, \"pause_before_ms\": 500}\n]",
  "output_file": "C:/Users/YOUR_USER/Desktop/tutorial.wav",
  "default_freq_khz": 22,
  "default_bit_depth": 16,
  "default_channels": 1
}
```

---

## 🩺 Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| `balcon is not recognized` | Not in `PATH` | Add the `balcon.exe` folder to the system `Path` and restart the terminal. |
| `ffmpeg failed to concatenate` | Incompatible version or not installed | Verify with `ffmpeg -version`. Reinstall if necessary. |
| `No voices found` | No SAPI voices installed | On Windows, install language packs with voices from Settings → Time & Language. |
| `balcon failed (code X)` | Text contains unescaped special characters | Ensure the text does not contain unescaped quotes inside the JSON payload. |

---

*README also available in [Spanish](./README.md).*
