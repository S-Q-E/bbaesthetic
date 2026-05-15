from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
TMP_DIR = BASE_DIR / "tmp"


@dataclass(slots=True, frozen=True)
class Settings:
    bot_token: str
    admin_id: int
    database_url: str
    data_dir: Path
    tmp_dir: Path
    log_level: str = "INFO"
    project_name: str = "Cosmetology Leads Bot"


def get_settings() -> Settings:
    bot_token = os.environ.get("BOT_TOKEN", "").strip()
    admin_id_raw = os.environ.get("ADMIN_ID", "").strip()
    log_level = os.environ.get("LOG_LEVEL", "INFO").strip().upper()

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set in environment variables.")

    if not admin_id_raw or not admin_id_raw.lstrip("-").isdigit():
        raise ValueError("ADMIN_ID is not set or contains invalid value.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    default_database_url = f"sqlite+aiosqlite:///{(DATA_DIR / 'app.db').as_posix()}"
    database_url = os.environ.get("DATABASE_URL", default_database_url).strip()

    return Settings(
        bot_token=bot_token,
        admin_id=int(admin_id_raw),
        database_url=database_url,
        data_dir=DATA_DIR,
        tmp_dir=TMP_DIR,
        log_level=log_level,
    )
