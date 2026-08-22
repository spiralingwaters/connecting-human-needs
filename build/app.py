import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "site.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "db", "seed.sql")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        db.executescript(f.read())
    with open(SEED_PATH) as f:
        db.executescript(f.read())
    db.commit()
    db.close()


@app.route("/")
def index():
    db = get_db()
    row = db.execute(
        "SELECT value FROM site_meta WHERE key = 'tagline'"
    ).fetchone()
    tagline = row["value"] if row else ""
    posts = db.execute(
        "SELECT author_name, body, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", tagline=tagline, posts=posts)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        author_name = request.form.get("author_name", "").strip()
        body = request.form.get("body", "").strip()
        if author_name and body:
            db = get_db()
            db.execute(
                "INSERT INTO posts (author_name, body) VALUES (?, ?)",
                (author_name, body),
            )
            db.commit()
        return redirect(url_for("index"))
    return render_template("new_post.html")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="127.0.0.1", port=5000)
