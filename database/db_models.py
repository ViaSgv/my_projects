from peewee import *
from datetime import datetime

db = SqliteDatabase('incubator.db')

class BaseModel(Model):
    class Meta:
        database = db

# Пользователи
class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    username = CharField(null=True)
    first_name = CharField()
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'users'

# Данные с датчиков
class SensorData(BaseModel):
    temperature = FloatField()
    humidity = FloatField()
    timestamp = DateTimeField(default=datetime.now, index=True)
    
    class Meta:
        table_name = 'sensor_data'

# Команды от админа
class AdminCommand(BaseModel):
    user_id = IntegerField()
    command = CharField()
    value = FloatField(null=True)
    timestamp = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'admin_commands'
        indexes = (
            (('timestamp',), False),
        )

# Состояние инкубатора (всегда одна запись)
class IncubatorState(BaseModel):
    target_temp = FloatField(default=37.5)
    target_hum = FloatField(default=55.0)
    is_running = BooleanField(default=False)
    last_update = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'incubator_state'

def create_tables():
    db.connect()
    db.create_tables([User, SensorData, AdminCommand, IncubatorState], safe=True)
    
    # Создаем начальное состояние и админа, если их нет
    if not IncubatorState.select().exists():
        IncubatorState.create()
    
    # Создаем админа из .env
    from tg_bot.config import Config
    if Config.ADMIN_ID and not User.select().where(User.telegram_id == Config.ADMIN_ID).exists():
        User.create(
            telegram_id=Config.ADMIN_ID,
            first_name="Admin",
            is_admin=True
        )
    
    db.close()
    print("✅ Таблицы созданы")