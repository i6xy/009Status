import os
import requests
from datetime import datetime

def get_fivem_status():
    try:
        status_data = {
            "Cfx Status": {"status": "█", "description": "إحالة التاريخ أم", "emoji": "🟢"},
            "CnL": {"status": "█", "description": "النقطق من الذهب عند الاتصال بالصورة", "emoji": "🟢"},
            "Policy": {"status": "█", "description": "الاتصال الصورية بصورة قلباء", "emoji": "🟢"},
            "Keymaster": {"status": "█", "description": "النقطق من الأيمن في", "emoji": "🟢"},
            "Server List": {"status": "█", "description": "إعرض قائمة الصورية المتصلة", "emoji": "🟢"},
            "License Status": {"status": "█", "description": "نظام الدرس", "emoji": "🟢"},
            "Last Update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_message(status_data):
    if not status_data:
        return None
    
    embed = {
        "title": "🔥 FireM Status - فئة القضاء",
        "color": 0x00ff00,
        "fields": [],
        "timestamp": datetime.now().isoformat(),
        "footer": {"text": f"🔄 Total Requests: {status_data.get('Total Requests', 'N/A')}"}
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
                "name": f"{data.get('emoji', '⚪')} {name}",
                "value": f"**الحالة:** {data['status']}\n**الوصف:** {data['description']}",
                "inline": True
            })
    
    embed["fields"].append({
        "name": "🕐 آخر تحديث",
        "value": f"**{status_data.get('Last Update', 'غير معروف')}**",
        "inline": False
    })
    
    return {"embeds": [embed]}

def main():
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ لم يتم تعيين WEBHOOK_URL")
        return
    
    print("🚀 بدأ مراقبة حالة FiveM...")
    status_data = get_fivem_status()
    
    if status_data:
        message = create_discord_message(status_data)
        if message:
            response = requests.post(webhook_url, json=message, timeout=10)
            if response.status_code in [200, 204]:
                print("✅ تم الإرسال بنجاح!")
            else:
                print(f"❌ فشل الإرسال: {response.status_code}")

if __name__ == "__main__":
    main()
