import os
import requests
from datetime import datetime
import json

def get_fivem_status():
    """
    جلب حالة FiveM - هنا تحتاج تعديل الكود حسب مصدر البيانات الفعلي
    """
    try:
        # 🔄 استبدل هذا الجزء بالكود الحقيقي لجلب البيانات
        # هذا مثال للبيانات اللي في الصورة
        status_data = {
            "Cfx Status": {
                "status": "█", 
                "description": "إحالة التاريخ أم",
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "CnL": {
                "status": "█", 
                "description": "النقطق من الذهب عند الاتصال بالصورة",
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "Policy": {
                "status": "█", 
                "description": "الاتصال الصورية بصورة قلباء", 
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "Keymaster": {
                "status": "█", 
                "description": "النقطق من الأيمن في",
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "Server List": {
                "status": "█", 
                "description": "إعرض قائمة الصورية المتصلة",
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "License Status": {
                "status": "█", 
                "description": "نظام الدرس",
                "emoji": "🟢" if "█" in "█" else "🔴"
            },
            "Last Update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ في جلب البيانات: {e}")
        return None

def create_discord_message(status_data):
    """إنشاء رسالة ديسكورد"""
    if not status_data:
        return None
    
    embed = {
        "title": "🔥 FireM Status - فئة القضاء",
        "color": 0x00ff00,
        "thumbnail": {"url": "https://i.imgur.com/7VZ7S6y.png"},
        "fields": [],
        "timestamp": datetime.now().isoformat(),
        "footer": {
            "text": f"🔄 Total Requests: {status_data.get('Total Requests', 'N/A')}"
        }
    }
    
    # إضافة الحقول الرئيسية
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
                "name": f"{data.get('emoji', '⚪')} {name}",
                "value": f"**الحالة:** {data['status']}\n**الوصف:** {data['description']}",
                "inline": True
            })
    
    # إضافة آخر تحديث
    embed["fields"].append({
        "name": "🕐 آخر تحديث",
        "value": f"**{status_data.get('Last Update', 'غير معروف')}**",
        "inline": False
    })
    
    return {"embeds": [embed]}

def send_webhook(webhook_url, message_data):
    """إرسال الويبهوك"""
    try:
        response = requests.post(
            webhook_url,
            json=message_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            print("✅ تم إرسال التحديث بنجاح!")
            return True
        else:
            print(f"❌ فشل الإرسال: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    # الحصول على رابط الويبهوك من Secrets
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ لم يتم تعيين WEBHOOK_URL في Secrets")
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
                print("🎉 تمت العملية بنجاح!")
            else:
                print("💥 فشلت العملية")
        else:
            print("❌ فشل في إنشاء الرسالة")
    else:
        print("❌ فشل في جلب بيانات الحالة")

if __name__ == "__main__":
    main()
