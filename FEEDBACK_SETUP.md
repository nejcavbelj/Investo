# 📬 Investo Feedback System Setup Guide

## Overview
The Investo Feedback System allows users to send feedback, suggestions, and bug reports directly from generated HTML reports to your Gmail inbox.

## Architecture
- **Frontend**: Feedback form embedded in HTML reports (`templates/combined_template.html`)
- **Backend**: Flask web server (`app.py`) that handles form submissions and sends emails
- **Email Service**: Gmail SMTP for sending feedback emails

---

## Setup Instructions

### Step 1: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable if not already enabled)
3. Scroll down to **App passwords**: https://myaccount.google.com/apppasswords
4. Generate a new app password:
   - **App**: Select "Mail"
   - **Device**: Select "Windows Computer" or "Other (Custom name)"
   - Click **Generate**
5. Copy the 16-character password (remove spaces)

### Step 2: Configure Environment Variables

1. Make sure you have a `.env` file in the project root
2. Add the following line to your `.env` file:
   ```
   GMAIL_APP_PASSWORD=your_16_character_app_password_here
   ```

### Step 3: Install Required Dependencies

Make sure Flask is installed:
```bash
pip install flask python-dotenv
```

---

## Usage

### Running the Feedback Server

**Option 1: Run in a separate terminal**
```bash
python app.py
```

**Option 2: Run in background (Windows PowerShell)**
```powershell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

**Option 3: Run in background (Command Prompt)**
```cmd
start /B python app.py
```

The server will start on `http://localhost:5000`

### Using the Main Application

1. **Start the feedback server** (as shown above)
2. **Run the main Investo application**:
   ```bash
   python main.py
   ```
3. **Generate a report** by entering a stock ticker
4. **Open the generated HTML report** in your browser
5. **Scroll to the bottom** to find the feedback form
6. **Submit feedback** - it will be sent to `investosystem@gmail.com`

---

## How It Works

### 1. User Submits Feedback
- User fills out the feedback form at the bottom of any Investo report
- Form includes:
  - Message (required)
  - Name (optional)

### 2. Form Submission
- Form sends POST request to `http://localhost:5000/feedback`
- Opens in a new tab to show submission status

### 3. Email Delivery
- Flask server receives the form data
- Creates a formatted HTML email
- Sends via Gmail SMTP to `investosystem@gmail.com`
- Shows success/error page to user

### 4. Confirmation
- Success: Green confirmation page (auto-closes after 3 seconds)
- Error: Red error page with details

---

## Email Format

Feedback emails are sent in both HTML and plain text formats:

### HTML Email Includes:
- 🚀 Investo branded header
- Sender name (or "Anonymous")
- Full feedback message
- Professional formatting

### Subject Line:
```
📬 New Investo Feedback from [Name]
```

---

## Customization

### Change Recipient Email

Edit `app.py`:
```python
RECIPIENT_EMAIL = "your_email@gmail.com"
```

### Change Sender Email

Edit `app.py`:
```python
SENDER_EMAIL = "your_email@gmail.com"
```

⚠️ **Note**: The sender email should match the Gmail account that generated the app password.

### Change Server Port

Edit `app.py` (bottom of file):
```python
app.run(host='0.0.0.0', port=5000, debug=False)  # Change 5000 to your preferred port
```

Then update the form action in `templates/combined_template.html`:
```html
<form method="post" action="http://localhost:YOUR_PORT/feedback" target="_blank">
```

---

## Troubleshooting

### Issue: "GMAIL_APP_PASSWORD not set"
**Solution**: 
- Make sure `.env` file exists in project root
- Verify `GMAIL_APP_PASSWORD` is set correctly (no spaces)
- Restart the Flask server after adding the password

### Issue: "Connection refused" or "Cannot POST"
**Solution**: 
- Make sure the Flask server (`app.py`) is running
- Check that the server is on port 5000: `http://localhost:5000`
- Verify no firewall is blocking port 5000

### Issue: "Authentication failed" (535 error)
**Solution**: 
- Verify the app password is correct (16 characters, no spaces)
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Step Verification is enabled on your Google account

### Issue: Feedback form not showing
**Solution**: 
- Regenerate the HTML report (old reports won't have the form)
- Make sure you're viewing the latest report in `reports/generated/`
- Clear browser cache and refresh

### Issue: Email not received
**Solution**: 
- Check spam/junk folder
- Verify `RECIPIENT_EMAIL` in `app.py` is correct
- Check Flask server logs for errors
- Test with a simple message

---

## Testing

### Test the Feedback Server

1. Start the server:
   ```bash
   python app.py
   ```

2. You should see:
   ```
   ============================================================
   🚀 Starting Investo Feedback Server
   ============================================================
   Server will run on: http://localhost:5000
   Feedback endpoint: http://localhost:5000/feedback
   Feedback will be sent to: investosystem@gmail.com
   ============================================================
   ```

3. Open browser and go to: `http://localhost:5000`
   - You should see a green "ONLINE" status page

### Test End-to-End

```bash
# Terminal 1: Start feedback server
python app.py

# Terminal 2: Generate a test report
python -c "from reports.combined_report_generator import create_combined_report; create_combined_report('AAPL')"
```

Then open the generated report and submit test feedback.

---

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never commit `.env` file** to git
2. **App passwords should be kept secret**
3. The feedback server runs on **localhost only** by default
4. For production deployment, use HTTPS and proper authentication
5. Consider rate limiting for production use

---

## Production Deployment

For deploying to a web server:

1. **Use environment variables** for configuration
2. **Enable HTTPS** (use a reverse proxy like Nginx)
3. **Add rate limiting** to prevent spam
4. **Implement CAPTCHA** for spam protection
5. **Use a proper WSGI server** (Gunicorn, uWSGI)
6. **Set up logging** for monitoring

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## File Structure

```
Investo/
├── app.py                          # Flask feedback server
├── main.py                         # Main Investo application
├── .env                            # Environment variables (not in git)
├── config/
│   ├── __init__.py                 # Config loader (includes GMAIL_APP_PASSWORD)
│   └── credentials_example.env     # Example credentials file
├── templates/
│   └── combined_template.html      # Report template with feedback form
└── FEEDBACK_SETUP.md              # This file
```

---

## Quick Start Checklist

- [ ] Generate Gmail App Password
- [ ] Add `GMAIL_APP_PASSWORD` to `.env` file
- [ ] Install Flask: `pip install flask`
- [ ] Test the feedback server: `python app.py`
- [ ] Generate a test report: `python main.py`
- [ ] Submit test feedback from the report
- [ ] Check email inbox for feedback

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Flask server logs for error messages
- Verify all environment variables are set correctly
- Test Gmail SMTP connection separately if needed

---

**Happy Analyzing! 🚀**

