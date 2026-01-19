# test_sensor_chain.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from arduino.serial_speaker import arduino
from database.db_crud import db
from logic.inc_control import controller
import time

print("Тест цепочки данных:")
print("=" * 60)

# 1. Подключение Arduino
print("1. Подключение Arduino...")
if arduino.connect('COM5'):
    print("   ✓ Arduino подключена")
else:
    print("   ✗ Arduino не подключена")
    arduino.is_connected = True  # Принудительно

# 2. Чтение данных напрямую
print("\n2. Прямой запрос к Arduino...")
response = arduino.send_and_read("GET_DATA")
print(f"   Ответ на GET_DATA: '{response}'")

# 3. Тест контроллера
print("\n3. Тест контроллера...")
data = controller._get_sensor_data()  # Прямой вызов метода
print(f"   Данные от контроллера: {data}")

# 4. Проверка БД
print("\n4. Проверка базы данных...")
latest = db.get_latest_sensor_data(limit=3)
print(f"   Последние записи в БД: {len(latest)}")
for i, record in enumerate(latest):
    print(f"   {i+1}. {record.timestamp}: {record.temperature}°C, {record.humidity}%")

# 5. Тест статуса инкубатора
print("\n5. Тест статуса инкубатора...")
state = db.get_state()
print(f"   Состояние инкубатора: {'Запущен' if state.is_running else 'Остановлен'}")
print(f"   Целевая температура: {state.target_temp}°C")
print(f"   Целевая влажность: {state.target_hum}%")

# 6. Запускаем контроллер
print("\n6. Запуск контроллера на 20 секунд...")
controller.start()
time.sleep(20)
controller.stop()

# 7. Снова проверяем БД
print("\n7. Проверка БД после работы контроллера...")
latest = db.get_latest_sensor_data(limit=5)
print(f"   Записей после работы: {len(latest)}")
for i, record in enumerate(latest):
    print(f"   {i+1}. {record.timestamp}: {record.temperature}°C, {record.humidity}%")

print("\n" + "=" * 60)
input("Нажмите Enter...")