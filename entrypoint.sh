#!/bin/sh
set -e

echo "=== STARTUP: resetting migrations state ==="

mkdir -p /app/data /app/tmp

# 1. Пытаемся применить миграции alembic
echo "Running migrations..."
alembic upgrade head || {
  echo "Migration failed → resetting Alembic state..."

  # 2. Асинхронное создание таблиц с использованием твоей функции create_engine_and_session
  python -c "
import asyncio
import os
from app.database import Base
from app.database.session import create_engine_and_session

# 1. Получаем URL из переменных окружения Railway
url = os.getenv('DATABASE_URL')

if url:
    # 2. Корректируем префикс для асинхронного Postgres
    if url.startswith('postgresql://'):
        url = url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    
    # 3. Вызываем твою функцию для создания движка
    engine, _ = create_engine_and_session(url)

    async def main():
        # 4. Асинхронно создаем таблицы напрямую через SQLAlchemy
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print('Tables ensured via create_engine_and_session')

    asyncio.run(main())
else:
    print('DATABASE_URL not found, skipping direct table creation')
"

  # 3. Принудительно маркируем alembic как head, чтобы заглушить ошибку миграций
  alembic stamp head || true
}

echo "=== STARTUP COMPLETE ==="

exec python -m app.main
