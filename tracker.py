import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Demo ke liye example.com use kar rahe hain
URL = "https://example.com/"

# Telegram Credentials
TELEGRAM_BOT_TOKEN = "8694739391:AAFyJm-HCUu9tySAbRJmDqhfc-UHdcaBkmk"
TELEGRAM_CHAT_ID = "712396656"

# Email Credentials
EMAIL_SENDER = "zainalishah7786@gmail.com"        # Jis account se email jaayegi (App Password wala)
EMAIL_RECEIVER = "instafacebook134@gmail.com"     # Jis email par aapko receive karni hai
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_email_message(subject, body):
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

def check_website():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            current_content = soup.get_text()
            file_name = "last_content.txt"
            
            alert_msg = "🚨 *Alert!* Website par nayi update aayi hai!\n\nCheck karein: " + URL

            if os.path.exists(file_name):
                with open(file_name, "r", encoding="utf-8") as f:
                    old_content = f.read()
                
                if current_content != old_content:
                    send_telegram_message(alert_msg)
                    send_email_message("Website Update Alert!", alert_msg)
                    
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(current_content)
            else:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(current_content)
                print("Initial state saved.")
        else:
            print(f"Website error: {response.status_code}")
    except Exception as e:
        print(f"Error fetching website: {e}")

if __name__ == "__main__":
    check_website()
