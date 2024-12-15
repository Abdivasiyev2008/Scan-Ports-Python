---

# Scan Ports Python 🔍

## Overview
You can check all ports of a website with this Python script! 🚀 Simple and effective for network scanning and security analysis.

---

## Installation 🛠️

### Step 1: Clone the Repository
First of all, you must clone this code to your computer with this command:

```bash
git clone git@github.com:Abdivasiyev2008/Scan-Ports-Python.git
```

---

### Step 2: Install Dependencies
Next, install all necessary Python packages using the following command:

```bash
pip install -r req.txt
```

---

## Usage 🚦

### Help Command
If you don't understand how to use this code, you can get detailed instructions by running:

```bash
python main.py --help
```

---

### Scan Ports with Defaults 🔑
To scan ports using default settings, you just need to enter the target website or IP address. Replace `example.com` with the desired URL:

```bash
python main.py https://example.com
```

---

### Start from a Specific Port 📍
If you want to start scanning from a specific port and go up to port 65535, use:

```bash
python main.py --start [port] https://example.com
```

---

### Add a Port Range Limit ⏳
To scan within a specific port range, define both the start and end ports:

```bash
python main.py --start [start_port] --end [end_port] https://example.com
```

---

## Example Output 🖥️

When scanning, you will see results like this:
```
Scanning target: https://example.com
Ports scanned: 1-65535
Open Ports:
 - Port 22: SSH
 - Port 80: HTTP
 - Port 443: HTTPS
```

---

## Credits 💡
Created by Sunnatillo Abdivasiyev.
