# SecretPlace

Веб сервис для передачи одноразовых секретов, реализованный в рамках выполнения лабораторных работ по дисциплине "Разработка Интернет Приложений".


## Программный стек
- Backend: `FastAPI`
- Frontend: `React` + `Vite` (AI Assisted)
- База данных: `SQLAlchemy` + `SQLite` + `Alembic`


## Установка и запуск сервера

### Локально

Необходим установленный пакетный менеджер `uv`.

```
git clone <адрес репозитория>
cd SecretPlace
uv sync
uv run main:app
```

Приложение будет доступно на адресе: `http://127.0.0.1:8080`.

### Docker

Необходимы установленные `Docker` и `Docker Compose`.

```
git clone <адрес репозитория>
cd SecretPlace
docker compose up --build -d
```

Приложение будет доступно на адресе: `http://127.0.0.1:8080`.


## CLI Утилиты

CLI утилиты находятся в директории `SecretPlace/app/cli`.

### Удаление просроченных секретов

Для удаления просроченных секретов используется утилита `delete_expired_secrets.py`.

Утилита удаляет из базы данных все секреты, срок жизни которых истек на момент запуска, и выводит их количество.

Запуск производится из корня проекта.

Использование:
```
uv run python -m app.cli.delete_expired_secrets [--dry-run]
```

Параметры:
- `--dry-run` - секреты не удаляются, утилита только подсчитывает количество просроченных секретов.
- `-h`, `--help` - вывод справки.

Пример вывода:
```
$ uv run python -m app.cli.delete_expired_secrets --dry-run
Expired secrets: 3

$ uv run python -m app.cli.delete_expired_secrets
Deleted expired secrets: 3
```


## TODO / Планы на будущее
- Переход с SQLite на PostgreSQL.
- Рефакторинг бэкенда под асинхронную архитектуру.
- Настоящее шифрование секретов в БД.