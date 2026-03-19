# 🛠️ Installation Guide

## Installing Python

Download the latest version of Python from [python.org/downloads](https://www.python.org/downloads/).

**macOS:**

Install via [Homebrew](https://brew.sh/):
```bash
brew install python
```
Or download the macOS installer from [python.org/downloads/macos](https://www.python.org/downloads/macos/).

**Windows:**

Download and run the installer from [python.org/downloads/windows](https://www.python.org/downloads/windows/). Make sure to check **"Add Python to PATH"** during installation.

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install python3
```
Or see [python.org/downloads/source](https://www.python.org/downloads/source/) for source builds.

## Installing pip

pip is included with Python 3.4+. To verify it's installed:
```bash
pip --version
```

If pip is missing, see the official [pip installation guide](https://pip.pypa.io/en/stable/installation/).

**macOS/Linux:**
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

**Windows:**
```bash
python -m ensurepip --upgrade
```

## Verify Installation

```bash
python --version
pip --version
```

## Installing Project Dependencies

```bash
pip install -r requirements.txt
```
