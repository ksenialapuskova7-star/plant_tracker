import requests
from django.conf import settings


def get_chat_id_by_username(username):
    """
    Получает chat_id пользователя по его Telegram username.
    Для этого пользователь должен написать боту.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get('ok'):
            return None
        
        # Ищем chat_id по username
        for update in data.get('result', []):
            message = update.get('message')
            if message:
                chat = message.get('chat')
                if chat and chat.get('username') == username.replace('@', ''):
                    return str(chat.get('id'))
        
        return None
    except Exception:
        return None


def send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram"""
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        response = requests.post(
            url,
            json={'chat_id': chat_id, 'text': text},
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        return response.status_code == 200
    except Exception:
        return False