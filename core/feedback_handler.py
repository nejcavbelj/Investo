"""
Feedback Handler
----------------
Receives user feedback from Investo report form and sends it to your Gmail inbox.
"""

from flask import Blueprint, request, redirect, flash, jsonify
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime
from pathlib import Path

feedback_bp = Blueprint("feedback_bp", __name__)

# --- Gmail Config ---
SENDER_EMAIL = "investosystem@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not main password
RECIPIENT_EMAIL = "investosystem@gmail.com"

# --- Feedback Storage ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = PROJECT_ROOT / "feedback"
FEEDBACK_DIR.mkdir(exist_ok=True)

def save_feedback_to_file(user, message):
    """Save feedback to a file as backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = FEEDBACK_DIR / f"feedback_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User: {user}\n")
            f.write(f"{'='*60}\n")
            f.write(f"Message:\n{message}\n")
        print(f"✓ Feedback saved to: {filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving feedback to file: {e}")
        return False

@feedback_bp.route("/feedback", methods=["POST"])
def receive_feedback():
    """Handle feedback form submission"""
    print("\n" + "="*60)
    print("Received feedback submission")
    print("="*60)
    
    try:
        user = request.form.get("user", "Anonymous").strip() or "Anonymous"
        message = request.form.get("message", "").strip()
        
        print(f"User: {user}")
        print(f"Message length: {len(message)} characters")

        if not message:
            print("ERROR: Empty message")
            flash("Message cannot be empty.", "error")
            return redirect(request.referrer or "/")

        # Always save to file first
        file_saved = save_feedback_to_file(user, message)

        # Try to send email if credentials are configured
        email_sent = False
        if SENDER_PASSWORD:
            try:
                # Compose email
                subject = f"New Feedback from {user}"
                body = f"User: {user}\n\nMessage:\n{message}"
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = SENDER_EMAIL
                msg["To"] = RECIPIENT_EMAIL

                # Send via Gmail SMTP
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.send_message(msg)
                
                print("✓ Email sent successfully")
                email_sent = True
            except Exception as e:
                print(f"✗ Error sending email: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠ GMAIL_APP_PASSWORD not configured - email not sent")

        # Show success message
        if email_sent:
            flash("✅ Thank you for your feedback! We've received your message via email.", "success")
        elif file_saved:
            flash("✅ Thank you for your feedback! Your message has been saved.", "success")
        else:
            flash("⚠️ Feedback received but could not be saved. Please try again.", "error")

        print("="*60 + "\n")
        
        # Safe redirect
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        else:
            return redirect("/")
            
    except Exception as e:
        print(f"✗ Unexpected error in feedback handler: {e}")
        import traceback
        traceback.print_exc()
        flash("❌ An error occurred. Please try again later.", "error")
        return redirect(request.referrer or "/")
