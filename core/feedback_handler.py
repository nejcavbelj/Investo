"""
Feedback Handler
----------------
Receives user feedback from Investo report form and sends it to your Gmail inbox.
"""

from flask import Blueprint, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
import os

feedback_bp = Blueprint("feedback_bp", __name__)

# --- Gmail Config ---
SENDER_EMAIL = "investosystem@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not main password
RECIPIENT_EMAIL = "investosystem@gmail.com"

@feedback_bp.route("/feedback", methods=["POST"])
def receive_feedback():
    user = request.form.get("user", "Anonymous").strip() or "Anonymous"
    message = request.form.get("message", "").strip()

    if not message:
        flash("Message cannot be empty.", "error")
        return redirect(request.referrer or "/")

    # Compose email
    subject = f"New Feedback from {user}"
    body = f"User: {user}\n\nMessage:\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    try:
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        flash("✅ Thank you for your feedback!", "success")
    except Exception as e:
        print(f"Error sending email: {e}")
        flash("❌ Failed to send feedback. Please try again later.", "error")

    return redirect(request.referrer or "/")
