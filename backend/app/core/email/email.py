import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")


async def send_verification_email(email: str, token: str):
    base_url = os.getenv("BASE_URL", "http://localhost:3000")
    verify_url = f"{base_url}/verify?token={token}"

    params = {
        "from": "Bestoolify <onboarding@resend.dev>",
        "to": [email],
        "subject": "Verify your email",
        "html": f"""
            <h2>Verify your email</h2>
            <p>Click the link below to verify your account:</p>
            <a href="{verify_url}">{verify_url}</a>
            <p>This link expires in 24 hours.</p>
            <p>If you didn't create an account, ignore this email.</p>
        """,
    }

    resend.Emails.send(params)