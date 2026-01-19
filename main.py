import logging
import time
from tg_bot.config import Config
from database.db_models import create_tables
from arduino.serial_speaker import arduino

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    print("=" * 50)
    print("ЗАПУСК СИСТЕМЫ УПРАВЛЕНИЯ ИНКУБАТОРОМ")
    print("=" * 50)
    
    print("1. Инициализация базы данных...")
    try:
        create_tables()
        print("   ✓ База данных готова")
    except Exception as e:
        print(f"   ✗ Ошибка БД: {e}")
        return
    
    print("\n2. Подключение к Arduino...")
    
    # Пробуем разные подходы подключения
    success = False
    
    # Способ 1: Простое подключение
    print("   Способ 1: Простое подключение...")
    if arduino.connect('COM5'):
        print("   ✓ Arduino подключена (способ 1)")
        success = True
    else:
        print("   ✗ Не удалось (способ 1)")
    
    # Способ 2: Принудительное подключение
    if not success:
        print("   Способ 2: Принудительное подключение...")
        try:
            import serial
            arduino.serial = serial.Serial('COM5', 9600, timeout=1)
            time.sleep(2)
            arduino.port = 'COM5'
            arduino.baudrate = 9600
            arduino.is_connected = True
            print("   ✓ Arduino принудительно подключена (способ 2)")
            success = True
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")
    
    # Способ 3: Ручное подключение
    if not success:
        print("   Способ 3: Ручное подключение...")
        port = input("   Введите порт Arduino (например COM5): ").strip()
        if arduino.connect(port):
            print(f"   ✓ Arduino подключена на {port} (способ 3)")
            success = True
        else:
            print("   ✗ Не удалось подключиться")
    
    if not success:
        print("   ⚠ Arduino не подключена. Работаем в режиме эмуляции.")
        arduino.is_connected = False
    
    print("\n3. Создание Telegram бота...")
    try:
        # Используем простой импорт чтобы избежать проблем с таймаутами
        from telegram.ext import ApplicationBuilder
        
        # Создаем бота с увеличенными таймаутами
        application = ApplicationBuilder() \
            .token(Config.BOT_TOKEN) \
            .connect_timeout(60.0) \
            .read_timeout(60.0) \
            .build()
        
        # Импортируем и добавляем обработчики
        from tg_bot.handlers import start_command, help_command, status_command
        from tg_bot.handlers import set_temperature_command, set_humidity_command
        from tg_bot.handlers import start_incubator_command, stop_incubator_command
        from tg_bot.handlers import connect_arduino_command, handle_message
        from telegram.ext import CommandHandler, MessageHandler, filters
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(CommandHandler("set_temp", set_temperature_command))
        application.add_handler(CommandHandler("set_hum", set_humidity_command))
        application.add_handler(CommandHandler("start_inc", start_incubator_command))
        application.add_handler(CommandHandler("stop_inc", stop_incubator_command))
        application.add_handler(CommandHandler("connect_arduino", connect_arduino_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("   ✓ Бот создан")
    except Exception as e:
        print(f"   ✗ Ошибка создания бота: {e}")
        return
    
    print("\n4. Запуск системы...")
    print("   Перейдите в Telegram и напишите /start")
    print("=" * 50)
    
    try:
        application.run_polling(
            poll_interval=3.0,
            timeout=30.0,
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
    except Exception as e:
        print(f"\n⚠ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()