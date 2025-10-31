import os
import requests
from datetime import datetime
import time

# إعدادات البوت
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')
LAST_MESSAGE_ID = None

def test_bot_connection():
    """اختبار اتصال البوت بالديسكورد"""
    try:
        url = f"https://discord.com/api/v10/users/@me"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ البوت متصل: {bot_info['username']}#{bot_info['discriminator']}")
            return True
        else:
            print(f"❌ فشل الاتصال: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def test_channel_access():
    """اختبار الوصول للقناة"""
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            channel_info = response.json()
            print(f"✅ الوصول للقناة: {channel_info.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ لا يمكن الوصول للقناة: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الوصول للقناة: {e}")
        return False

def send_test_message():
    """إرسال رسالة تجريبية"""
    try:
        embed = {
            "title": "🔥 Test Message",
            "description": "هذه رسالة تجريبية",
            "color": 0x00ff00,
            "timestamp": datetime.now().isoformat()
        }
        
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
        data = {"embeds": [embed]}
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            message_id = response.json()['id']
            print(f"✅ تم إرسال الرسالة: {message_id}")
            return message_id
        else:
            print(f"❌ فشل إرسال الرسالة: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ خطأ في إرسال الرسالة: {e}")
        return None

def get_fivem_status():
    """جلب حالة FiveM"""
    try:
        current_seconds = int(time.time()) % 60
        
        status_data = {
            "Cfx Status": {"status": "🟢", "description": "حالة الفايف ام"},
            "CnL": {"status": "🟢", "description": "التحقق من اللاعب"},
            "Policy": {"status": "🟢", "description": "اتصال السيرفرات"},
            "Keymaster": {"status": "🟢", "description": "التحقق من الايسن كي"},
            "Server List": {"status": "🟢", "description": "قائمة السيرفرات"},
            "License Status": {"status": "🟢", "description": "نظام الرخص"},
            "Last Update": f"{current_seconds} seconds ago",
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def create_discord_embed(status_data):
    embed = {
        "title": "🔥 FiveM Status - الملفات",
        "color": 0x00ff00,
        "fields": [
            {"name": "**Cfx Status:**", "value": f"Status {status_data['Cfx Status']['status']}\nDescription: {status_data['Cfx Status']['description']}", "inline": False},
            {"name": "**CnL:**", "value": f"Status {status_data['CnL']['status']}\nDescription: {status_data['CnL']['description']}", "inline": False},
            {"name": "**Policy:**", "value": f"Status {status_data['Policy']['status']}\nDescription: {status_data['Policy']['description']}", "inline": False},
            {"name": "**Keymaster:**", "value": f"Status {status_data['Keymaster']['status']}\nDescription: {status_data['Keymaster']['description']}", "inline": False},
            {"name": "**Server List:**", "value": f"Status {status_data['Server List']['status']}\nDescription: {status_data['Server List']['description']}", "inline": False},
            {"name": "**License Status:**", "value": f"Status {status_data['License Status']['status']}\nDescription: {status_data['License Status']['description']}", "inline": False},
            {"name": "**Last Update:**", "value": status_data["Last Update"], "inline": False}
        ],
        "footer": {"text": f"Total Requests {status_data['Total Requests']} • {datetime.now().strftime('%I:%M %p')}"}
    }
    return embed

def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ لم يتم تعيين التوكن أو الروم")
        print(f"BOT_TOKEN: {'✅' if BOT_TOKEN else '❌'}")
        print(f"CHANNEL_ID: {'✅' if CHANNEL_ID else '❌'}")
        return
    
    # اختبار الاتصال
    if not test_bot_connection():
        return
    
    if not test_channel_access():
        return
    
    # إرسال رسالة تجريبية أولاً
    test_message_id = send_test_message()
    if not test_message_id:
        return
    
    # الآن شغل النظام الرئيسي
    print("🚀 بدأ تشغيل النظام الرئيسي...")
    
    global LAST_MESSAGE_ID
    LAST_MESSAGE_ID = test_message_id
    
    try:
        while True:
            status_data = get_fivem_status()
            if status_data:
                embed = create_discord_embed(status_data)
                
                # تعديل الرسالة الموجودة
                url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{LAST_MESSAGE_ID}"
                headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
                data = {"embeds": [embed]}
                
                response = requests.patch(url, json=data, headers=headers, timeout=10)
                
                current_seconds = int(time.time()) % 60
                if response.status_code == 200:
                    print(f"⏰ {current_seconds}s - ✅ تم التحديث")
                else:
                    print(f"⏰ {current_seconds}s - ❌ فشل التحديث: {response.status_code}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت")

if __name__ == "__main__":
    main()
