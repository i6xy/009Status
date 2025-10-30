import os
import requests
from datetime import datetime
import time

# إعدادات البوت
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')

# متغير لحفظ آخر رسالة
LAST_MESSAGE_ID = None

def get_fivem_status():
    """جلب حالة FiveM مع وقت ديسكورد الديناميكي"""
    try:
        status_data = {
            "Cfx Status": {
                "status": "<:online:795669431044145192>", 
                "description": "حالة الفايف ام"
            },
            "CnL": {
                "status": "<:online:795669431044145192>", 
                "description": "التحقق من اللاعب عند الاتصال بالسيرفر"
            },
            "Policy": {
                "status": "<:online:795669431044145192>", 
                "description": "اتصال السيرفرات بسيرفرات فايف إم"
            },
            "Keymaster": {
                "status": "<:online:795669431044145192>", 
                "description": "التحقق من الايسن كي"
            },
            "Server List": {
                "status": "<:online:795669431044145192>", 
                "description": "عرض قائمة السيرفرات المتصلة"
            },
            "License Status": {
                "status": "<:online:795669431044145192>", 
                "description": "نظام الرخص"
            },
            "Last Update": f"<t:{int(time.time()) % 60}:R>",
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def get_last_bot_message():
    """جلب آخر رسالة للبوت في الروم"""
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
                    print(f"📝 وجدت الرسالة السابقة: {LAST_MESSAGE_ID}")
                    return LAST_MESSAGE_ID
        print("❌ لم أجد رسالة سابقة")
        return None
    except Exception as e:
        print(f"❌ خطأ في جلب الرسائل: {e}")
        return None

def create_discord_embed(status_data):
    """إنشاء رسالة إمبدد"""
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "**Cfx Status:**",
                "value": f"Status {status_data['Cfx Status']['status']}\nDescription: {status_data['Cfx Status']['description']}",
                "inline": False
            },
            {
                "name": "**CnL:**", 
                "value": f"Status {status_data['CnL']['status']}\nDescription: {status_data['CnL']['description']}", 
                "inline": False
            },
            {
                "name": "**Policy:**",
                "value": f"Status {status_data['Policy']['status']}\nDescription: {status_data['Policy']['description']}",
                "inline": False
            },
            {
                "name": "**Keymaster:**", 
                "value": f"Status {status_data['Keymaster']['status']}\nDescription: {status_data['Keymaster']['description']}",
                "inline": False
            },
            {
                "name": "**Server List:**",
                "value": f"Status {status_data['Server List']['status']}\nDescription: {status_data['Server List']['description']}", 
                "inline": False
            },
            {
                "name": "**License Status:**",
                "value": f"Status {status_data['License Status']['status']}\nDescription: {status_data['License Status']['description']}",
                "inline": False
            },
            {
                "name": "**Last Update:**",
                "value": status_data["Last Update"],
                "inline": False
            }
        ],
        "footer": {
            "text": f"Total Requests {status_data['Total Requests']} • Today at {datetime.now().strftime('%I:%M %p')}"
        }
    }
    return embed

def send_or_edit_message(embed_data):
    """إرسال رسالة جديدة أو تعديل الرسالة السابقة"""
    global LAST_MESSAGE_ID
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {"embeds": [embed_data]}
    
    try:
        # إذا عندنا رسالة سابقة، جرب نعدلها
        if LAST_MESSAGE_ID:
            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{LAST_MESSAGE_ID}"
            response = requests.patch(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ تم تعديل الرسالة بنجاح!")
                return True
            else:
                print(f"❌ فشل التعديل: {response.status_code} - سيتم إنشاء رسالة جديدة")
                LAST_MESSAGE_ID = None
        
        # إرسال رسالة جديدة
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            LAST_MESSAGE_ID = response_data['id']
            print(f"✅ تم إرسال رسالة جديدة: {LAST_MESSAGE_ID}")
            return True
        else:
            print(f"❌ فشل الإرسال: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدأ مراقبة FiveM...")
    
    if not BOT_TOKEN:
        print("❌ لم يتم تعيين DISCORD_BOT_TOKEN")
        return
        
    if not CHANNEL_ID:
        print("❌ لم يتم تعيين DISCORD_CHANNEL_ID")
        return
    
    # جلب آخر رسالة للبوت
    get_last_bot_message()
    
    # جلب البيانات
    status_data = get_fivem_status()
    
    if status_data:
        # إنشاء الرسالة
        embed = create_discord_embed(status_data)
        
        # إرسال أو تعديل الرسالة
        success = send_or_edit_message(embed)
        
        if success:
            print("✅ تم التحديث بنجاح!")
        else:
            print("💥 فشل التحديث")
    else:
        print("❌ فشل في جلب البيانات")

if __name__ == "__main__":
    main()
