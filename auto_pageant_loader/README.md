# Auto Pageant Loader

This is a simple Python automation script that runs Pageant and auto-loads a private key with its passphrase using PyAutoGUI.

## Features

- Launches PuTTY Pageant
- Loads your `.ppk` key automatically
- Auto-types the passphrase so you don’t have to

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Create a .env file (can refer to .env.sample):
   ```
   PAGEANT_PATH="C:/Path/To/pageant.exe"
   KEY_PATH="C:/Path/To/yourkey.ppk"
   PASSPHRASE="your-passphrase"
3. Run the script:
   ```bash
   python auto_pageant.py

NB: Windows only. Tested on Python 3.11