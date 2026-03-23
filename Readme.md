# Сокращатель ссылок

## Основные возможности
*   Получить короткую ссылку из оригинальной
*   Получить редирект по короткой ссылке
*   Отследить количество редиректов

## Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/Puffs/LinkShortener.git

# Перейдите в папку проекта и установите зависимости
poetry install

# Добавьте файлы .env и .db.env в директорию app
.env
DEBUG=True
TEST_BASE_URL=http://127.0.0.1:8000/

.db.env
POSTGRES_HOST=pg
POSTGRES_PORT=5432
POSTGRES_DB=link_bd
POSTGRES_USER=user
POSTGRES_PASSWORD=123
POSTGRES_TEST_DB=test_db

# Перейдите в директорию deploy и запустите сборку докер
docker compose up -d --build

# Доступ
Сервер доступен на http://127.0.0.1:8000/

```

## Запуск тестов

```bash
# Поменяйте в файле .db.env переменную POSTGRES_HOST на localhost

# перейдите в директорию проекта

# Запустите тесты командой:

pytest
```