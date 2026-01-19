from datetime import datetime, timedelta
from .db_models import *

class SimpleCRUD:
    """Минимальный CRUD для основных операций"""
    
    # ============ ПОЛЬЗОВАТЕЛИ ============
    
    def create_user(self, telegram_id, first_name, username=None):
        """Создать/обновить пользователя"""
        try:
            user, created = User.get_or_create(
                telegram_id=telegram_id,
                defaults={'first_name': first_name, 'username': username}
            )
            
            if not created:
                user.first_name = first_name
                user.username = username
                user.save()
            
            return user
        except Exception as e:
            print(f"Ошибка создания пользователя: {e}")
            return None
    
    def get_user(self, telegram_id):
        """Получить пользователя"""
        try:
            return User.get(User.telegram_id == telegram_id)
        except User.DoesNotExist:
            return None
    
    # ============ ДАННЫЕ ДАТЧИКОВ ============
    
    def add_sensor_data(self, temperature, humidity):
        """Просто записать данные с датчиков"""
        try:
            return SensorData.create(
                temperature=temperature,
                humidity=humidity
            )
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
            return None
    
    def get_latest_sensor_data(self, limit=10):
        """Получить последние N записей"""
        try:
            query = SensorData.select().order_by(SensorData.timestamp.desc()).limit(limit)
            return list(query)
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            return []
    
    def get_sensor_data_since(self, hours=24):
        """Получить данные за последние N часов"""
        try:
            time_threshold = datetime.now() - timedelta(hours=hours)
            query = SensorData.select().where(SensorData.timestamp >= time_threshold)
            return list(query)
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            return []
    
    # ============ КОМАНДЫ ============
    
    def add_command(self, user_id, command, value=None):
        """Добавить команду от админа"""
        try:
            return AdminCommand.create(
                user_id=user_id,
                command=command,
                value=value
            )
        except Exception as e:
            print(f"Ошибка сохранения команды: {e}")
            return None
    
    def get_last_commands(self, limit=20):
        """Получить последние команды"""
        try:
            query = AdminCommand.select().order_by(AdminCommand.timestamp.desc()).limit(limit)
            return list(query)
        except Exception as e:
            print(f"Ошибка получения команд: {e}")
            return []
    
    # ============ СОСТОЯНИЕ ИНКУБАТОРА ============
    
    def get_state(self):
        """Получить текущее состояние"""
        try:
            return IncubatorState.select().get()
        except IncubatorState.DoesNotExist:
            return IncubatorState.create()
    
    def update_state(self, **kwargs):
        """Обновить состояние инкубатора"""
        try:
            state = self.get_state()
            for key, value in kwargs.items():
                setattr(state, key, value)
            state.last_update = datetime.now()
            state.save()
            return state
        except Exception as e:
            print(f"Ошибка обновления состояния: {e}")
            return None
    
    def set_temperature(self, temperature):
        """Установить целевую температуру"""
        return self.update_state(target_temp=temperature)
    
    def set_humidity(self, humidity):
        """Установить целевую влажность"""
        return self.update_state(target_hum=humidity)
    
    def start_incubator(self):
        """Запустить инкубатор"""
        return self.update_state(is_running=True)
    
    def stop_incubator(self):
        """Остановить инкубатор"""
        return self.update_state(is_running=False)

# Глобальный экземпляр для удобства
db = SimpleCRUD()