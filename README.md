# Telegram Lead Bot for Cosmetologist / Weight Loss Specialist

Production-ready Telegram-бот на `Python 3.12` и `aiogram 3.x` для максимально быстрого сбора заявок на консультацию.

Основная цель проекта:
- провести пользователя по сценарию меньше чем за минуту;
- минимизировать количество кликов;
- сохранить заявку в SQLite;
- мгновенно отправить лид админу;
- дать админу возможность выгрузить все заявки в Excel.

## Возможности

- Быстрый сценарий заявки через FSM
- Чистый UX без лишнего текста
- Request contact кнопка для телефона
- Валидация имени, возраста, города и цели похудения
- Защита от пустых сообщений
- Сохранение заявок в SQLite через SQLAlchemy 2.0 Async
- Репозиторий для работы с БД
- Миграции через Alembic
- Админ-уведомление с inline-кнопками
- Команда `/export` для экспорта заявок в `.xlsx`
- Автоматическое удаление временного Excel-файла после отправки
- Production-ready Docker и Docker Compose
- Консольное логирование
- Полностью асинхронный код

## Стек

- Python 3.12
- aiogram 3.x
- SQLAlchemy 2.0 async
- SQLite3
- Alembic
- openpyxl
- python-dotenv
- Docker
- Docker Compose

## Структура проекта

```text
.
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── alembic.ini
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── data/
│   └── .gitkeep
├── tmp/
│   └── .gitkeep
└── app/
    ├── __init__.py
    ├── main.py
    ├── config/
    │   ├── __init__.py
    │   ├── logging.py
    │   └── settings.py
    ├── database/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── session.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── application.py
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   └── application.py
    │   └── migrations/
    │       ├── README
    │       ├── env.py
    │       ├── script.py.mako
    │       └── versions/
    │           ├── __init__.py
    │           └── 20260515_0001_create_applications_table.py
    ├── filters/
    │   ├── __init__.py
    │   └── admin.py
    ├── handlers/
    │   ├── __init__.py
    │   ├── admin.py
    │   └── user.py
    ├── keyboards/
    │   ├── __init__.py
    │   ├── inline.py
    │   └── reply.py
    ├── middlewares/
    │   ├── __init__.py
    │   ├── database.py
    │   └── errors.py
    ├── services/
    │   ├── __init__.py
    │   ├── application.py
    │   ├── dto.py
    │   └── export.py
    ├── states/
    │   ├── __init__.py
    │   └── application.py
    └── utils/
        ├── __init__.py
        ├── chat_actions.py
        ├── messages.py
        └── validators.py
```

## Как работает сценарий

1. Пользователь отправляет `/start`
2. Бот показывает приветствие и кнопку `Оставить заявку`
3. Бот последовательно спрашивает:
   - имя
   - возраст
   - город
   - сколько кг хочет сбросить
   - номер телефона через `request_contact`
4. После получения данных:
   - заявка сохраняется в SQLite
   - админу приходит оформленное уведомление
   - пользователь получает подтверждение

## Формат данных в БД

Таблица `applications`:

- `id`
- `full_name`
- `age`
- `city`
- `target_weight_loss`
- `phone`
- `telegram_username`
- `telegram_id`
- `created_at`

## Настройка окружения

Скопируйте пример env-файла:

```bash
cp .env.example .env
```

Для Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Заполните `.env`:

```env
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
```

Опционально можно добавить:

```env
LOG_LEVEL=INFO
DATABASE_URL=sqlite+aiosqlite:///./data/app.db
```

## Локальный запуск без Docker

### 1. Создайте виртуальное окружение

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Установите зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Примените миграции

```bash
alembic upgrade head
```

### 4. Запустите бота

```bash
python -m app.main
```

## Docker запуск

После заполнения `.env` достаточно одной команды:

```bash
docker compose up --build
```

Что происходит автоматически:

- собирается Docker image;
- создаются volume для `data` и `tmp`;
- выполняются миграции Alembic;
- бот запускается автоматически.

Для фонового режима:

```bash
docker compose up --build -d
```

Остановить контейнер:

```bash
docker compose down
```

Посмотреть логи:

```bash
docker compose logs -f
```

## Миграции Alembic

Применить миграции:

```bash
alembic upgrade head
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

Создать новую миграцию вручную:

```bash
alembic revision -m "add new column"
```

Если меняете схему БД:

1. Обновите SQLAlchemy-модель
2. Создайте новую миграцию
3. Проверьте `upgrade()` и `downgrade()`
4. Примените миграции локально
5. После этого обновляйте контейнер

## Команда `/export`

Команда доступна только пользователю с `ADMIN_ID`.

Сценарий:

1. Админ отправляет `/export`
2. Бот отвечает `📊 Экспортирую заявки...`
3. Бот выгружает все записи из SQLite
4. Создает `.xlsx` файл через `openpyxl`
5. Отправляет файл в Telegram
6. Удаляет временный файл

Если заявок нет, бот отправит:

```text
Заявок пока нет.
```

## Что находится в ключевых файлах

- `app/main.py` — точка входа, инициализация бота, middleware и polling
- `app/handlers/user.py` — пользовательский сценарий заявки
- `app/handlers/admin.py` — экспорт и admin callbacks
- `app/database/models/application.py` — ORM-модель заявки
- `app/database/repositories/application.py` — репозиторий работы с заявками
- `app/services/export.py` — сборка Excel-файла
- `app/database/migrations/versions/20260515_0001_create_applications_table.py` — первая миграция

## Как поменять `ADMIN_ID`

1. Откройте `.env`
2. Замените значение `ADMIN_ID`
3. Перезапустите приложение

Локально:

```bash
python -m app.main
```

В Docker:

```bash
docker compose up -d --build
```

## Как обновлять проект

### Локально

```bash
git pull
pip install -r requirements.txt
alembic upgrade head
python -m app.main
```

### В Docker

```bash
git pull
docker compose up -d --build
```

Если добавились новые миграции, `entrypoint.sh` применит их автоматически при старте контейнера.

## Деплой на Railway

SQLite на Railway требует сохранения файла БД в persistent volume. Без volume база будет теряться при пересоздании контейнера.

### Шаги

1. Создайте новый проект в Railway
2. Подключите GitHub-репозиторий
3. Убедитесь, что Railway использует `Dockerfile`
4. Добавьте переменные окружения:
   - `BOT_TOKEN`
   - `ADMIN_ID`
5. Создайте persistent volume
6. Смонтируйте volume в путь `/app/data`
7. Задеплойте проект

### Что важно для Railway

- `entrypoint.sh` сам выполнит `alembic upgrade head`
- бот стартует командой `python -m app.main`
- файл SQLite будет храниться в `/app/data/app.db`

### Рекомендуемый порядок обновления на Railway

1. Отправьте изменения в Git
2. Railway подтянет новый commit
3. При новом старте контейнера автоматически выполнятся миграции
4. Бот продолжит работу на обновленном коде

## Production notes

- Код полностью асинхронный
- Логи идут в консоль
- Все ошибки верхнего уровня логируются через middleware
- FSM использует `MemoryStorage`
- Для текущего сценария этого достаточно, так как важные бизнес-данные сохраняются в SQLite сразу после заполнения формы

## Команды запуска

Локально:

```bash
alembic upgrade head
python -m app.main
```

В Docker:

```bash
docker compose up --build
```

## Полезные улучшения на будущее

- Добавить Redis storage для FSM
- Добавить статусы заявок в БД
- Добавить несколько администраторов
- Добавить webhooks для cloud-hosting
- Добавить локализацию под несколько языков
