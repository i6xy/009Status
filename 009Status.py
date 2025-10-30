import os
import requests
from datetime import datetime
import random

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')

def main():
    print("🚀 بدأ التشغيل...")
    print(f"البوت: {'✅' if BOT_TOKEN else '❌'}")
    print(f"الروم: {'✅' if CHANNEL_ID else '❌'}")
    
    if not BOT_TOKEN:
        print("❌ لم يتم تعيين التوكن")
        return
        
    if not CHANNEL_ID:
        print("❌ لم يتم تعيين الروم")
        return
    
    # بيانات بسيطة للتجربة
    embed = {
        "title": "🔥 اختبار البوت",
        "description": "هذا اختبار أولي",
        "color": 0x00ff00
    }
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        response = requests.post(url, json={"embeds": [embed]}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ تم إرسال الرسالة بنجاح!")
        else:
            print(f"❌ فشل الإرسال: {response.status_code}")
            print(f"الرد: {response.text}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    main()
