import serial
import time
from datetime import datetime

class ArduinoSerialSimple:
    """Простой класс для работы с Arduino через Serial"""
    
    def __init__(self):
        self.port = None
        self.baudrate = 9600
        self.serial = None
        self.is_connected = False
    
    def connect(self, port='COM5', baudrate=9600):
        """Упрощенное подключение к Arduino"""
        print(f"[ARDUINO] Подключение к {port}...")
        
        try:
            # Пробуем открыть порт
            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=2,
                write_timeout=2
            )
            
            print(f"[ARDUINO] Порт {port} открыт")
            
            # Даем Arduino время на перезагрузку
            import time
            time.sleep(3)
            
            # Очищаем буфер
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            
            # Пробуем прочитать приветствие
            time.sleep(1)
            if self.serial.in_waiting > 0:
                welcome = self.serial.readline().decode('utf-8', errors='ignore').strip()
                print(f"[ARDUINO] Приветствие: {welcome}")
            
            # Отправляем тестовую команду
            self.serial.write(b"PING\n")
            self.serial.flush()
            
            # Ждем ответа
            time.sleep(2)
            
            if self.serial.in_waiting > 0:
                response = self.serial.readline().decode('utf-8', errors='ignore').strip()
                print(f"[ARDUINO] Ответ на PING: {response}")
                
                if "PONG" in response or "ARDUINO" in response or response:
                    print(f"[ARDUINO] ✓ Подключено к {port}")
                    self.port = port
                    self.baudrate = baudrate
                    self.is_connected = True
                    return True
                else:
                    print(f"[ARDUINO] Ответ не распознан: {response}")
                    # Все равно считаем подключенной
                    self.port = port
                    self.baudrate = baudrate
                    self.is_connected = True
                    print(f"[ARDUINO] ⚠ Подключено в режиме 'доверия'")
                    return True
            else:
                print(f"[ARDUINO] Нет ответа на PING")
                # Проверяем, может порт просто открыт
                self.port = port
                self.baudrate = baudrate
                self.is_connected = True
                print(f"[ARDUINO] ⚠ Подключено без проверки ответа")
                return True
                
        except Exception as e:
            print(f"[ARDUINO] ✗ Ошибка подключения: {e}")
            return False
    
    def disconnect(self):
        """Отключиться"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.is_connected = False
            print("Отключено от Arduino")
    
    def send(self, command):
        """Просто отправить команду"""
        if not self.serial or not self.serial.is_open:
            return False
        
        try:
            self.serial.write(f"{command}\n".encode('utf-8'))
            self.serial.flush()
            return True
        except:
            return False
    
    def read(self):
        """Прочитать ответ"""
        if not self.serial or not self.serial.is_open:
            return None
        
        try:
            response = self.serial.readline().decode('utf-8').strip()
            return response if response else None
        except:
            return None
    
    def get_data(self):
        """Получить данные с датчиков"""
        response = self.send_and_read("GET_DATA")
        if not response:
            return None
        
        try:
            if "," in response:
                parts = response.split(",")
                if len(parts) >= 2:
                    temp = float(parts[0].strip())
                    hum = float(parts[1].strip())
                    from datetime import datetime
                    return temp, hum, datetime.now()
        except:
            pass
        
        return None

    def get_emulated_data(self):
        """Генерация эмулированных данных"""
        import random
        from datetime import datetime
        
        # Базовые значения
        base_temp = 37.5
        base_hum = 55.0
        
        # Случайные колебания
        temp = base_temp + random.uniform(-0.3, 0.3)
        hum = base_hum + random.uniform(-2.0, 2.0)
        
        # Ограничения
        temp = max(36.0, min(39.0, temp))
        hum = max(45.0, min(65.0, hum))
        
        print(f"[Эмуляция] Температура: {temp:.1f}°C, Влажность: {hum:.1f}%")
        
        return temp, hum, datetime.now()
        
    def send_and_read(self, command):
            """Отправить и прочитать ответ"""
            if self.send(command):
                return self.read()
            return None
        
    def heater_on(self):
            """Включить нагреватель"""
            return self.send_and_read("HEATER:1") == "OK"
        
    def heater_off(self):
            """Выключить нагреватель"""
            return self.send_and_read("HEATER:0") == "OK"
        
    def humidifier_on(self):
            """Включить увлажнитель"""
            return self.send_and_read("HUMIDIFIER:1") == "OK"
        
    def humidifier_off(self):
            """Выключить увлажнитель"""
            return self.send_and_read("HUMIDIFIER:0") == "OK"
        
    def fan_on(self):
            """Включить вентилятор"""
            return self.send_and_read("FAN:1") == "OK"
        
    def fan_off(self):
            """Выключить вентилятор"""
            return self.send_and_read("FAN:0") == "OK"
        
    def turner_on(self):
            """Включить поворот яиц"""
            return self.send_and_read("TURNER:1") == "OK"
        
    def turner_off(self):
            """Выключить поворот яиц"""
            return self.send_and_read("TURNER:0") == "OK"
        
    def vent_on(self):
            """Открыть проветривание"""
            return self.send_and_read("VENT:1") == "OK"
        
    def vent_off(self):
            """Закрыть проветривание"""
            return self.send_and_read("VENT:0") == "OK"
        
    def all_off(self):
            """Выключить все устройства"""
            return self.send_and_read("ALL_OFF") == "OK"


arduino = ArduinoSerialSimple()