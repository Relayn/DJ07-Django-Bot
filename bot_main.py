import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Проверяем, что токен загрузился
if not BOT_TOKEN:
    print("Ошибка: Токен Telegram бота не найден в переменных окружения!")
    print("Убедитесь, что в файле .env или в окружении установлена переменная TELEGRAM_BOT_TOKEN.")
    exit() # Выходим, если токен не установлен

API_URL = "http://127.0.0.1:8000/api/register/" # URL нашего Django API endpoint для регистрации

bot = telebot.TeleBot(BOT_TOKEN) # Создаем экземпляр бота

@bot.message_handler(commands=['start']) # Обработчик команды /start
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else '' # Получаем username, если он есть

    data = { # Собираем данные пользователя для отправки в API
        "user_id": user_id,
        "username": username
    }

    try:
        # Отправляем POST-запрос к Django API
        response = requests.post(API_URL, json=data)

        # --- НАЧАЛО КОДА ОБРАБОТКИ ОТВЕТА ---
        if response.status_code == 201: # Проверяем статус ответа от API. 201 - пользователь создан
            bot.send_message(message.chat.id, "Вы успешно зарегистрированы!") # Отправляем сообщение об успешной регистрации
        elif response.status_code == 200: # 200 - пользователь уже зарегистрирован (по коду API, который мы писали ранее)
             # Если API вернуло {'message': 'User is already registered'} при статусе 200
             if response.json().get('message') == 'User is already registered':
                 bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
             else:
                 # Обработка других возможных успешных ответов со статусом 200, если они есть
                 bot.send_message(message.chat.id, "Получен успешный ответ, но статус не 201.")
                 print(f"Неожиданный успешный ответ от API (status 200): {response.json()}")

        else:
            # Обрабатываем другие возможные ошибки, например 400 Bad Request, 500 Internal Server Error
            bot.send_message(message.chat.id, f"Произошла ошибка при регистрации. Код статуса: {response.status_code}")
            print(f"Ошибка API (status {response.status_code}): {response.text}") # Для отладки

        # --- КОНЕЦ КОДА ОБРАБОТКИ ОТВЕТА ---

    except requests.exceptions.RequestException as e:
        # Обрабатываем ошибки при отправке запроса (например, если Django сервер не запущен или проблемы с сетью)
        bot.send_message(message.chat.id, "Не удалось связаться с сервером регистрации. Убедитесь, что сервер запущен.")
        print(f"Ошибка запроса к API: {e}") # Для отладки


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True) # Запускаем бесконечный цикл получения обновлений от Telegram