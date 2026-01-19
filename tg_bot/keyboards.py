from telegram import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def get_main_keyboard():
    """Главное меню"""
    keyboard = [
        [KeyboardButton("📊 Статус инкубатора")],
        [KeyboardButton("🌡️ Установить температуру"), KeyboardButton("💧 Установить влажность")],
        [KeyboardButton("🌀 Проветривание"), KeyboardButton("🥚 Поворот яиц")],
        [KeyboardButton("🚀 Запустить инкубатор"), KeyboardButton("🛑 Остановить инкубатор")],
        [KeyboardButton("📈 История данных"), KeyboardButton("⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_temperature_keyboard():
    """Клавиатура для температуры"""
    keyboard = [
        [KeyboardButton("37.0°C"), KeyboardButton("37.5°C"), KeyboardButton("38.0°C")],
        [KeyboardButton("38.5°C"), KeyboardButton("39.0°C")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_humidity_keyboard():
    """Клавиатура для влажности"""
    keyboard = [
        [KeyboardButton("45%"), KeyboardButton("50%"), KeyboardButton("55%")],
        [KeyboardButton("60%"), KeyboardButton("65%"), KeyboardButton("70%")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_ventilation_keyboard():
    """Клавиатура для проветривания"""
    keyboard = [
        [KeyboardButton("🌀 Запустить проветривание")],
        [KeyboardButton("⏱️ Настроить интервал")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_settings_keyboard():
    """Клавиатура настроек"""
    keyboard = [
        [KeyboardButton("🔌 Подключить Arduino"), KeyboardButton("🔓 Отключить Arduino")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("🧹 Очистить историю")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_confirm_keyboard():
    """Клавиатура подтверждения"""
    keyboard = [
        [KeyboardButton("✅ Да"), KeyboardButton("❌ Нет")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_history_keyboard():
    """Inline кнопки для выбора периода истории"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Последние 10", callback_data="history_last_10"),
            InlineKeyboardButton("⏰ Последний час", callback_data="history_1h")
        ],
        [
            InlineKeyboardButton("📅 Сегодня", callback_data="history_today"),
            InlineKeyboardButton("📆 24 часа", callback_data="history_24h")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============ ДОПОЛНИТЕЛЬНЫЕ КЛАВИАТУРЫ ============

def get_egg_turning_keyboard():
    """Клавиатура для поворота яиц"""
    keyboard = [
        [KeyboardButton("🔄 Запустить поворот")],
        [KeyboardButton("⏰ Настроить интервал")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_quick_actions_keyboard():
    """Быстрые действия"""
    keyboard = [
        [KeyboardButton("🌡️ Температура +0.5"), KeyboardButton("🌡️ Температура -0.5")],
        [KeyboardButton("💧 Влажность +5%"), KeyboardButton("💧 Влажность -5%")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    """Клавиатура администратора"""
    keyboard = [
        [KeyboardButton("👥 Пользователи"), KeyboardButton("📊 Логи")],
        [KeyboardButton("🔧 Системные настройки"), KeyboardButton("🔄 Перезапуск")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)