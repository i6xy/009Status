import os
import requests
from datetime import datetime
import time

# إعدادات البوت
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')
LAST_MESSAGE_ID = None

def get_fivem_status():
    """جلب حالة FiveM مع وقت يرجع لصفر كل 60 ثانية"""
    try:
        # حساب الثواني الحالية في الدقيقة (0-59)
        current_seconds = int(time.time()) % 60
        
        status_data = {
            "Cfx Status": {"status": "<:online:795669431044145192>", "description": "حالة الفايف ام"},
            "CnL": {"status": "<:online:795669431044145192>", "description": "التحقق من اللاعب عند الاتصال بالسيرفر"},
            "Policy": {"status": "<:online:795669431044145192>", "description": "اتصال السيرفرات بسيرفرات فايف إم"},
            "Keymaster": {"status": "<:online:795669431044145192>", "description": "التحقق من الايسن كي"},
            "Server List": {"status": "<:online:795669431044145192>", "description": "عرض قائمة السيرفرات المتصلة"},
            "License Status": {"status": "<:online:795669431044145192>", "description": "نظام الرخص"},
            "Last Update": f"{current_seconds} seconds ago",
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def get_last_bot_message():
    global LAST_MESSAGE_ID
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=10"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                if msg['author']['bot'] and any('Status' in str(field.get('name', '')) for field in msg.get('embeds', [{}])[0].get('fields', [])):
                    LAST_MESSAGE_ID = msg['id']
                    return LAST_MESSAGE_ID
        return None
    except:
        return None

def create_discord_embed(status_data):
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,
        "fields": [
            {"name": "**Cfx Status:**", "value": f"Status {status_data['Cfx Status']['status']}\nDescription: {status_data['Cfx Status']['description']}", "inline": False},
            {"name": "**CnL:**", "value": f"Status {status_data['CnL']['status']}\nDescription: {status_data['CnL']['description']}", "inline": False},
            {"name": "**Policy:**", "value": f"Status {status_data['Policy']['status']}\nDescription: {status_data['Policy']['description']}", "inline": False},
            {"name": "**Keymaster:**", "value": f"Status {status_data['Keymaster']['status']}\nDescription: {status_data['Keymaster']['description']}", "inline": False},
            {"name": "**Server List:**", "value": f"Status {status_data['Server List']['status']}\nDescription: {status_data['Server List']['description']}", "inline": False},
            {"name": "**License Status:**", "value": f"Status {status_data['License Status']['status']}\nDescription: {status_data['License Status']['description']}", "inline": False},
            {"name": "**Last Update:**", "value": status_data["Last Update"], "inline": False}
        ],
        "footer": {"text": f"Total Requests {status_data['Total Requests']} • Today at {datetime.now().strftime('%I:%M %p')}"}
    }
    return embed

def send_or_edit_message(embed_data):
    global LAST_MESSAGE_ID
    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    data = {"embeds": [embed_data]}
    
    try:
        if LAST_MESSAGE_ID:
            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{LAST_MESSAGE_ID}"
            response = requests.patch(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                return True
            else:
                LAST_MESSAGE_ID = None
        
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            LAST_MESSAGE_ID = response.json()['id']
            return True
        return False
    except:
        return False

def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ لم يتم تعيين التوكن أو الروم")
        return
    
    get_last_bot_message()
    status_data = get_fivem_status()
    
    if status_data:
        embed = create_discord_embed(status_data)
        success = send_or_edit_message(embed)
        print("✅ تم التحديث" if success else "❌ فشل التحديث")

if __name__ == "__main__":
    main()
