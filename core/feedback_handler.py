"""
Feedback Handler
----------------
Receives user feedback from Investo web form and sends it via Brevo API.
Also saves a local backup file for each submission.
"""

from flask import Blueprint, request, jsonify
import os
import requests
from datetime import datetime
from pathlib import Path
import traceback

# Blueprint setup
feedback_bp = Blueprint("feedback_bp", __name__)

# --- Email Configuration (Brevo API) ---
SENDER_EMAIL = "investosystem@gmail.com"
RECIPIENT_EMAIL = "investosystem@gmail.com"
BREVO_API_KEY = os.getenv("BREVO_API_KEY")  # Stored in Railway environment variables

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


def send_feedback_via_brevo(user: str, message: str) -> bool:
    """Send feedback email using Brevo (Sendinblue) API over HTTPS."""
    if not BREVO_API_KEY:
        print("⚠️ BREVO_API_KEY not set — cannot send email.")
        return False

    subject = f"New Feedback from {user}"
    body = f"User: {user}\n\nMessage:\n{message}"

    payload = {
        "sender": {"name": "Investo Feedback", "email": SENDER_EMAIL},
        "to": [{"email": RECIPIENT_EMAIL}],
        "subject": subject,
        "textContent": body
    }

    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": BREVO_API_KEY,
                "accept": "application/json",
                "content-type": "application/json"
            },
            json=payload,
            timeout=15
        )
        if response.status_code in (200, 201):
            print("✅ Feedback email sent successfully via Brevo API.")
            return True
        else:
            print(f"✗ Brevo API error: {response.status_code} - {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Exception sending via Brevo: {e}")
        traceback.print_exc()
        return False


@feedback_bp.route("/feedback", methods=["POST"])
def receive_feedback():
    """Receive feedback from Investo frontend and forward via Brevo API."""
    print("\n" + "=" * 60)
    print("📨 Received feedback submission")
    print("=" * 60)

    try:
        # --- Get Data ---
        data = request.get_json(force=True, silent=True) or request.form
        user = (data.get("user") or "Anonymous").strip()
        message = (data.get("message") or "").strip()

        print(f"User: {user}")
        print(f"Message length: {len(message)} characters")

        if not message:
            print("❌ Error: Empty message received.")
            return jsonify({"error": "Message cannot be empty."}), 400

        # --- Save feedback locally ---
        file_saved = save_feedback_to_file(user, message)

        # --- Send via Brevo API ---
        email_sent = send_feedback_via_brevo(user, message)

        print("=" * 60 + "\n")

        # --- JSON Response ---
        if email_sent:
            return jsonify({"success": True, "message": "✅ Feedback sent to Investo inbox."}), 200
        elif file_saved:
            return jsonify({"success": True, "message": "✅ Feedback saved locally (email unavailable)."}), 200
        else:
            return jsonify({"error": "⚠️ Could not save or send feedback. Please try again later."}), 500

    except Exception as e:
        print(f"✗ Unexpected error in feedback handler: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Server error: {e}"}), 500
