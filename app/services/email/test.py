from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
BASEDIR = Path(__file__).resolve().parent.parent.parent
CONFIGDIR = BASEDIR / 'config.env'
load_dotenv(CONFIGDIR)
BASELINK = os.getenv('BASELINK')
print(CONFIGDIR)
print(BASELINK)



MAIL_USERNAME=os.getenv("MAIL_USERNAME")
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
print(MAIL_PASSWORD)