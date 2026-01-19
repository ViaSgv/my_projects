from peewee import SqliteDatabase

db = SqliteDatabase('incubator.db')

def connect_db():
    if db.is_closed():
        db.connect()

def close_db():
    if not db.is_closed():
        db.close()

# Простой контекстный менеджер
def with_db(func):
    """Декоратор для автоматического подключения к БД"""
    def wrapper(*args, **kwargs):
        connect_db()
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
        finally:
            close_db()
    return wrapper