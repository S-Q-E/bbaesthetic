#!/bin/sh
set -e

echo "=== STARTUP: resetting migrations state ==="

mkdir -p /app/data /app/tmp

# 1. Пытаемся применить миграции
echo "Running migrations..."
alembic upgrade head || {
  echo "Migration failed → resetting Alembic state..."

  # 2. Сброс версии миграций
  python -c "
from app.database import Base
from app.database.session import engine

# просто трогаем БД чтобы гарантировать создание
Base.metadata.create_all(bind=engine)
print('Tables ensured')
"

  # 3. Принудительно синхронизируем alembic
  alembic stamp head || true
}

echo "=== STARTUP COMPLETE ==="

exec python -m app.main