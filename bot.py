import os
import requests
import time

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')
LAST_MESSAGE_ID = None

print("🚀 FiveM Status Bot Started!")

def get_last_message():
    global LAST_MESSAGE_ID
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=5"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                if msg['author']['bot']:
                    LAST_MESSAGE_ID = msg['id']
                    return LAST_MESSAGE_ID
        return None
    except Exception as e:
        print(f"❌ Error finding message: {e}")
        return None

def send_or_edit_message():
    global LAST_MESSAGE_ID
    try:
        current_seconds = (int(time.time()) % 60) + 1
        
        embed = {
            "title": "🔥 FiveM Status",
            "color": 0x00ff00,
            "fields": [
                {"name": "Last Update", "value": f"{current_seconds} seconds ago", "inline": False}
            ],
            "footer": {"text": "24/7 Online"}
        }
        
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {"embeds": [embed]}
        
        # إذا في رسالة قديمة، عدلها
        if LAST_MESSAGE_ID:
            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{LAST_MESSAGE_ID}"
            response = requests.patch(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ Updated: {current_seconds}s")
                return True
            else:
                print(f"❌ Edit failed: {response.status_code}")
                LAST_MESSAGE_ID = None
        
        # إذا مافي، أنشئ رسالة جديدة
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            LAST_MESSAGE_ID = response.json()['id']
            print(f"✅ New message: {current_seconds}s")
            return True
        else:
            print(f"❌ Send failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# جلب آخر رسالة عند البدء
if LAST_MESSAGE_ID is None:
    get_last_message()

# التشغيل الرئيسي
while True:
    send_or_edit_message()
    time.sleep(5)  # كل 5 ثواني
