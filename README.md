# test_4_dify

Минимальное интерактивное Python-приложение для отладки Dify без Instagram, PostgreSQL и остальной части основного проекта.

## Что делает

- загружает настройки из локального `.env`;
- запрашивает текст пользователя в цикле;
- отправляет текст в Dify через `POST /chat-messages`;
- печатает ответ Dify;
- опционально отправляет трассировки в Langfuse;
- завершает работу после ввода `EXIT`.

## Загрузка окружения

Приложение проверяет пути в таком порядке:

1. `DIFY_CONSOLE_ENV_PATH`, если задана эта переменная окружения
2. локальный `.env` в этой директории
3. `C:\task-by-antipov\try_insta\.env`

Перед запуском создайте локальный `.env` из `.env.example`:

```powershell
Copy-Item .env.example .env
```

Затем заполните обязательные секреты и нужные локальные переопределения.

Обязательные переменные:

- `DIFY_API_KEY`

Опциональные переменные:

- `DIFY_API_BASE_URL`, по умолчанию: `https://api.dify.ai/v1`
- `DIFY_RESPONSE_MODE`, по умолчанию: `blocking`
- `DIFY_TIMEOUT_SECONDS`, по умолчанию: `30`
- `DIFY_USER_ID`, по умолчанию: `interactive-console`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PORT`, по умолчанию для локального запуска: `3001`
- `LANGFUSE_BASE_URL`, по умолчанию для локального запуска: `http://localhost:3001`

## Langfuse

Локальные сервисы Langfuse описаны в [docker-compose.yml](docker-compose.yml).

Перед запуском убедитесь, что в локальном `.env` заполнены корректные Langfuse-секреты.

Запуск:

```powershell
cd C:\task-by-antipov\test_4_dify
docker compose up -d
```

Затем откройте:

```text
http://localhost:3001
```

Важно:

- compose-файл включает headless-инициализацию Langfuse через `LANGFUSE_INIT_*`;
- `LANGFUSE_INIT_*` можно использовать, чтобы на свежем локальном стенде создать организацию, проект и администратора;
- после `docker compose up -d` дождитесь готовности Langfuse и войдите на `http://localhost:3001`;
- если в `.env` заданы bootstrap-учётные данные, входите через `LANGFUSE_INIT_USER_EMAIL` и `LANGFUSE_INIT_USER_PASSWORD`;
- если меняете ключи проекта в `.env`, держите в синхронизации `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` и `LANGFUSE_INIT_PROJECT_PUBLIC_KEY` / `LANGFUSE_INIT_PROJECT_SECRET_KEY`.

## Запуск

Лёгкий режим только для Dify:

```powershell
cd C:\task-by-antipov\test_4_dify
.\.venv\Scripts\python.exe light_main.py
```

`light_main.py` использует только настройки `DIFY_*` из `.env`. Он не импортирует код Langfuse и не требует `docker compose`.

Полный режим с опциональной трассировкой Langfuse:

```powershell
cd C:\task-by-antipov\test_4_dify
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Остановка

Введите:

```text
EXIT
```
