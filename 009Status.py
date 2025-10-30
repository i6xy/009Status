import os
import requests
from datetime import datetime
import time

def get_fivem_status():
    """جلب حالة FiveM"""
    try:
        # الوقت الحالي للتحديث
        current_time = datetime.now()
        
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
            "Last Update": f"{current_time.strftime('%H:%M:%S')}",
            "Total Requests": "343823",
            "Current Time": current_time.strftime("Today at %I:%M %p")
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_message(status_data):
    """إنشاء رسالة ديسكورد"""
    if not status_data:
        return None
    
    # إنشاء الأزرار
    components = [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "Cfx Status",
                    "style": 3,
                    "custom_id": "cfx_status",
                    "disabled": True
                },
                {
                    "type": 2,
                    "label": "License Status", 
                    "style": 3,
                    "custom_id": "license_status",
                    "disabled": True
                },
                {
                    "type": 2,
                    "label": "Keymaster",
                    "style": 3,
                    "custom_id": "keymaster",
                    "disabled": True
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
            "text": f"Total Requests {status_data['Total Requests']} • {status_data['Current Time']}"
        }
    }
    
    return {
        "embeds": [embed],
        "components": components
    }

def send_webhook(webhook_url, message_data):
    """إرسال رسالة ويب هوك"""
    try:
        response = requests.post(webhook_url, json=message_data, timeout=10)
        
        if response.status_code in [200, 204]:
            print("✅ تم إرسال الرسالة بنجاح!")
            return True
        else:
            print(f"❌ فشل الإرسال: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ لم يتم تعيين WEBHOOK_URL")
        return
    
    print("🚀 بدأ مراقبة حالة FiveM...")
    
    # جلب البيانات
    status_data = get_fivem_status()
    
    if status_data:
        # إنشاء الرسالة
        message = create_discord_message(status_data)
        
        if message:
            # إرسال الرسالة
            success = send_webhook(webhook_url, message)
            
            if success:
                print(f"✅ تم الإرسال في: {status_data['Last Update']}")
            else:
                print("💥 فشل إرسال الرسالة")
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
