#!/bin/sh
set -e

echo "=== STARTUP: resetting migrations state ==="

mkdir -p /app/data /app/tmp

# 1. Пытаемся применить миграции
echo "Running migrations..."
alembic upgrade head || {
  echo "Migration failed → resetting Alembic state..."

  # 2. Асинхронное создание таблиц напрямую через SQLAlchemy, если миграции легли
  python -c "
import asyncio
from app.database import Base
from app.database.session import engine  # Проверьте, что в session.py переменная зовется именно engine

async def main():
    # Используем begin() и run_sync для асинхронного создания таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Tables ensured via async approach')

asyncio.run(main())
"

  # 3. Принудительно синхронизируем alembic
  alembic stamp head || true
}

echo "=== STARTUP COMPLETE ==="

exec python -m app.main
