import logging
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler,
    ContextTypes
)

from tg_bot.keyboards import (
    get_main_keyboard,
    get_temperature_keyboard,
    get_humidity_keyboard,
    get_ventilation_keyboard,
    get_settings_keyboard,
    get_confirm_keyboard
)

from tg_bot.config import Config
from database.db_crud import db
from arduino.serial_speaker import arduino
from logic.inc_control import controller

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные для состояний
user_states = {}

# ============ КОМАНДЫ ============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    from tg_bot.keyboards import get_main_keyboard
    user = update.effective_user
    
    # Регистрируем пользователя
    db_user = db.create_user(
        telegram_id=user.id,
        first_name=user.first_name,
        username=user.username
    )
    
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n"
        f"🤖 Я бот для управления инкубатором\n\n"
        f"📋 Используйте кнопки ниже или команды:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "📖 Помощь по командам:\n\n"
        "Основные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/status - Статус инкубатора\n\n"
        
        "Управление:\n"
        "/set_temp 37.5 - Установить температуру\n"
        "/set_hum 55 - Установить влажность\n"
        "/start_inc - Запустить инкубатор\n"
        "/stop_inc - Остановить инкубатор\n"
        "/vent - Проветривание\n"
        "/turn - Поворот яиц\n"
        "/history - История данных\n"
        "/settings - Настройки\n\n"
        
        "Или используйте кнопки меню 👇"
    )
    
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить статус инкубатора"""
    from tg_bot.keyboards import get_main_keyboard
    try:
        # Получаем состояние из БД
        state = db.get_state()
        
        # Получаем последние данные с датчиков
        latest_data = db.get_latest_sensor_data(limit=1)
        
        if latest_data:
            last_data = latest_data[0]
            temp = f"{last_data.temperature:.1f}"
            hum = f"{last_data.humidity:.0f}"
            time_str = last_data.timestamp.strftime("%H:%M:%S")
        else:
            temp = hum = "Н/Д"
            time_str = "Нет данных"
        
        # Получаем статус Arduino
        arduino_status = "✅ Подключена" if arduino.is_connected else "❌ Отключена"
        
        # Формируем сообщение
        status_text = (
            "📊 СТАТУС ИНКУБАТОРА\n\n"
            f"🔌 Arduino: {arduino_status}\n"
            f"📈 Состояние: {'🚀 Запущен' if state.is_running else '🛑 Остановлен'}\n\n"
            f"🌡️ Текущая температура: {temp}°C\n"
            f"🎯 Целевая температура: {state.target_temp}°C\n\n"
            f"💧 Текущая влажность: {hum}%\n"
            f"🎯 Целевая влажность: {state.target_hum}%\n\n"
            f"🕐 Последние данные: {time_str}"
        )
        
        await update.message.reply_text(
            status_text,
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Ошибка в status_command: {e}")
        await update.message.reply_text(
            "❌ Ошибка получения статуса",
            reply_markup=get_main_keyboard()
        )

async def set_temperature_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установить температуру"""
    from tg_bot.keyboards import get_temperature_keyboard
    user_id = update.effective_user.id
    
    # Если передано значение в команде
    if context.args:
        try:
            temp = float(context.args[0])
            if 35.0 <= temp <= 40.0:
                controller.set_temperature(temp)
                db.add_command(user_id, "set_temp", temp)
                
                await update.message.reply_text(
                    f"✅ Температура установлена: {temp}°C",
                    reply_markup=get_main_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Температура должна быть от 35.0 до 40.0°C",
                    reply_markup=get_main_keyboard()
                )
        except ValueError:
            await update.message.reply_text(
                "❌ Неверный формат температуры. Пример: /set_temp 37.5",
                reply_markup=get_main_keyboard()
            )
    else:
        await update.message.reply_text(
            "🌡️ Выберите температуру:",
            reply_markup=get_temperature_keyboard()
        )
        user_states[user_id] = 'waiting_for_temp'

async def set_humidity_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установить влажность"""
    from tg_bot.keyboards import get_humidity_keyboard
    user_id = update.effective_user.id
    
    if context.args:
        try:
            hum = float(context.args[0])
            if 40.0 <= hum <= 80.0:
                controller.set_humidity(hum)
                db.add_command(user_id, "set_hum", hum)
                
                await update.message.reply_text(
                    f"✅ Влажность установлена: {hum}%",
                    reply_markup=get_main_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Влажность должна быть от 40.0 до 80.0%",
                    reply_markup=get_main_keyboard()
                )
        except ValueError:
            await update.message.reply_text(
                "❌ Неверный формат влажности. Пример: /set_hum 55.0",
                reply_markup=get_main_keyboard()
            )
    else:
        await update.message.reply_text(
            "💧 Выберите влажность:",
            reply_markup=get_humidity_keyboard()
        )
        user_states[user_id] = 'waiting_for_hum'

async def start_incubator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запустить инкубатор"""
    from tg_bot.keyboards import get_main_keyboard
    user_id = update.effective_user.id
    
    if controller.start():
        db.add_command(user_id, "start_inc", None)
        await update.message.reply_text(
            "✅ Инкубатор запущен!",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Инкубатор уже запущен",
            reply_markup=get_main_keyboard()
        )

async def stop_incubator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановить инкубатор"""
    from tg_bot.keyboards import get_main_keyboard
    user_id = update.effective_user.id
    
    if controller.stop():
        db.add_command(user_id, "stop_inc", None)
        await update.message.reply_text(
            "✅ Инкубатор остановлен!",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Инкубатор уже остановлен",
            reply_markup=get_main_keyboard()
        )

async def ventilation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проветривание"""
    from tg_bot.keyboards import get_ventilation_keyboard
    await update.message.reply_text(
        "🌀 Управление проветриванием:",
        reply_markup=get_ventilation_keyboard()
    )

async def egg_turning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поворот яиц"""
    from tg_bot.keyboards import get_main_keyboard
    await update.message.reply_text(
        "🥚 Управление поворотом яиц:",
        reply_markup=get_main_keyboard()
    )

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """История данных"""
    from tg_bot.keyboards import get_main_keyboard
    try:
        # Получаем данные за последние 24 часа
        data_list = db.get_sensor_data_since(hours=24)
        
        if not data_list:
            await update.message.reply_text(
                "📊 История данных пуста\n"
                "Данные появятся после запуска инкубатора",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Формируем сообщение
        text = "📊 История данных (последние 24 часа):\n\n"
        
        # Показываем последние 10 записей
        for i, record in enumerate(data_list[-10:], 1):
            time_str = record.timestamp.strftime("%H:%M")
            text += f"{i}. {time_str} - {record.temperature:.1f}°C, {record.humidity:.0f}%\n"
        
        # Добавляем статистику
        if len(data_list) > 1:
            temps = [r.temperature for r in data_list]
            hums = [r.humidity for r in data_list]
            avg_temp = sum(temps) / len(temps)
            avg_hum = sum(hums) / len(hums)
            
            text += f"\n📈 Средние значения:\n"
            text += f"🌡️ Температура: {avg_temp:.1f}°C\n"
            text += f"💧 Влажность: {avg_hum:.0f}%\n"
        
        text += f"\n📋 Всего записей: {len(data_list)}"
        
        await update.message.reply_text(
            text,
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Ошибка в history_command: {e}")
        await update.message.reply_text(
            "❌ Ошибка получения истории",
            reply_markup=get_main_keyboard()
        )

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройки"""
    from tg_bot.keyboards import get_settings_keyboard
    
    state = db.get_state()
    text = (
        "⚙️ Настройки системы:\n\n"
        f"🔧 Arduino: {'✅ Подключена' if arduino.is_connected else '❌ Отключена'}\n"
        f"🌡️ Целевая температура: {state.target_temp}°C\n"
        f"💧 Целевая влажность: {state.target_hum}%\n\n"
        "Используйте кнопки ниже:"
    )
    
    await update.message.reply_text(
        text,
        reply_markup=get_settings_keyboard()
    )

async def connect_arduino_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подключить Arduino"""
    from tg_bot.keyboards import get_main_keyboard
    user_id = update.effective_user.id
    
    port = context.args[0] if context.args else Config.ARDUINO_PORT
    
    if arduino.connect(port):
        db.add_command(user_id, "connect_arduino", port)
        await update.message.reply_text(
            f"✅ Arduino подключена на порту {port}",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            f"❌ Не удалось подключиться к Arduino на порту {port}",
            reply_markup=get_main_keyboard()
        )

# ============ ОБРАБОТЧИКИ КНОПОК ============

async def start_ventilation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запустить проветривание"""
    from tg_bot.keyboards import get_main_keyboard
    
    if arduino.is_connected:
        response = arduino.send_and_read("VENT:1")
        if response == "OK":
            await update.message.reply_text(
                "🌀 Проветривание включено на 5 минут",
                reply_markup=get_main_keyboard()
            )
            
            # Автоматическое выключение через 5 минут
            import threading
            def auto_off():
                import time
                time.sleep(300)  # 5 минут
                if arduino.is_connected:
                    arduino.send_and_read("VENT:0")
            
            threading.Thread(target=auto_off, daemon=True).start()
        else:
            await update.message.reply_text(
                "❌ Ошибка включения проветривания",
                reply_markup=get_main_keyboard()
            )
    else:
        await update.message.reply_text(
            "❌ Arduino не подключена",
            reply_markup=get_main_keyboard()
        )

async def start_egg_turning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запустить поворот яиц"""
    from tg_bot.keyboards import get_main_keyboard
    
    if arduino.is_connected:
        response = arduino.send_and_read("TURNER:1")
        if response == "OK":
            await update.message.reply_text(
                "🥚 Поворот яиц включен на 30 секунд",
                reply_markup=get_main_keyboard()
            )
            
            # Автоматическое выключение через 30 секунд
            import threading
            def auto_off():
                import time
                time.sleep(30)
                if arduino.is_connected:
                    arduino.send_and_read("TURNER:0")
            
            threading.Thread(target=auto_off, daemon=True).start()
        else:
            await update.message.reply_text(
                "❌ Ошибка включения поворота",
                reply_markup=get_main_keyboard()
            )
    else:
        await update.message.reply_text(
            "❌ Arduino не подключена",
            reply_markup=get_main_keyboard()
        )

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистить историю"""
    from tg_bot.keyboards import get_settings_keyboard
    from database.db_models import SensorData
    from database.database import db as database
    
    try:
        database.connect()
        count = SensorData.delete().execute()
        database.close()
        
        await update.message.reply_text(
            f"✅ История очищена. Удалено записей: {count}",
            reply_markup=get_settings_keyboard()
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка очистки: {e}",
            reply_markup=get_settings_keyboard()
        )

async def disconnect_arduino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отключить Arduino"""
    from tg_bot.keyboards import get_settings_keyboard
    
    if arduino.is_connected:
        arduino.disconnect()
        await update.message.reply_text(
            "✅ Arduino отключена",
            reply_markup=get_settings_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Arduino уже отключена",
            reply_markup=get_settings_keyboard()
        )

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику"""
    from tg_bot.keyboards import get_settings_keyboard
    
    try:
        # Получаем все данные
        data_list = db.get_sensor_data_since(hours=24)
        
        if not data_list:
            await update.message.reply_text(
                "📊 Нет данных для статистики",
                reply_markup=get_settings_keyboard()
            )
            return
        
        temps = [r.temperature for r in data_list]
        hums = [r.humidity for r in data_list]
        
        text = (
            "📊 Статистика за 24 часа:\n\n"
            f"📈 Всего записей: {len(data_list)}\n"
            f"🌡️ Средняя температура: {sum(temps)/len(temps):.1f}°C\n"
            f"📉 Минимальная температура: {min(temps):.1f}°C\n"
            f"📈 Максимальная температура: {max(temps):.1f}°C\n\n"
            f"💧 Средняя влажность: {sum(hums)/len(hums):.0f}%\n"
            f"📉 Минимальная влажность: {min(hums):.0f}%\n"
            f"📈 Максимальная влажность: {max(hums):.0f}%"
        )
        
        await update.message.reply_text(
            text,
            reply_markup=get_settings_keyboard()
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка статистики: {e}",
            reply_markup=get_settings_keyboard()
        )

# ============ ОБРАБОТЧИК СООБЩЕНИЙ ============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    from tg_bot.keyboards import (
        get_main_keyboard, get_temperature_keyboard, 
        get_humidity_keyboard, get_settings_keyboard,
        get_ventilation_keyboard
    )
    
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Проверяем состояние пользователя
    user_state = user_states.get(user_id)
    
    # Обработка ввода температуры
    if user_state == 'waiting_for_temp':
        if message_text == "↩️ Назад":
            user_states.pop(user_id, None)
            await update.message.reply_text(
                "Главное меню:",
                reply_markup=get_main_keyboard()
            )
        else:
            try:
                # Убираем °C если есть
                temp_text = message_text.replace('°C', '').strip()
                temp = float(temp_text)
                
                if 35.0 <= temp <= 40.0:
                    controller.set_temperature(temp)
                    db.add_command(user_id, "set_temp", temp)
                    
                    await update.message.reply_text(
                        f"✅ Температура установлена: {temp}°C",
                        reply_markup=get_main_keyboard()
                    )
                    user_states.pop(user_id, None)
                else:
                    await update.message.reply_text(
                        "❌ Температура должна быть от 35.0 до 40.0°C\nПопробуйте еще раз:",
                        reply_markup=get_temperature_keyboard()
                    )
            except ValueError:
                await update.message.reply_text(
                    "❌ Неверный формат. Введите число, например: 37.5",
                    reply_markup=get_temperature_keyboard()
                )
    
    # Обработка ввода влажности
    elif user_state == 'waiting_for_hum':
        if message_text == "↩️ Назад":
            user_states.pop(user_id, None)
            await update.message.reply_text(
                "Главное меню:",
                reply_markup=get_main_keyboard()
            )
        else:
            try:
                # Убираем % если есть
                hum_text = message_text.replace('%', '').strip()
                hum = float(hum_text)
                
                if 40.0 <= hum <= 80.0:
                    controller.set_humidity(hum)
                    db.add_command(user_id, "set_hum", hum)
                    
                    await update.message.reply_text(
                        f"✅ Влажность установлена: {hum}%",
                        reply_markup=get_main_keyboard()
                    )
                    user_states.pop(user_id, None)
                else:
                    await update.message.reply_text(
                        "❌ Влажность должна быть от 40.0 до 80.0%\nПопробуйте еще раз:",
                        reply_markup=get_humidity_keyboard()
                    )
            except ValueError:
                await update.message.reply_text(
                    "❌ Неверный формат. Введите число, например: 55.0",
                    reply_markup=get_humidity_keyboard()
                )
    
    else:
        # Обработка кнопок главного меню
        if message_text == "📊 Статус инкубатора":
            await status_command(update, context)
        
        elif message_text == "🌡️ Установить температуру":
            await update.message.reply_text(
                "🌡️ Выберите температуру:",
                reply_markup=get_temperature_keyboard()
            )
            user_states[user_id] = 'waiting_for_temp'
        
        elif message_text == "💧 Установить влажность":
            await update.message.reply_text(
                "💧 Выберите влажность:",
                reply_markup=get_humidity_keyboard()
            )
            user_states[user_id] = 'waiting_for_hum'
        
        elif message_text == "🌀 Проветривание":
            await ventilation_command(update, context)
        
        elif message_text == "🥚 Поворот яиц":
            await start_egg_turning(update, context)
        
        elif message_text == "🚀 Запустить инкубатор":
            await start_incubator_command(update, context)
        
        elif message_text == "🛑 Остановить инкубатор":
            await stop_incubator_command(update, context)
        
        elif message_text == "📈 История данных":
            await history_command(update, context)
        
        elif message_text == "⚙️ Настройки":
            await settings_command(update, context)
        
        # Обработка кнопок проветривания
        elif message_text == "🌀 Запустить проветривание":
            await start_ventilation(update, context)
        
        elif message_text == "⏱️ Настроить интервал":
            await update.message.reply_text(
                "⏱️ Введите интервал проветривания в часах (например: 2):\n"
                "Или напишите 'отмена' чтобы вернуться"
            )
            user_states[user_id] = 'waiting_for_vent_interval'
        
        # Обработка кнопок настроек
        elif message_text == "🔌 Подключить Arduino":
            await connect_arduino_command(update, context)
        
        elif message_text == "🔓 Отключить Arduino":
            await disconnect_arduino(update, context)
        
        elif message_text == "📊 Статистика":
            await show_statistics(update, context)
        
        elif message_text == "🧹 Очистить историю":
            await clear_history(update, context)
        
        elif message_text == "↩️ Назад":
            await update.message.reply_text(
                "Главное меню:",
                reply_markup=get_main_keyboard()
            )
        
        # Обработка интервала проветривания
        elif user_state == 'waiting_for_vent_interval':
            if message_text.lower() == 'отмена':
                user_states.pop(user_id, None)
                await update.message.reply_text(
                    "Отменено",
                    reply_markup=get_ventilation_keyboard()
                )
            else:
                try:
                    hours = float(message_text)
                    if 0.5 <= hours <= 12:
                        controller.vent_interval = timedelta(hours=hours)
                        await update.message.reply_text(
                            f"✅ Интервал проветривания установлен: {hours} часов",
                            reply_markup=get_ventilation_keyboard()
                        )
                        user_states.pop(user_id, None)
                    else:
                        await update.message.reply_text(
                            "❌ Интервал должен быть от 0.5 до 12 часов\n"
                            "Попробуйте еще раз или напишите 'отмена':"
                        )
                except ValueError:
                    await update.message.reply_text(
                        "❌ Введите число (например: 2)\n"
                        "Или напишите 'отмена' чтобы отменить:"
                    )
        
        else:
            await update.message.reply_text(
                "🤔 Используйте кнопки меню или команды\n"
                "Для справки: /help",
                reply_markup=get_main_keyboard()
            )

# ============ ИНИЦИАЛИЗАЦИЯ БОТА ============

def create_bot_application():
    """Создание приложения бота"""
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("set_temp", set_temperature_command))
    application.add_handler(CommandHandler("set_hum", set_humidity_command))
    application.add_handler(CommandHandler("start_inc", start_incubator_command))
    application.add_handler(CommandHandler("stop_inc", stop_incubator_command))
    application.add_handler(CommandHandler("vent", ventilation_command))
    application.add_handler(CommandHandler("turn", egg_turning_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("connect_arduino", connect_arduino_command))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application