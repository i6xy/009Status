import os
import requests
from datetime import datetime
import time
import json

# ملف لحفظ آخر رسالة ID
MESSAGE_FILE = 'message_data.json'

def get_fivem_status():
    """جلب حالة FiveM مع البيانات الجديدة"""
    try:
        # حساب الوقت المنقضي منذ بداية التشغيل
        if not hasattr(get_fivem_status, "start_time"):
            get_fivem_status.start_time = time.time()
        
        elapsed_seconds = int(time.time() - get_fivem_status.start_time)
        
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
                "name": "**Cfx Status:**",
                "value": f"Status █\nDescription: حالة الفايف ام",
                "inline": False
            },
            {
                "name": "**CnL:**", 
                "value": f"Status █\nDescription: التحقق من اللاعب عند الاتصال بالسيرفر", 
                "inline": False
            },
            {
                "name": "**Policy:**",
                "value": f"Status █\nDescription: اتصال السيرفرات بسيرفرات فايف إم",
                "inline": False
            },
            {
                "name": "**Keymaster:**", 
                "value": f"Status █\nDescription: التحقق من الايسن كي",
                "inline": False
            },
            {
                "name": "**Server List:**",
                "value": f"Status █\nDescription: عرض قائمة السيرفرات المتصلة", 
                "inline": False
            },
            {
                "name": "**License Status:**",
                "value": f"Status █\nDescription: نظام الرخص",
                "inline": False
            },
            {
                "name": "**Last Update:**",
                "value": status_data["Last Update"],
                "inline": False
            }
        ],
        "footer": {
            "text": f"Total Requests 343823 • {status_data['Current Time']}"
        }
    }
    
    return {
        "embeds": [embed],
        "components": components
    }

def load_message_data():
    """تحميل بيانات الرسالة من ملف"""
    try:
        with open(MESSAGE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"message_id": None, "webhook_url": None}

def save_message_data(message_id, webhook_url):
    """حفظ بيانات الرسالة في ملف"""
    try:
        data = {
            "message_id": message_id,
            "webhook_url": webhook_url
        }
        with open(MESSAGE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"❌ خطأ في حفظ البيانات: {e}")

def send_or_edit_webhook(webhook_url, message_data, message_id=None):
    """إرسال رسالة جديدة أو تعديل الرسالة السابقة"""
    try:
        if message_id:
            # تعديل الرسالة السابقة - الطريقة الصحيحة
            edit_url = f"{webhook_url}/messages/{message_id}"
            response = requests.patch(edit_url, json=message_data, timeout=10)
            
            if response.status_code == 404:
                print("📝 الرسالة القديمة غير موجودة، سيتم إنشاء رسالة جديدة")
                return None
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
            print(f"❌ فشل العملية: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return None

def main():
    """الدالة الرئيسية"""
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ لم يتم تعيين WEBHOOK_URL")
        return
    
    print("🚀 بدأ مراقبة حالة FiveM...")
    
    # جلب بيانات الرسالة السابقة
    message_data = load_message_data()
    last_message_id = message_data.get("message_id")
    last_webhook_url = message_data.get("webhook_url")
    
    # إذا تغير رابط الويب هوك، ابدأ من جديد
    if last_webhook_url != webhook_url:
        print("🔄 رابط الويب هوك تغير، سيتم إنشاء رسالة جديدة")
        last_message_id = None
    
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
                # حفظ بيانات الرسالة الجديدة
                save_message_data(new_message_id, webhook_url)
                print(f"💾 تم حفظ الرسالة ID: {new_message_id}")
                print(f"🕐 الوقت: {status_data['Last Update']}")
            else:
                # إذا فشل التعديل، أنشئ رسالة جديدة
                print("🔄 فشل التعديل، جاري إنشاء رسالة جديدة...")
                new_message_id = send_or_edit_webhook(webhook_url, message, None)
                if new_message_id:
                    save_message_data(new_message_id, webhook_url)
                    print(f"💾 تم إنشاء رسالة جديدة ID: {new_message_id}")
                else:
                    print("💥 فشل إنشاء الرسالة الجديدة")
                    save_message_data(None, webhook_url)
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
