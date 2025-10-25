"""
Feedback Handler
----------------
Receives user feedback from Investo web form and sends it to Gmail inbox.
Also saves a local backup file for each submission.
"""

from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime
from pathlib import Path
import traceback

# Blueprint setup
feedback_bp = Blueprint("feedback_bp", __name__)

# --- Gmail Configuration ---
SENDER_EMAIL = "investosystem@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # App Password required
RECIPIENT_EMAIL = "investosystem@gmail.com"

# --- Feedback Storage Directory ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = PROJECT_ROOT / "feedback"
FEEDBACK_DIR.mkdir(exist_ok=True)


def save_feedback_to_file(user: str, message: str) -> bool:
    """Save feedback to a timestamped file as backup."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = FEEDBACK_DIR / f"feedback_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            f.write(f"User: {user}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Message:\n{message}\n")

        print(f"✓ Feedback saved to: {filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving feedback to file: {e}")
        traceback.print_exc()
        return False


@feedback_bp.route("/feedback", methods=["POST"])
def receive_feedback():
    """Receive feedback from Investo frontend and send to Gmail."""
    print("\n" + "=" * 60)
    print("📨 Received feedback submission")
    print("=" * 60)

    try:
        # --- Get Data ---
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        user = (data.get("user") or "Anonymous").strip()
        message = (data.get("message") or "").strip()

        print(f"User: {user}")
        print(f"Message length: {len(message)} characters")

        if not message:
            print("❌ Error: Empty message received.")
            return jsonify({"error": "Message cannot be empty."}), 400

        # --- Save to file ---
        file_saved = save_feedback_to_file(user, message)

        # --- Send via Gmail ---
        email_sent = False
        if SENDER_PASSWORD:
            try:
                subject = f"New Feedback from {user}"
                body = f"User: {user}\n\nMessage:\n{message}"

                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = SENDER_EMAIL
                msg["To"] = RECIPIENT_EMAIL

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.send_message(msg)

                print("✅ Feedback email sent successfully to Gmail inbox.")
                email_sent = True
            except Exception as e:
                print(f"✗ Error sending Gmail feedback: {e}")
                traceback.print_exc()
        else:
            print("⚠️ GMAIL_APP_PASSWORD not set in environment — skipping email send.")

        print("=" * 60 + "\n")

        # --- JSON Response ---
        if email_sent:
            return jsonify({"success": True, "message": "✅ Thank you! Feedback sent to Investo inbox."}), 200
        elif file_saved:
            return jsonify({"success": True, "message": "✅ Feedback saved locally (email unavailable)."}), 200
        else:
            return jsonify({"error": "⚠️ Could not save or send feedback. Please try again later."}), 500

    except Exception as e:
        print(f"✗ Unexpected error in feedback handler: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Server error: {e}"}), 500
