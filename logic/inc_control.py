import time
import threading
from datetime import datetime, timedelta
from database.db_crud import db
from arduino.serial_speaker import arduino

class IncubatorController:
    """Контроллер инкубатора"""
    
    def __init__(self):
        self.is_running = False
        self.target_temp = 37.5
        self.target_hum = 55.0
        
        # Настройки проветривания
        self.vent_enabled = True
        self.vent_interval = timedelta(hours=1)
        self.vent_duration = timedelta(minutes=5)
        
        # Время последних действий
        self.last_vent_time = None
        self.last_turn_time = None
        
        # Поток для автоматического управления
        self.control_thread = None
        self.stop_event = threading.Event()
    
    def start(self):
        """Запустить инкубатор"""
        if self.is_running:
            return False
        
        # Считываем настройки из БД
        state = db.get_state()
        self.target_temp = state.target_temp
        self.target_hum = state.target_hum
        
        # Обновляем статус в БД
        db.start_incubator()
        
        # Запускаем поток управления
        self.is_running = True
        self.stop_event.clear()
        self.control_thread = threading.Thread(target=self._control_loop, daemon=True)
        self.control_thread.start()
        
        # Сбрасываем таймеры
        self.last_vent_time = datetime.now()
        self.last_turn_time = datetime.now()
        
        print("✅ Инкубатор запущен")
        return True
    
    def stop(self):
        """Остановить инкубатор"""
        if not self.is_running:
            return False
        
        self.is_running = False
        self.stop_event.set()
        
        # Выключаем все устройства на Arduino
        if arduino.is_connected:
            arduino.send_and_read("ALL_OFF")
        
        # Обновляем статус в БД
        db.stop_incubator()
        
        print("✅ Инкубатор остановлен")
        return True
    
    def set_temperature(self, temp):
        """Установить целевую температуру"""
        self.target_temp = temp
        db.set_temperature(temp)
        print(f"✅ Целевая температура: {temp}°C")
    
    def set_humidity(self, hum):
        """Установить целевую влажность"""
        self.target_hum = hum
        db.set_humidity(hum)
        print(f"✅ Целевая влажность: {hum}%")
    
    def _control_loop(self):
        """Основной цикл управления"""
        while not self.stop_event.is_set() and self.is_running:
            try:
                # 1. Получаем данные с датчиков
                sensor_data = self._get_sensor_data()
                if sensor_data:
                    temp, hum = sensor_data
                    
                    # 2. Управляем температурой
                    self._control_temperature(temp)
                    
                    # 3. Управляем влажностью
                    self._control_humidity(hum)
                
                # 4. Проверяем проветривание
                self._check_ventilation()
                
                # 5. Проверяем поворот яиц
                self._check_egg_turning()
                
                # Пауза между циклами
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Ошибка в control_loop: {e}")
                time.sleep(10)
    
    def _get_sensor_data(self):
        """Получить данные с датчиков"""
        if not arduino.is_connected:
            return None
        
        # Используем send_and_read вместо get_data
        response = arduino.send_and_read("GET_DATA")
        
        if response and "," in response:
            try:
                parts = response.split(",")
                temp = float(parts[0].strip())
                hum = float(parts[1].strip())
                
                # Сохраняем в БД
                db.add_sensor_data(temp, hum)
                return temp, hum
            except Exception as e:
                print(f"Ошибка разбора данных: {e}")
                return None
        
        return None
    
    def _control_temperature(self, current_temp):
        """Управление температурой"""
        if not arduino.is_connected:
            return
        
        # Включаем нагреватель, если температура ниже целевой
        if current_temp < self.target_temp - 0.5:
            arduino.send_and_read("HEATER:1")
        elif current_temp > self.target_temp + 0.5:
            arduino.send_and_read("HEATER:0")
    
    def _control_humidity(self, current_hum):
        """Управление влажностью"""
        if not arduino.is_connected:
            return
        
        # Включаем увлажнитель, если влажность ниже целевой
        if current_hum < self.target_hum - 5.0:
            arduino.send_and_read("HUMIDIFIER:1")
        elif current_hum > self.target_hum + 5.0:
            arduino.send_and_read("HUMIDIFIER:0")
    
    def _check_ventilation(self):
        """Проверка и управление проветриванием"""
        if not self.vent_enabled or not arduino.is_connected:
            return
        
        now = datetime.now()
        
        # Проверяем, пора ли проветривать
        if self.last_vent_time and (now - self.last_vent_time) >= self.vent_interval:
            print("🌀 Начинаем проветривание...")
            
            # Открываем
            arduino.send_and_read("VENT:1")
            
            # Ждем указанное время
            time.sleep(self.vent_duration.total_seconds())
            
            # Закрываем
            arduino.send_and_read("VENT:0")
            
            # Обновляем время последнего проветривания
            self.last_vent_time = now
            
            print(f"✅ Проветривание завершено")
    
    def _check_egg_turning(self):
        """Проверка и управление поворотом яиц"""
        if not arduino.is_connected:
            return
        
        now = datetime.now()
        
        # Поворачиваем каждые 4 часа
        if self.last_turn_time and (now - self.last_turn_time) >= timedelta(hours=4):
            print("🥚 Поворачиваем яйца...")
            
            # Включаем поворот
            arduino.send_and_read("TURNER:1")
            
            # Ждем 30 секунд
            time.sleep(30)
            
            # Выключаем
            arduino.send_and_read("TURNER:0")
            
            # Обновляем время
            self.last_turn_time = now
            
            print("✅ Поворот завершен")

# Глобальный экземпляр контроллера
controller = IncubatorController()