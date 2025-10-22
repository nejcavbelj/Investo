"""
Investo Feedback Server
========================
Flask web server to handle feedback submissions from generated HTML reports.
Run this alongside the main Investo application to receive user feedback.
"""

from flask import Flask, request, redirect, render_template_string, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import load_config
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secret key for sessions

# Load configuration
config = load_config()

# Gmail Configuration
SENDER_EMAIL = "investosystem@gmail.com"
RECIPIENT_EMAIL = "investosystem@gmail.com"


@app.route("/")
def index():
    """Landing page"""
    return """
    <html>
    <head>
        <title>Investo Feedback Server</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                background: #222;
                padding: 3em;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(255, 165, 0, 0.2);
                border: 1px solid #FFA500;
            }
            h1 {
                color: #FFA500;
                margin-bottom: 0.5em;
                font-size: 2.5em;
            }
            p {
                color: #aaa;
                font-size: 1.1em;
            }
            .status {
                display: inline-block;
                background: #00FF00;
                color: #000;
                padding: 0.5em 1em;
                border-radius: 20px;
                margin-top: 1em;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Investo Feedback Server</h1>
            <p>The feedback server is running successfully!</p>
            <div class="status">ONLINE</div>
            <p style="margin-top: 2em; font-size: 0.9em;">
                This server handles feedback submissions from Investo reports.
            </p>
        </div>
    </body>
    </html>
    """


@app.route("/feedback", methods=["POST"])
def receive_feedback():
    """Handle feedback form submissions"""
    try:
        user = request.form.get("user", "Anonymous").strip() or "Anonymous"
        message = request.form.get("message", "").strip()
    except Exception as e:
        print(f"Error parsing form data: {e}")
        return f"<h1>Error</h1><p>Error parsing form data: {e}</p>", 500

    if not message:
        # Return a simple error page
        return """
        <html>
        <head>
            <title>Error - Investo Feedback</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #1a1a1a;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    background: #222;
                    padding: 3em;
                    border-radius: 15px;
                }
                h1 { color: #FF3C00; }
                a {
                    color: #FFA500;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 1em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Error</h1>
                <p>Message cannot be empty.</p>
                <a href="javascript:history.back()">← Go Back</a>
            </div>
        </body>
        </html>
        """

    # Get Gmail app password from config
    gmail_password = config.get('GMAIL_APP_PASSWORD')
    
    if not gmail_password:
        print("ERROR: GMAIL_APP_PASSWORD not set in .env file")
        return """
        <html>
        <head>
            <title>Configuration Error - Investo Feedback</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #1a1a1a;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    background: #222;
                    padding: 3em;
                    border-radius: 15px;
                }
                h1 { color: #FF3C00; }
                p { color: #aaa; margin: 1em 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚙️ Configuration Error</h1>
                <p>Gmail app password is not configured.</p>
                <p>Please add GMAIL_APP_PASSWORD to your .env file.</p>
            </div>
        </body>
        </html>
        """

    # Compose email
    subject = f"New Investo Feedback from {user}"
    
    # Create HTML email
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f5f5f5;
                padding: 20px;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .user-info {{
                background: #f9f9f9;
                border-left: 4px solid #FFA500;
                padding: 15px;
                margin-bottom: 20px;
            }}
            .message-box {{
                background: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                line-height: 1.6;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #888;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>New Feedback from Investo User</h1>
            </div>
            <div class="content">
                <div class="user-info">
                    <strong>From:</strong> {user}
                </div>
                <div class="message-box">
                    <strong>Message:</strong><br><br>
                    {message.replace(chr(10), '<br>')}
                </div>
            </div>
            <div class="footer">
                Sent via Investo Feedback System
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    text_body = f"""
New Investo Feedback

From: {user}

Message:
{message}

---
Sent via Investo Feedback System
    """
    
    # Create MIME message
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    
    # Attach both plain text and HTML versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Send via Gmail SMTP
        print(f"Sending feedback email from {user}...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, gmail_password)
            server.send_message(msg)
        
        print(f"✓ Feedback email sent successfully!")
        
        # Return success page
        return """
        <html>
        <head>
            <title>Thank You - Investo Feedback</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    background: #222;
                    padding: 3em;
                    border-radius: 15px;
                    box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
                    border: 1px solid #00FF00;
                }
                h1 {
                    color: #00FF00;
                    margin-bottom: 0.5em;
                    font-size: 2.5em;
                }
                p {
                    color: #aaa;
                    font-size: 1.1em;
                }
                .checkmark {
                    font-size: 4em;
                    margin-bottom: 0.2em;
                }
                a {
                    color: #FFA500;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 1em;
                    padding: 0.5em 1em;
                    border: 1px solid #FFA500;
                    border-radius: 5px;
                    transition: all 0.3s;
                }
                a:hover {
                    background: #FFA500;
                    color: #000;
                }
            </style>
            <script>
                // Auto-close after 3 seconds
                setTimeout(function() {
                    window.close();
                }, 3000);
            </script>
        </head>
        <body>
            <div class="container">
                <div class="checkmark">✓</div>
                <h1>Thank You!</h1>
                <p>Your feedback has been sent successfully.</p>
                <p style="font-size: 0.9em; color: #666;">This window will close automatically...</p>
                <a href="javascript:window.close()">Close Window</a>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        
        # Return error page
        return f"""
        <html>
        <head>
            <title>Error - Investo Feedback</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #1a1a1a;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .container {{
                    text-align: center;
                    background: #222;
                    padding: 3em;
                    border-radius: 15px;
                    border: 1px solid #FF3C00;
                }}
                h1 {{ color: #FF3C00; }}
                p {{ color: #aaa; margin: 1em 0; }}
                .error-details {{
                    background: #1a1a1a;
                    padding: 1em;
                    border-radius: 5px;
                    margin-top: 1em;
                    font-family: monospace;
                    font-size: 0.9em;
                    color: #ff6b6b;
                }}
                a {{
                    color: #FFA500;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 1em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Failed to Send Feedback</h1>
                <p>An error occurred while sending your feedback.</p>
                <div class="error-details">{str(e)}</div>
                <p style="margin-top: 2em;">Please try again later or contact support directly.</p>
                <a href="javascript:history.back()">← Go Back</a>
            </div>
        </body>
        </html>
        """


if __name__ == "__main__":
    print("=" * 60)
    print("Starting Investo Feedback Server")
    print("=" * 60)
    print(f"Server will run on: http://localhost:5000")
    print(f"Feedback endpoint: http://localhost:5000/feedback")
    print(f"Feedback will be sent to: {RECIPIENT_EMAIL}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
