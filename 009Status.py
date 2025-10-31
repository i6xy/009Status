def get_last_bot_message():
    """البحث عن آخر رسالة للبوت في الروم"""
    global LAST_MESSAGE_ID
    try:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=20"
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                # التحقق إذا كانت الرسالة من البوت ولها العنوان المطلوب
                if (msg['author']['bot'] and 
                    msg.get('embeds') and 
                    len(msg['embeds']) > 0 and
                    'FiveM Status' in msg['embeds'][0].get('title', '')):
                    
                    LAST_MESSAGE_ID = msg['id']
                    print(f"📝 وجدت الرسالة السابقة: {LAST_MESSAGE_ID}")
                    return LAST_MESSAGE_ID
        
        print("❌ لم أجد رسالة سابقة للبوت")
        return None
        
    except Exception as e:
        print(f"❌ خطأ في البحث عن الرسالة: {e}")
        return None
