import os
import logging
import telegram
from typing import Tuple

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALLOWED_EVENTS = os.getenv("ALLOWED_EVENTS", "").split(',')

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def process_event(event, data) -> Tuple[str, int]:
    try:
        logging.info(f"Processing event: {event}")
        if event == "Pipeline Hook":
            return handle_pipeline(data)
        elif event == "Merge Request Hook":
            return handle_merge_request(data)
        elif event == "Push Hook":
            return handle_push(data)
        logging.warning(f"Unknown event type: {event}")
        return "Unknown event", 400
    except Exception as e:
        logging.error(f"Error processing event: {str(e)}")
        return f"Error: {str(e)}", 500

def handle_pipeline(data):
    """ Обработка событий CI/CD """
    status = data['object_attributes']['status']
    project = data['project']['name']
    branch = data['object_attributes']['ref']
    duration = data['object_attributes']['duration']
    url = data['object_attributes']['web_url']

    if "pipeline" not in ALLOWED_EVENTS:
        return "Ignored", 200

    message = f"🚀 *CI/CD Pipeline в {project}*\nВетка: `{branch}`\nСтатус: *{status}*\nДлительность: {duration} сек\n"
    message += f"[Открыть Pipeline]({url})"

    send_telegram_message(message)
    return "OK", 200

def handle_merge_request(data):
    """ Обработка Merge Requests """
    action = data['object_attributes']['action']
    project = data['project']['name']
    author = data['user']['name']
    source_branch = data['object_attributes']['source_branch']
    target_branch = data['object_attributes']['target_branch']
    url = data['object_attributes']['url']

    if "merge_request" not in ALLOWED_EVENTS:
        return "Ignored", 200

    message = f"🔀 *Merge Request в {project}*\nАвтор: {author}\nВетка: `{source_branch}` → `{target_branch}`\nДействие: *{action}*\n"
    message += f"[Открыть MR]({url})"

    send_telegram_message(message)
    return "OK", 200

def handle_push(data):
    """ Обработка Push (коммитов) """
    project = data['project']['name']
    author = data['user_name']
    branch = data['ref'].split('/')[-1]
    commits = data['total_commits_count']

    if "push" not in ALLOWED_EVENTS:
        return "Ignored", 200

    message = f"📌 *Новый Push в {project}*\nАвтор: {author}\nВетка: `{branch}`\nКоммитов: {commits}\n"

    for commit in data['commits']:
        message += f"\n- {commit['message']} ([{commit['id'][:7]}]({commit['url']}))"

    send_telegram_message(message)
    return "OK", 200

def send_telegram_message(message: str) -> None:
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, 
                        text=message, 
                        parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {str(e)}")
        raise
