# Telegram-бот задач

Бот использует Python, `aiogram` и встроенный `sqlite3`. Задачи хранятся в файле `tasks.db` в этой же папке.

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
- `/list` — список задач текущего пользователя;
- `/list_csv` — отправка CSV-файла с задачами текущего пользователя.
