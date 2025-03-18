# GitLab Telegram Bot

Этот бот получает уведомления от GitLab и отправляет их в Telegram.

## 🚀 Установка и запуск

### 1️⃣ Клонирование репозитория

```bash
git clone https://github.com/your-repo/gitlab-telegram-bot.git
cd gitlab-telegram-bot
```

### 2️⃣ Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3️⃣ Настройка переменных окружения
Создайте файл `.env` и добавьте:

```ini
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
ALLOWED_EVENTS=pipeline,merge_request,push
```

4️⃣ Запуск бота

```bash
python server/app.py
```

5️⃣ Запуск через Docker

```bash
docker-compose up --build -d
```

## Использование

Настройте вебхуки в вашем проекте GitLab, чтобы они указывали на ваш сервер:


$$
http://<your_server_ip>:5000/webhook
$$

## Лицензия

Этот проект лицензирован под лицензией MIT.