import hashlib
import os
import secrets
import sqlite3

from flask import Flask, g, redirect, render_template, request, session, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "site.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "db", "seed.sql")
SECRET_KEY_PATH = os.path.join(BASE_DIR, "db", "flask_secret_key")

app = Flask(__name__)

if os.path.exists(SECRET_KEY_PATH):
    with open(SECRET_KEY_PATH) as f:
        app.secret_key = f.read().strip()
else:
    app.secret_key = secrets.token_hex(32)
    with open(SECRET_KEY_PATH, "w") as f:
        f.write(app.secret_key)


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


def hash_key(raw_key):
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    db = get_db()
    return db.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchone()


@app.context_processor
def inject_current_user():
    return {"current_user": current_user()}


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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            return render_template("signup.html", error="Enter a username.")
        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            return render_template(
                "signup.html", error="That username is taken."
            )
        raw_key = secrets.token_urlsafe(24)
        db.execute(
            "INSERT INTO users (username, key_hash) VALUES (?, ?)",
            (username, hash_key(raw_key)),
        )
        db.commit()
        return render_template("signup.html", issued_key=raw_key, username=username)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        raw_key = request.form.get("key", "").strip()
        db = get_db()
        user = db.execute(
            "SELECT id FROM users WHERE key_hash = ?", (hash_key(raw_key),)
        ).fetchone()
        if user is None:
            return render_template("login.html", error="Key not recognized.")
        session["user_id"] = user["id"]
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/new", methods=["GET", "POST"])
def new_post():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            db = get_db()
            db.execute(
                "INSERT INTO posts (author_name, author_id, body) VALUES (?, ?, ?)",
                (user["username"], user["id"], body),
            )
            db.commit()
        return redirect(url_for("index"))
    return render_template("new_post.html")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="127.0.0.1", port=5000)
