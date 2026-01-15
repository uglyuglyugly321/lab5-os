import os
import psycopg2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# -----------------------
# Настройки подключения к существующей базе hotel
# -----------------------
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")  # если база локальная
DB_NAME = os.getenv("DB_NAME", "hotel")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Установите TELEGRAM_BOT_TOKEN!")

# -----------------------
# Работа с таблицей hotel
# -----------------------
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def list_hotels():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM hotel")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_hotel(name, city):
    conn = get_connection()
    cur = conn.cursor()
    # просто вставляем name и city, не возвращаем id
    cur.execute("INSERT INTO hotel (name, city) VALUES (%s, %s)", (name, city))
    conn.commit()
    cur.close()
    conn.close()

# -----------------------
# Команды бота
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для работы с таблицей hotel.")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hotels = list_hotels()
    if not hotels:
        await update.message.reply_text("Нет записей в таблице hotel.")
        return
    
    msg_lines = []
    for i, row in enumerate(hotels, start=1):
        # row — это кортеж с любым количеством колонок
        row_str = " | ".join(str(x) for x in row)
        msg_lines.append(f"{i}. {row_str}")
    
    msg = "\n".join(msg_lines)
    await update.message.reply_text(msg)
    
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Используйте: /add <name> <city>")
        return
    name = context.args[0]
    city = context.args[1]
    add_hotel(name, city)
    await update.message.reply_text(f"Отель '{name}' в городе '{city}' добавлен!")

# -----------------------
# Запуск бота
# -----------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("add", add_command))
    app.run_polling()