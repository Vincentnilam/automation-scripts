import subprocess
import pyautogui
import time
import os
from dotenv import load_dotenv

load_dotenv()

PAGEANT_PATH = os.getenv("PAGEANT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
PASSPHRASE = os.getenv("PASSPHRASE")

# Run Pageant with the key
subprocess.Popen([PAGEANT_PATH, KEY_PATH])

# Wait for Pageant to pop up and ask for passphrase
time.sleep(2)

# Enter passphrase and enter
pyautogui.typewrite(PASSPHRASE)
pyautogui.press('enter')