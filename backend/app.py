"""Flask REST API exposing the published Telegram posts."""
from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS

from .database import get_connection, initialise_database

app = Flask(__name__)
CORS(app)

initialise_database()

REQUIRED_FIELDS = {"title", "summary", "source_url", "release_date"}


def serialise_row(row) -> Dict[str, Any]:
    return {key: row[key] for key in row.keys()}


@app.get("/api/posts")
def list_posts():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, summary, source_url, image_url, release_date, provider, type, created_at FROM posts ORDER BY created_at DESC"
        ).fetchall()
    items: List[Dict[str, Any]] = [serialise_row(row) for row in rows]
    return jsonify({"items": items})


@app.get("/api/posts/<int:post_id>")
def retrieve_post(post_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, summary, source_url, image_url, release_date, provider, type, created_at FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()
    if row is None:
        return jsonify({"error": "not_found", "details": "Post not found"}), HTTPStatus.NOT_FOUND
    return jsonify(serialise_row(row))


@app.post("/api/posts")
def create_post():
    if not request.is_json:
        return jsonify({"error": "invalid_request", "details": "Request payload must be JSON"}), HTTPStatus.BAD_REQUEST
    payload: Dict[str, Any] = request.get_json(force=True)

    missing = REQUIRED_FIELDS.difference(payload)
    if missing:
        return (
            jsonify({"error": "invalid_request", "details": f"Missing required fields: {', '.join(sorted(missing))}"}),
            HTTPStatus.BAD_REQUEST,
        )

    values = (
        payload.get("title", "").strip(),
        payload.get("summary", "").strip(),
        payload.get("source_url", "").strip(),
        payload.get("image_url"),
        payload.get("release_date", "").strip(),
        payload.get("provider"),
        payload.get("type"),
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO posts (title, summary, source_url, image_url, release_date, provider, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        connection.commit()
        new_id = cursor.lastrowid

        row = connection.execute(
            "SELECT id, title, summary, source_url, image_url, release_date, provider, type, created_at FROM posts WHERE id = ?",
            (new_id,),
        ).fetchone()

    return jsonify(serialise_row(row)), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(debug=True)
