import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Credentials
TELEGRAM_BOT_TOKEN = "8694739391:AAFyJm-HCUu9tySAbRJmDqhfc-UHdcaBkmk"
TELEGRAM_CHAT_ID = "712396656"

EMAIL_SENDER = "zainalishah7786@gmail.com"
EMAIL_RECEIVER = "instafacebook134@gmail.com"
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram Response:", response.text)
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_email_message(subject, body):
    if not EMAIL_PASSWORD:
        print("Email Error: GMAIL_PASSWORD secret is missing or not loaded!")
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email Error: {e}")

if __name__ == "__main__":
    print("Running test notification script...")
    test_message = "🚨 *Instant Demo Alert!* GitHub Actions ki taraf se test message successfully pohch gaya hai."
    
    send_telegram_message(test_message)
    send_email_message("GitHub Tracker Instant Demo Alert", test_message)
