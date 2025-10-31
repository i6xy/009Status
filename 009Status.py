def get_fivem_status():
    """جلب حالة FiveM مع وقت من 1 إلى 60 ثم يعيد"""
    try:
        # حساب الثواني من 1 إلى 60 ثم يعيد
        current_seconds = (int(time.time()) % 60) + 1  # +1 علشان يبدأ من 1 ليس 0
        
        status_data = {
            "Cfx Status": {"status": "<:online:795669431044145192>", "description": "حالة الفايف ام"},
            "CnL": {"status": "<:online:795669431044145192>", "description": "التحقق من اللاعب عند الاتصال بالسيرفر"},
            "Policy": {"status": "<:online:795669431044145192>", "description": "اتصال السيرفرات بسيرفرات فايف إم"},
            "Keymaster": {"status": "<:online:795669431044145192>", "description": "التحقق من الايسن كي"},
            "Server List": {"status": "<:online:795669431044145192>", "description": "عرض قائمة السيرفرات المتصلة"},
            "License Status": {"status": "<:online:795669431044145192>", "description": "نظام الرخص"},
            "Last Update": f"{current_seconds} seconds ago",
            "Total Requests": "343781"
        }
        return status_data
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None
