# SecretPlace

Сервис для передачи одноразовых секретов: бэкенд на FastAPI (корень репозитория) и SPA на React (`frontend/`).

## Запуск для демонстрации

Фронтенд собирается в статику, которую раздаёт сам FastAPI, поэтому нужен один процесс:

```sh
cd frontend
npm install
npm run build
cd ..
uv run uvicorn main:app
```

Приложение откроется на http://localhost:8000.

## Разработка

В двух терминалах:

```sh
uv run uvicorn main:app --reload    # бэкенд на :8000
cd frontend && npm run dev          # фронтенд на :5173
```

Открывать http://localhost:5173: Vite проксирует запросы `/api` на бэкенд и перезагружает страницу при изменениях.
