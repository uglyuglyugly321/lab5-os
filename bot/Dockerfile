FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости для psycopg2 и pip
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir python-telegram-bot==20.3 psycopg2-binary==2.9.6 && \
    apt-get remove -y gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY bot.py .

CMD ["python", "bot.py"]