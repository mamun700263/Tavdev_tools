# app/core/email.py

import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_verification_email(email: str, token: str):
    # this will be the link the user clicks
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    verify_url = f"{base_url}/accounts/verify/{token}"

    body = f"""
    <h2>Verify your email</h2>
    <p>Click the link below to verify your account:</p>
    <a href="{verify_url}">{verify_url}</a>
    <p>This link expires in 24 hours.</p>
    <p>If you didn't create an account, ignore this email.</p>
    """

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)