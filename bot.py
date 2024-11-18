from telegram import Update
from telegram.ext import Application, CommandHandler
import requests

# Твой API-ключ от TimeZoneDB
API_KEY = "CW5JTGTDKUT1"

# Функция для получения времени через TimeZoneDB
def get_time(city):
    try:
        # Отправляем запрос к API TimeZoneDB
        response = requests.get(
            "http://api.timezonedb.com/v2.1/get-time-zone",
            params={
                "key": API_KEY,
                "format": "json",
                "by": "zone",
                "zone": city
            }
        )
        data = response.json()

        # Проверяем статус ответа
        if data.get("status") == "OK":
            time = data.get("formatted", "No time found").split(" ")[1]
            return f"{city} time: {time}"
        else:
            return f"Ошибка: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Не удалось получить время. Ошибка: {str(e)}"

# Обработчик команды /time
async def time(update: Update, context):
    if len(context.args) > 0:
        city = context.args[0]
        result = get_time(city)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Пожалуйста, укажите город. Пример: /time Europe/Moscow")

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = Application.builder().token("7701961002:AAE_2hEapTc8mu3X8pnxPzQN2QtftXc61p8").build()

    # Добавляем обработчик команды /time
    application.add_handler(CommandHandler("time", time))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
