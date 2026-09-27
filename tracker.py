import requests
from bs4 import BeautifulSoup
import os

# Website jise track karna hai
URL = "https://new.microtv.st/"

# Aapke Telegram credentials jo humne banaye thay
TELEGRAM_BOT_TOKEN = "8694739391:AAFyJm-HCUu9tySAbRJmDqhfc-UHdcaBkmk"
TELEGRAM_CHAT_ID = "712396656"

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
        print(f"Error sending message: {e}")

def check_website():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Yahan hum page ka text ya pehla video title nikal rahe hain
            # (Aapki zaroorat ke mutabiq yeh basic check hai)
            current_content = soup.get_text()
            
            # Simple logic: Hum check karenge ke file mein pehle kya save tha
            file_name = "last_content.txt"
            
            if os.path.exists(file_name):
                with open(file_name, "r", encoding="utf-8") as f:
                    old_content = f.read()
                
                if current_content != old_content:
                    send_telegram_message("🚨 *Alert!* MicroTV website par koi nayi update ya video aayi hai!\n\nCheck karein: https://new.microtv.st/")
                    # Naya content save kar lein
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(current_content)
            else:
                # Pehli dafa file nahi thi toh save kar lo
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(current_content)
                print("Initial state saved.")
                
        else:
            print(f"Website error: {response.status_code}")
    except Exception as e:
        print(f"Error fetching website: {e}")

if __name__ == "__main__":
    check_website()
