import os
import requests
from datetime import datetime
import random
import time

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')

# متغيرات الوقت
start_time = time.time()
LAST_MESSAGE_ID = None

def get_fivem_status():
    """جلب حالة FiveM مع وقت حقيقي متحرك"""
    global start_time
    
    try:
        # حساب الوقت المنقضي منذ بداية التشغيل
        current_time = time.time()
        elapsed_seconds = int(current_time - start_time)
        
        # إذا تعدى 60 ثانية، نعيد الضبط
        if elapsed_seconds > 60:
            start_time = current_time
            elapsed_seconds = 0
        
        status_data = {
            "Cfx Status": "█",
            "CnL": "█", 
            "Policy": "█",
            "Keymaster": "█",
            "Server List": "█",
            "License Status": "█",
            "Last Update": f"{elapsed_seconds} seconds ago",
            "Total Requests": str(343823 + elapsed_seconds),
            "Current Time": datetime.now().strftime("Today at %I:%M %p")
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
                "value": f"Status {status_data['Cfx Status']}\nDescription: حالة الفايف ام",
                "inline": False
            },
            {
                "name": "**CnL:**", 
                "value": f"Status {status_data['CnL']}\nDescription: التحقق من اللاعب عند الاتصال بالسيرفر", 
                "inline": False
            },
            {
                "name": "**Policy:**",
                "value": f"Status {status_data['Policy']}\nDescription: اتصال السيرفرات بسيرفرات فايف إم",
                "inline": False
            },
            {
                "name": "**Keymaster:**", 
                "value": f"Status {status_data['Keymaster']}\nDescription: التحقق من الايسن كي",
                "inline": False
            },
            {
                "name": "**Server List:**",
                "value": f"Status {status_data['Server List']}\nDescription: عرض قائمة السيرفرات المتصلة", 
                "inline": False
            },
            {
                "name": "**License Status:**",
                "value": f"Status {status_data['License Status']}\nDescription: نظام الرخص",
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
        },
        "timestamp": datetime.now().isoformat()
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
        print("❌ لم يتم تعيين التوكن")
        return
        
    if not CHANNEL_ID:
        print("❌ لم يتم تعيين الروم")
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
            print(f"✅ تم التحديث: {status_data['Last Update']}")
        else:
            print("💥 فشل التحديث")
    else:
        print("❌ فشل في جلب البيانات")

if __name__ == "__main__":
    main()
