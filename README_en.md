# ## ⚙️ MCP Client Configuration

To connect the Balcon TTS server to your MCP client, you will need to configure your client's settings file (usually `mcp_config.json` or similar). 

Below is an example configuration. **Remember to replace `<YOUR_USER>`** with your actual system username and adjust the path to where `balcon_mcp_server.py` is located.

```json
{
  "mcpServers": {
    "balcon-tts": {
      "command": "python",
      "args": [
        "C:/Users/<YOUR_USER>/.gemini/antigravity/balcon_mcp_server.py"
      ]
    }
  }
}

# 🛠️ Setup Guide: Dependencies for Balcon MCP

To run **Balcon MCP** properly, your system requires two key dependencies to be installed and available in your system's `PATH`:

1. **FFmpeg**: Handles audio processing, conversion, and formatting.
2. **Balcon**: The command-line interface (CLI) for Balabolka, responsible for the Text-to-Speech (TTS) synthesis.

> ⚠️ **Compatibility Notice:** Balcon relies on the native Microsoft Speech API (SAPI), meaning **Windows is its native and recommended environment**. For Linux and macOS, you will need to run it through **Wine**. Note that non-Windows systems will only have access to the TTS voices you manually install inside the Wine environment.

Below are the installation instructions for each operating system.

---

## 🪟 Windows (Native & Recommended)

### 1. Install FFmpeg

The fastest way is using a Windows package manager. Open **PowerShell** and run:

```powershell
# Using Winget (Built-in on Windows 10/11)
winget install ffmpeg

# OR using Scoop:
scoop install ffmpeg
```

*(If you prefer to install it manually: download the ZIP from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and **you must manually add the `bin` folder to your system's `PATH`**).*

### 2. Install Balcon (CLI)

Balcon doesn't have an installer. You just need to download the executable and add it to your PATH.

1. Download the official `.zip` file from [Cross+A (balcon.zip)](http://www.cross-plus-a.com/balcon.zip).
2. Extract the contents to a permanent folder, for example: `C:\balcon\`
3. **Add this folder to your system `PATH`** (Crucial for the MCP to find it):
   - Press the Windows key, type *"Environment Variables"* and select **Edit the system environment variables**.
   - Click the **Environment Variables...** button.
   - Under *System variables* (or *User variables*), find the **Path** variable and click **Edit**.
   - Click **New** and paste the exact path: `C:\balcon`
   - Click OK to save and close all windows.

### 3. Verify Installation

Open a **new** terminal (to refresh the PATH) and check if both commands are recognized:

```bash
ffmpeg -version
balcon -l
```

*(The `balcon -l` command will list all available SAPI voices installed on your Windows system).*

---

## 🐧 Linux

### 1. Install FFmpeg and Wine

Since Balcon is a `.exe` file, we need **Wine** to run it, along with FFmpeg. On Debian/Ubuntu-based distros, open your terminal:

```bash
sudo apt update
sudo apt install ffmpeg wine unzip
```

*(Note: Package managers automatically add `ffmpeg` and `wine` to your PATH).*

### 2. Install Balcon

We will download Balcon, extract it to a hidden folder, and create an executable wrapper script in `~/.local/bin` so the MCP server can execute it like a native command.

```bash
# Download and extract
wget http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Create a wrapper script in ~/.local/bin
mkdir -p ~/.local/bin
echo '#!/bin/bash' > ~/.local/bin/balcon
echo 'wine ~/.balcon/balcon.exe "$@"' >> ~/.local/bin/balcon
chmod +x ~/.local/bin/balcon
```

### 3. Add to PATH (If you haven't already)

Ensure `~/.local/bin` is in your system's PATH. Add this line to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Apply the changes:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

### 4. Verify Installation

```bash
ffmpeg -version
balcon -l
```

---

## 🍏 macOS

### 1. Install FFmpeg and Wine

We will use [Homebrew](https://brew.sh/). If you don't have it, install it first. Then, run:

```bash
# Install native FFmpeg
brew install ffmpeg

# Install Wine to emulate the Windows .exe
brew install --cask wine-stable
```

### 2. Install Balcon

Similar to Linux, we will download it and create a wrapper script.

```bash
# Download and extract
curl -O http://www.cross-plus-a.com/balcon.zip
unzip balcon.zip -d ~/.balcon

# Create a wrapper script in a standard local bin directory
mkdir -p ~/.local/bin
echo '#!/bin/bash' > ~/.local/bin/balcon
echo 'wine ~/.balcon/balcon.exe "$@"' >> ~/.local/bin/balcon
chmod +x ~/.local/bin/balcon
```

### 3. Add to PATH (If you haven't already)

macOS uses Zsh by default. Ensure `~/.local/bin` is in your PATH so the MCP can find the `balcon` command globally:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Verify Installation

```bash
ffmpeg -version
balcon -l
```

> **macOS Note:** Balcon will not have access to native Apple voices (like Siri). The engine will only read voices installed inside the Wine environment.



# 🐍 Final Checklist: Python Requirements


Since this MCP server is built with Python, please ensure you have the following ready before trying to run it:


1. **Python Installed & in PATH**: Make sure Python is installed on your system and added to your environment variables (`PATH`). You can verify this by opening a terminal and running:




```
python --version
```

   

2. **Install the MCP Package**: The server requires the official MCP Python library to communicate. Install it via pip by running:
   
   ```bash
   pip install mcp
   ```
   
      
