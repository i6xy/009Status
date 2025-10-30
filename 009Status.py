import os
import requests
from datetime import datetime
import time

# متغير عالمي لحفظ رسالة ID
LAST_MESSAGE_ID = None

def get_fivem_status():
    """جلب حالة FiveM مع البيانات الجديدة"""
    try:
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
            "Last Update": f"{int(time.time() - time.time())} seconds ago",
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_message(status_data):
    """إنشاء رسالة ديسكورد بنفس تنسيق الصورة"""
    if not status_data:
        return None
    
    # حساب الوقت منذ آخر تحديث
    update_time = "0 seconds ago"  # يمكنك تعديل هذا ليعكس الوقت الحقيقي
    
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,  # اللون الأخضر
        "fields": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # إضافة الحقول الرئيسية بشكل عمودي
    components = [
        ("Cfx Status", "Cfx Status"),
        ("CnL", "CnL"),
        ("Policy", "Policy"), 
        ("Keymaster", "Keymaster"),
        ("Server List", "Server List"),
        ("License Status", "License Status")
    ]
    
    for key, name in components:
        if key in status_data:
            data = status_data[key]
            embed["fields"].append({
                "name": f"**{name} :**",
                "value": f"Status {data['status']}\nDescription: {data['description']}",
                "inline": False
            })
    
    # إضافة آخر تحديث
    embed["fields"].append({
        "name": "**Last Update :**",
        "value": update_time,
        "inline": False
    })
    
    # إضافة الأزرار (غير قابلة للضغط) - كحقول عادية
    embed["fields"].append({
        "name": "**Cfx Status**",
        "value": "█ License Status\n█ Keymaster",
        "inline": False
    })
    
    # إضافة الفوتر
    embed["footer"] = {
        "text": "Total Requests 343781 • Today at 12:10 AM"
    }
    
    return {"embeds": [embed]}

def send_or_edit_webhook(webhook_url, message_data, message_id=None):
    """إرسال رسالة جديدة أو تعديل الرسالة السابقة"""
    try:
        if message_id:
            # تعديل الرسالة السابقة
            edit_url = f"https://discord.com/api/webhooks/{webhook_url.split('/')[-2]}/{webhook_url.split('/')[-1]}/messages/{message_id}"
            response = requests.patch(edit_url, json=message_data, timeout=10)
        else:
            # إرسال رسالة جديدة
            response = requests.post(webhook_url, json=message_data, timeout=10)
        
        if response.status_code in [200, 204]:
            if message_id:
                print("✅ تم تحديث الرسالة بنجاح!")
            else:
                print("✅ تم إرسال الرسالة بنجاح!")
            
            # إذا كانت استجابة جديدة، احفظ الـ message ID
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
            else:
                print("💥 فشلت العملية - سيتم إنشاء رسالة جديدة في المرة القادمة")
                # إذا فشل التعديل، احذف الـ ID القديم
                save_last_message_id(None)
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
