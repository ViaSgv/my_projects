from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from tg_bot.handlers import create_bot_application
from tg_bot.config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем FastAPI приложение
app = FastAPI(title="Incubator Bot API")

# Создаем бота
bot_app = create_bot_application()

@app.on_event("startup")
async def startup_event():
    """Действия при запуске"""
    logger.info("Starting up incubator bot...")
    
    # Устанавливаем webhook
    if Config.WEBHOOK_URL:
        webhook_url = f"{Config.WEBHOOK_URL}/webhook"
        await bot_app.bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.info("Webhook URL not set, using polling")

@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке"""
    logger.info("Shutting down incubator bot...")
    if Config.WEBHOOK_URL:
        await bot_app.bot.delete_webhook()
    await bot_app.shutdown()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Incubator Bot API",
        "status": "running",
        "webhook": Config.WEBHOOK_URL or "not set"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {"status": "healthy"}

@app.post("/webhook")
async def webhook(request: Request):
    """Эндпоинт для webhook от Telegram"""
    try:
        # Получаем обновление от Telegram
        update_data = await request.json()
        
        # Обрабатываем обновление
        await bot_app.process_update(update_data)
        
        return JSONResponse(content={"status": "ok"})
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def api_status():
    """Статус API"""
    return {
        "bot_running": True,
        "webhook_enabled": bool(Config.WEBHOOK_URL),
        "admin_id": Config.ADMIN_ID
    }