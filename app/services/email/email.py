from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import ConnectionConfig
from .email_template import render_template
from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
BASEDIR = Path(__file__).resolve().parent.parent.parent
CONFIGDIR = BASEDIR / 'Config.env'
load_dotenv(CONFIGDIR)
BASELINK = os.getenv('BASELINK')

print(BASELINK,CONFIGDIR)
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)

async def send_verification_email(email: str,token: str,username):
    verification_link = (
    f"{BASELINK}verify-email?token={token}")
    
    
    html = render_template(

                        "emails/verify_email.html",

                        title="Verify Email",

                        username=username,

                        verification_link=verification_link,

                        logo_url=f"{BASELINK}app/services/email/logo_image.png")


    message = MessageSchema(
    subject="Verify Your Email",
    recipients=[email],
    body=html,
    subtype="html")


    
    await fm.send_message(message)

async def send_password_refresh_email(email: str,token: str,username):
    verification_link = (
    f"{BASELINK}password/reset-password?token={token}")
    html = render_template(

                        "emails/reset_password.html",

                        title="Reset password",

                        username=username,

                        reset_link=verification_link,

                        logo_url=f"{BASELINK}app/services/email/logo_image.png")
    
    message = MessageSchema(
    subject="Reset your Password",
    recipients=[email],
    body=html,
    subtype="html")

    await fm.send_message(message)


