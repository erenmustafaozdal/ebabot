from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, encoding="UTF-8")
if os.name == "nt":
	web_profile = os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data"
if os.name == "posix":
	web_profile = os.getenv("HOME") + "/.config/chromium/"
users_xl = os.getenv("USERS_EXCEL")
driver_path = os.getenv("DRIVER_PATH")
web_headless = False if os.getenv("WEB_HEADLESS")=="" else (os.getenv("WEB_HEADLESS") == 'True')
web_implicitly_wait= 3 if os.getenv("WEB_IMPLICITLY_WAIT")=="" else os.getenv("WEB_IMPLICITLY_WAIT")

web_size= "max" if os.getenv("WEB_SIZE")=="" else os.getenv("WEB_SIZE")
if web_size != "max":
    web_size = [int(i) for i in web_size.split(",")]

eba_user_sign = False if os.getenv ("EBA_USER_LOGIN")=="" else (os.getenv ("EBA_USER_LOGIN") == 'True')
