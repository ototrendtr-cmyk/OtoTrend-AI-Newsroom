"""Eski yerel veritabanlarını zararsız küçük şema güncellemeleriyle uyumlar."""

from __future__ import annotations

from sqlalchemy import inspect, text

from app.database.database import engine


def ensure_database_upgrades() -> None:
    """Alembic çalıştırılmamış mevcut SQLite kurulumlarını da güncel tutar."""
    inspector = inspect(engine)
    with engine.begin() as connection:
        if inspector.has_table("sources"):
            source_columns = {
                column["name"] for column in inspector.get_columns("sources")
            }
            required_source_columns = {
                "consecutive_failures": "INTEGER NOT NULL DEFAULT 0",
                "auto_disabled_at": "DATETIME",
            }
            for column_name, definition in required_source_columns.items():
                if column_name not in source_columns:
                    connection.execute(
                        text(
                            f"ALTER TABLE sources ADD COLUMN {column_name} {definition}"
                        )
                    )

        if inspector.has_table("news"):
            news_columns = {column["name"] for column in inspector.get_columns("news")}
            required_news_columns = {
                "ai_attempts": "INTEGER NOT NULL DEFAULT 0",
                "ai_last_error": "TEXT",
                "ai_next_retry_at": "DATETIME",
            }
            for column_name, definition in required_news_columns.items():
                if column_name not in news_columns:
                    connection.execute(
                        text(f"ALTER TABLE news ADD COLUMN {column_name} {definition}")
                    )

            connection.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS ix_news_ai_retry_queue "
                    "ON news (ai_processed, status, ai_next_retry_at, created_at)"
                )
            )
