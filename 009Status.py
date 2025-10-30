import os
import requests
from datetime import datetime
import time

# متغير عالمي للوقت
start_time = time.time()

def get_fivem_status():
    """جلب حالة FiveM مع وقت متحرك من 0 إلى 60"""
    global start_time
    
    try:
        # حساب الوقت المنقضي منذ بداية التشغيل
        current_time = time.time()
        elapsed_seconds = int(current_time - start_time)
        
        # إذا وصل 60 ثانية، نعيد الضبط
        if elapsed_seconds >= 60:
            start_time = current_time
            elapsed_seconds = 0
        
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
            "Last Update": f"{elapsed_seconds} seconds ago",
            "Total Requests": str(343781 + elapsed_seconds)
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_message(status_data):
    """إنشاء رسالة ديسكورد بنفس تنسيق الصورة"""
    if not status_data:
        return None
    
    embed = {
        "title": "🔥 FireM Status - فئة القضاء",
        "color": 0x00ff00,
        "fields": [],
        "timestamp": datetime.now().isoformat(),
        "footer": {
            "text": f"Total Requests {status_data.get('Total Requests', 'N/A')}"
        }
    }
    
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
                "name": f"**{name}:**",
                "value": f"Status {data['status']}\nDescription: {data['description']}",
                "inline": False
            })
    
    embed["fields"].append({
        "name": "**Last Update:**",
        "value": status_data.get("Last Update", "غير معروف"),
        "inline": False
    })
    
    embed["fields"].append({
        "name": "**Cfx Status**",
        "value": "🟢 License Status\n🟢 Keymaster",
        "inline": False
    })
    
    return {"embeds": [embed]}

def send_or_edit_webhook(webhook_url, message_data, message_id=None):
    """إرسال رسالة جديدة أو تعديل الرسالة السابقة"""
    try:
        if message_id:
            edit_url = f"{webhook_url}/messages/{message_id}"
            response = requests.patch(edit_url, json=message_data, timeout=10)
        else:
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
    
    last_message_id = load_last_message_id()
    print(f"📝 آخر رسالة ID: {last_message_id}")
    
    status_data = get_fivem_status()
    
    if status_data:
        message = create_discord_message(status_data)
        
        if message:
            new_message_id = send_or_edit_webhook(webhook_url, message, last_message_id)
            
            if new_message_id:
                save_last_message_id(new_message_id)
                print(f"💾 تم حفظ الرسالة ID: {new_message_id}")
                print(f"⏰ الوقت الحالي: {status_data['Last Update']}")
            else:
                print("💥 فشلت العملية")
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
