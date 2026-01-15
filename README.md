LAB5-OS/
├── bot/                    # Исходный код Telegram-бота
│   ├── bot.py               # Основная логика бота (handlers, команды)
│   ├── db.py                # Работа с PostgreSQL (подключение, запросы)
│   ├── Dockerfile           # Dockerfile для сборки контейнера бота
│   └── requirements.txt     # Python-зависимости бота
│
├── docker-compose.yml       # Запуск бота и PostgreSQL через Docker Compose
├── requirements.txt         # (опционально) общие зависимости проекта
└── README.md                # Описание проекта и инструкция по запуску
