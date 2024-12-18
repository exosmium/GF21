# Button labels
BUTTON_CHECK_STATUS = "📍 Проверить статус"
BUTTON_UPDATE_LOCATION = "🔄 Обновить местоположение"

# Command descriptions 
CMD_START = "Запустить бота"
CMD_HELP = "Показать справку"

# Welcome message
WELCOME_MESSAGE = "👋 Добро пожаловать в GPS трекер!\n\nИспользуйте кнопки ниже для управления:"

# Help message
HELP_MESSAGE = """📖 **Справка по командам**

• /start - Запустить бота и показать меню
• /help - Показать это сообщение

Используйте кнопки в меню для:
• 📍 Проверить статус - получить текущие данные о местоположении
• 🔄 Обновить местоположение - запросить обновление GPS данных"""

# Status update messages
PROCESSING_UPDATE = "🔄 Отправка запроса на обновление местоположения..."
UPDATE_SUCCESS = """✅ Запрос на обновление местоположения отправлен успешно!

Нажмите кнопку «Проверить статус» через несколько секунд, чтобы увидеть обновленную информацию."""
UPDATE_FAILED = "❌ Не удалось отправить запрос на обновление.\nПожалуйста, попробуйте еще раз позже."
UPDATE_ERROR = "❌ Произошла ошибка при отправке запроса на обновление."

# Status check messages
GETTING_STATUS = "🔄 Получение текущих данных..."
STATUS_FAILED = "❌ Не удалось получить данные. Попробуйте позже."
STATUS_ERROR = "❌ Произошла ошибка при получении статуса."

# Vehicle status template
STATUS_TEMPLATE = """🚗 **{name}**

📍 **Местоположение**
- Последнее обновление: {update_time}
- Время до дома: {travel_time}

📊 **Состояние**
- Скорость: {speed} км/ч
- Заряд батареи: {battery}%"""

# Vehicle status strings
STATUS_UNKNOWN = "Неизвестно"
STATUS_STATIC = "Автомобиль стоит на месте {} минут"

# Time units for formatting
MINUTE_1 = "минута"
MINUTE_2_4 = "минуты"
MINUTE_5_20 = "минут"
HOUR_1 = "час"
HOUR_2_4 = "часа"
HOUR_5_20 = "часов"