import os
import requests
from datetime import datetime
import time

# متغيرات التوقيت
last_update_time = time.time()

def get_fivem_status():
    """جلب حالة FiveM مع البيانات الجديدة"""
    global last_update_time
    
    try:
        # حساب الوقت المنقضي منذ آخر تحديث
        current_time = time.time()
        elapsed_seconds = int(current_time - last_update_time)
        last_update_time = current_time
        
        status_data = {
            "Cfx Status": {
                "status": "█", 
                "description": "حالة الفايف ام"
            },
            "CnL": {
                "status": "█", 
                "description": "التحقق من اللاعب عند الاتصال بالسيرفر"
            },
            "Policy": {
                "status": "█", 
                "description": "اتصال السيرفرات بسيرفرات فايف إم"
            },
            "Keymaster": {
                "status": "█", 
                "description": "التحقق من الايسن كي"
            },
            "Server List": {
                "status": "█", 
                "description": "عرض قائمة السيرفرات المتصلة"
            },
            "License Status": {
                "status": "█", 
                "description": "نظام الرخص"
            },
            "Last Update": f"{elapsed_seconds} seconds ago",
            "Total Requests": "343823",
            "Current Time": datetime.now().strftime("Today at %I:%M %p")
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_message(status_data):
    """إنشاء رسالة ديسكورد بنفس تنسيق الصورة"""
    if not status_data:
        return None
    
    # إنشاء الأزرار كما في الصورة
    components = [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "Cfx Status",
                    "style": 3,  # أخضر
                    "custom_id": "cfx_status",
                    "disabled": True  # غير قابل للضغط
                },
                {
                    "type": 2,
                    "label": "License Status",
                    "style": 3,  # أخضر
                    "custom_id": "license_status", 
                    "disabled": True  # غير قابل للضغط
                },
                {
                    "type": 2,
                    "label": "Keymaster",
                    "style": 3,  # أخضر
                    "custom_id": "keymaster",
                    "disabled": True  # غير قابل للضغط
                }
            ]
        }
    ]
    
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "**Cfx Status :**",
                "value": f"Status {status_data['Cfx Status']['status']}\nDescription: {status_data['Cfx Status']['description']}",
                "inline": False
            },
            {
                "name": "**CnL :**", 
                "value": f"Status {status_data['CnL']['status']}\nDescription: {status_data['CnL']['description']}",
                "inline": False
            },
            {
                "name": "**Policy :**",
                "value": f"Status {status_data['Policy']['status']}\nDescription: {status_data['Policy']['description']}",
                "inline": False
            },
            {
                "name": "**Keymaster :**",
                "value": f"Status {status_data['Keymaster']['status']}\nDescription: {status_data['Keymaster']['description']}",
                "inline": False
            },
            {
                "name": "**Server List :**",
                "value": f"Status {status_data['Server List']['status']}\nDescription: {status_data['Server List']['description']}",
                "inline": False
            },
            {
                "name": "**License Status :**", 
                "value": f"Status {status_data['License Status']['status']}\nDescription: {status_data['License Status']['description']}",
                "inline": False
            },
            {
                "name": "**Last Update :**",
                "value": status_data["Last Update"],
                "inline": False
            }
        ],
        "footer": {
            "text": f"Total Requests {status_data['Total Requests']} • {status_data['Current Time']}"
        }
    }
    
    return {
        "embeds": [embed],
        "components": components
    }

def send_or_edit_webhook(webhook_url, message_data, message_id=None):
    """إرسال رسالة جديدة أو تعديل الرسالة السابقة"""
    try:
        if message_id:
            # تعديل الرسالة السابقة
            webhook_parts = webhook_url.split('/')
            webhook_id = webhook_parts[-2]
            webhook_token = webhook_parts[-1]
            
            edit_url = f"https://discord.com/api/v10/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
            response = requests.patch(edit_url, json=message_data, timeout=10)
        else:
            # إرسال رسالة جديدة
            response = requests.post(webhook_url, json=message_data, timeout=10)
        
        if response.status_code in [200, 204]:
            if message_id:
                print("✅ تم تحديث الرسالة بنجاح!")
            else:
                print("✅ تم إرسال الرسالة بنجاح!")
            
            if not message_id and response.status_code == 200:
                response_data = response.json()
                return response_data.get('id')
            return message_id
        else:
            print(f"❌ فشل العملية: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return None

def load_last_message_id():
    """تحميل آخر رسالة ID من ملف"""
    try:
        with open('last_message.txt', 'r') as f:
            return f.read().strip()
    except:
        return None

def save_last_message_id(message_id):
    """حفظ آخر رسالة ID في ملف"""
    try:
        with open('last_message.txt', 'w') as f:
            f.write(str(message_id))
    except Exception as e:
        print(f"❌ خطأ في حفظ الرسالة: {e}")

def main():
    """الدالة الرئيسية"""
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ لم يتم تعيين WEBHOOK_URL")
        return
    
    print("🚀 بدأ مراقبة حالة FiveM...")
    
    # جلب آخر رسالة ID
    last_message_id = load_last_message_id()
    print(f"📝 آخر رسالة ID: {last_message_id}")
    
    # جلب البيانات
    status_data = get_fivem_status()
    
    if status_data:
        # إنشاء الرسالة
        message = create_discord_message(status_data)
        
        if message:
            # إرسال أو تعديل الرسالة
            new_message_id = send_or_edit_webhook(webhook_url, message, last_message_id)
            
            if new_message_id:
                # حفظ الـ message ID الجديد
                save_last_message_id(new_message_id)
                print(f"💾 تم حفظ الرسالة ID: {new_message_id}")
                print(f"🕐 الوقت: {status_data['Last Update']}")
            else:
                print("💥 فشلت العملية - سيتم إنشاء رسالة جديدة في المرة القادمة")
                save_last_message_id(None)
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
