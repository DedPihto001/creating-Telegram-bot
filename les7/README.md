# Telegram-бот задач

Бот использует Python, `aiogram` и встроенный `sqlite3`. Задачи хранятся в файле `tasks.db` в этой же папке. Для каждой задачи сохраняются текст, пользователь, дата создания, статус и категория. Новые задачи получают статус `Новая` и категорию `Без категории`.

## Установка в Windows PowerShell

```powershell
cd "C:\Users\Lenovo\Desktop\Course\les7"
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:BOT_TOKEN = "токен-от-BotFather"
python bot.py
```

Если команда активации окружения не работает, используйте Python из окружения напрямую:

```powershell
cd "C:\Users\Lenovo\Desktop\Course\les7"
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:BOT_TOKEN = "токен-от-BotFather"
..\.venv\Scripts\python.exe bot.py
```

## Команды бота

- `/start` — приветствие и справка;
- `/add Купить молоко` — добавление задачи;
- `/list` — список задач текущего пользователя со статусом и категорией;
- `/list_csv` — отправка CSV-файла с задачами текущего пользователя. В файле есть колонки `Статус` и `Категория`.
