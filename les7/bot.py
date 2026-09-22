"""Telegram-бот для хранения пользовательских задач в SQLite."""

import asyncio
import csv
import io
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message


# База данных хранится рядом с файлом бота, чтобы путь не зависел от текущей папки запуска.
DATABASE_PATH = Path(__file__).with_name("tasks.db")


def initialize_database() -> None:
    """Создаёт таблицу tasks, если база данных запускается впервые."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def add_task(task_text: str, user: str) -> int:
    """Добавляет задачу в базу и возвращает присвоенный ей идентификатор."""
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
            (task_text, user, created_at),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_tasks(user: str) -> list[tuple[int, str, str, str]]:
    """Возвращает задачи конкретного пользователя в порядке добавления."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            """
            SELECT id, text, user, created_at
            FROM tasks
            WHERE user = ?
            ORDER BY id
            """,
            (user,),
        ).fetchall()
    return rows


def get_user_name(message: Message) -> str:
    """Формирует стабильное значение пользователя для записи в поле user."""
    if message.from_user is None:
        return "unknown"
    return str(message.from_user.id)


def create_csv_file(tasks: list[tuple[int, str, str, str]]) -> BufferedInputFile:
    """Создаёт CSV-файл в памяти и подготавливает его для отправки в Telegram."""
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["id", "text", "user", "created_at"])
    writer.writerows(tasks)
    return BufferedInputFile(
        output.getvalue().encode("utf-8-sig"),
        filename="tasks.csv",
    )


async def start_handler(message: Message) -> None:
    """Приветствует пользователя и показывает доступные команды."""
    await message.answer(
        "Привет! Я помогу хранить ваши задачи.\n\n"
        "Команды:\n"
        "/add текст задачи — добавить задачу\n"
        "/list — показать все ваши задачи\n"
        "/list_csv — скачать ваши задачи в CSV"
    )


async def add_handler(message: Message) -> None:
    """Добавляет задачу из текста после команды /add."""
    task_text = (message.text or "").partition(" ")[2].strip()
    if not task_text:
        await message.answer("Укажите текст задачи после команды, например:\n/add Купить молоко")
        return

    task_id = add_task(task_text, get_user_name(message))
    await message.answer(f"Задача добавлена. Её номер: {task_id}")


async def list_handler(message: Message) -> None:
    """Показывает пользователю список сохранённых задач."""
    tasks = get_tasks(get_user_name(message))
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    task_lines = [f"{task_id}. {text} ({created_at})" for task_id, text, _, created_at in tasks]
    await message.answer("Ваши задачи:\n" + "\n".join(task_lines))


async def list_csv_handler(message: Message) -> None:
    """Формирует CSV-файл со всеми задачами пользователя и отправляет его."""
    tasks = get_tasks(get_user_name(message))
    if not tasks:
        await message.answer("У вас пока нет задач для выгрузки.")
        return

    await message.answer_document(
        document=create_csv_file(tasks),
        caption="Выгрузка ваших задач в CSV.",
    )


async def main() -> None:
    """Инициализирует базу и запускает обработку обновлений Telegram."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Укажите токен Telegram-бота в переменной BOT_TOKEN.")

    initialize_database()
    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.message.register(start_handler, Command("start"))
    dispatcher.message.register(add_handler, Command("add"))
    dispatcher.message.register(list_handler, Command("list"))
    dispatcher.message.register(list_csv_handler, Command("list_csv"))

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
