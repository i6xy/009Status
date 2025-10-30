import os
import requests
from datetime import datetime
import random

# التوكن من Environment Variables
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')

def get_fivem_status():
    """جلب حالة FiveM"""
    try:
        random_seconds = random.randint(1, 60)
        current_time = datetime.now()
        
        status_data = {
            "Last Update": f"{random_seconds} seconds ago",
            "Total Requests": str(343823 + random.randint(1, 100)),
            "Current Time": current_time.strftime("Today at %I:%M %p")
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_embed(status_data):
    """إنشاء رسالة إمبدد"""
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "**Cfx Status:**",
                "value": f"Status █\nDescription: حالة الفايف ام",
                "inline": False
            },
            {
                "name": "**Last Update:**",
                "value": status_data["Last Update"],
                "inline": False
            }
        ],
        "footer": {
            "text": f"Total Requests {status_data['Total Requests']} • {status_data['Current Time']}"
        }
    }
    return embed

def get_last_message():
    """جلب آخر رسالة من البوت"""
    if not BOT_TOKEN or not CHANNEL_ID:
        return None
        
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=5"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                if msg['author']['bot']:
                    return msg['id']
        return None
    except:
        return None

def send_bot_message(embed_data, message_id=None):
    """إرسال أو تعديل رسالة البوت"""
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ لم يتم تعيين التوكن أو رقم الروم")
        return False
        
    try:
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "embeds": [embed_data]
        }
        
        if message_id:
            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{message_id}"
            response = requests.patch(url, json=data, headers=headers, timeout=10)
        else:
            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
            response = requests.post(url, json=data, headers=headers, timeout=10)
        
        return response.status_code == 200
    except:
        return False

def main():
    """الدالة الرئيسية"""
    if not BOT_TOKEN:
        print("❌ لم يتم تعيين DISCORD_BOT_TOKEN في Secrets")
        return
        
    if not CHANNEL_ID:
        print("❌ لم يتم تعيين DISCORD_CHANNEL_ID في Secrets")
        return
    
    print("🚀 بدأ المراقبة...")
    
    last_message_id = get_last_message()
    status_data = get_fivem_status()
    
    if status_data:
        embed = create_discord_embed(status_data)
        success = send_bot_message(embed, last_message_id)
        print("✅ تم التحديث" if success else "❌ فشل التحديث")

if __name__ == "__main__":
    main()
