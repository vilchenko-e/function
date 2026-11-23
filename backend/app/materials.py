from datetime import datetime, timezone

from app.database import get_connection
from app.schemas import MaterialCreate

def create_material(material: MaterialCreate) -> dict | None:
    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")

        existing = connection.execute(
            """
            SELECT id
            FROM materials
            WHERE title = ?
              AND content = ?
              AND sources = ?
            LIMIT 1
            """,
            (
                material.title,
                material.content,
                material.sources,
            ),
        ).fetchone()

        if existing is not None:
            return None

        cursor = connection.execute(
            """
            INSERT INTO materials (
                title,
                content,
                sources,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                material.title,
                material.content,
                material.sources,
                timestamp,
                timestamp,
            ),
        )

        row = connection.execute(
            "SELECT * FROM materials WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return dict(row)


def list_materials() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM materials ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]


def get_material(material_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM materials WHERE id = ?",
            (material_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)
