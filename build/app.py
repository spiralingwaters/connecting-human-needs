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
    viewer = current_user()
    if viewer is None:
        posts = db.execute(
            "SELECT author_name, body, kind, created_at FROM posts ORDER BY id DESC"
        ).fetchall()
    else:
        posts = db.execute(
            """
            SELECT author_name, body, kind, created_at FROM posts
            WHERE author_id IS NULL OR author_id NOT IN (
                SELECT blocked_id FROM blocks WHERE blocker_id = ?
            )
            ORDER BY id DESC
            """,
            (viewer["id"],),
        ).fetchall()
    return render_template("index.html", tagline=tagline, posts=posts)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    terms = query.split()
    tiers = [[], [], []]
    if terms:
        db = get_db()
        viewer = current_user()
        if viewer is None:
            posts = db.execute(
                "SELECT author_name, body, created_at FROM posts ORDER BY id DESC"
            ).fetchall()
        else:
            posts = db.execute(
                """
                SELECT author_name, body, created_at FROM posts
                WHERE author_id IS NULL OR author_id NOT IN (
                    SELECT blocked_id FROM blocks WHERE blocker_id = ?
                )
                ORDER BY id DESC
                """,
                (viewer["id"],),
            ).fetchall()
        term_count = len(terms)
        for post in posts:
            haystack = (post["author_name"] + " " + post["body"]).lower()
            matched = sum(1 for t in terms if t.lower() in haystack)
            if matched == 0:
                continue
            if matched == term_count:
                tiers[0].append(post)
            elif matched > 1:
                tiers[1].append(post)
            else:
                tiers[2].append(post)
    return render_template(
        "search_results.html",
        query=query,
        all_match=tiers[0],
        some_match=tiers[1],
        one_match=tiers[2],
    )


def find_or_create_thread(db, user_a_id, user_b_id):
    thread = db.execute(
        """
        SELECT id FROM message_threads
        WHERE (user_a_id = ? AND user_b_id = ?)
           OR (user_a_id = ? AND user_b_id = ?)
        """,
        (user_a_id, user_b_id, user_b_id, user_a_id),
    ).fetchone()
    if thread is not None:
        return thread["id"]
    is_bot_thread = db.execute(
        "SELECT 1 FROM users WHERE id IN (?, ?) AND is_bot = 1",
        (user_a_id, user_b_id),
    ).fetchone()
    cur = db.execute(
        "INSERT INTO message_threads (user_a_id, user_b_id, is_bot_thread) VALUES (?, ?, ?)",
        (user_a_id, user_b_id, 1 if is_bot_thread else 0),
    )
    return cur.lastrowid


def thread_other_user(thread, my_id):
    return thread["user_b_id"] if thread["user_a_id"] == my_id else thread["user_a_id"]


@app.route("/messages")
def messages():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    threads = db.execute(
        """
        SELECT message_threads.id, message_threads.user_a_id, message_threads.user_b_id,
               message_threads.is_bot_thread
        FROM message_threads
        WHERE user_a_id = ? OR user_b_id = ?
        ORDER BY id DESC
        """,
        (user["id"], user["id"]),
    ).fetchall()
    people = []
    bots = []
    for t in threads:
        other_id = thread_other_user(t, user["id"])
        other = db.execute(
            "SELECT username FROM users WHERE id = ?", (other_id,)
        ).fetchone()
        entry = {"id": t["id"], "other_username": other["username"] if other else "?"}
        (bots if t["is_bot_thread"] else people).append(entry)
    return render_template("messages.html", people=people, bots=bots)


@app.route("/messages/new", methods=["GET", "POST"])
def new_thread():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        db = get_db()
        other = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if other is None:
            return render_template("new_thread.html", error="No user with that username.")
        thread_id = find_or_create_thread(db, user["id"], other["id"])
        db.commit()
        return redirect(url_for("thread", thread_id=thread_id))
    return render_template("new_thread.html")


@app.route("/messages/<int:thread_id>", methods=["GET", "POST"])
def thread(thread_id):
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    t = db.execute(
        "SELECT * FROM message_threads WHERE id = ?", (thread_id,)
    ).fetchone()
    if t is None or user["id"] not in (t["user_a_id"], t["user_b_id"]):
        return redirect(url_for("messages"))
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            db.execute(
                "INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
                (thread_id, user["id"], body),
            )
            db.commit()
        return redirect(url_for("thread", thread_id=thread_id))
    other_id = thread_other_user(t, user["id"])
    other = db.execute("SELECT username FROM users WHERE id = ?", (other_id,)).fetchone()
    block = db.execute(
        "SELECT created_at FROM blocks WHERE blocker_id = ? AND blocked_id = ?",
        (user["id"], other_id),
    ).fetchone()
    if block is None:
        history = db.execute(
            """
            SELECT messages.body, messages.created_at, users.username AS sender
            FROM messages JOIN users ON users.id = messages.sender_id
            WHERE thread_id = ? ORDER BY messages.id ASC
            """,
            (thread_id,),
        ).fetchall()
    else:
        history = db.execute(
            """
            SELECT messages.body, messages.created_at, users.username AS sender
            FROM messages JOIN users ON users.id = messages.sender_id
            WHERE thread_id = ?
              AND (messages.sender_id != ? OR messages.created_at <= ?)
            ORDER BY messages.id ASC
            """,
            (thread_id, other_id, block["created_at"]),
        ).fetchall()
    return render_template(
        "thread.html", thread_id=thread_id, other_username=other["username"], history=history
    )


def is_blocked_by_viewer(db, viewer_id, other_id):
    if viewer_id is None:
        return False
    row = db.execute(
        "SELECT 1 FROM blocks WHERE blocker_id = ? AND blocked_id = ?",
        (viewer_id, other_id),
    ).fetchone()
    return row is not None


@app.route("/u/<username>")
def profile(username):
    db = get_db()
    user = db.execute(
        "SELECT id, username, is_bot FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user is None:
        return render_template("profile.html", profile_user=None, username=username)
    viewer = current_user()
    blocked = is_blocked_by_viewer(db, viewer["id"] if viewer else None, user["id"])
    if blocked:
        gift_wall = []
        own_posts = []
    else:
        gift_wall = db.execute(
            """
            SELECT title, redeemed_at FROM gift_notes
            WHERE original_author_id = ? AND redeemed_at IS NOT NULL
            ORDER BY redeemed_at DESC
            """,
            (user["id"],),
        ).fetchall()
        own_posts = db.execute(
            """
            SELECT body, created_at FROM posts
            WHERE author_id = ? AND kind = 'post'
            ORDER BY id DESC
            """,
            (user["id"],),
        ).fetchall()
    can_block = viewer is not None and viewer["id"] != user["id"]
    return render_template(
        "profile.html",
        profile_user=user,
        gift_wall=gift_wall,
        own_posts=own_posts,
        can_block=can_block,
        blocked=blocked,
    )


@app.route("/u/<username>/block", methods=["POST"])
def block_user(username):
    viewer = current_user()
    if viewer is None:
        return redirect(url_for("login"))
    db = get_db()
    target = db.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if target is not None and target["id"] != viewer["id"]:
        db.execute(
            "INSERT OR IGNORE INTO blocks (blocker_id, blocked_id) VALUES (?, ?)",
            (viewer["id"], target["id"]),
        )
        db.commit()
    return redirect(url_for("profile", username=username))


@app.route("/u/<username>/unblock", methods=["POST"])
def unblock_user(username):
    viewer = current_user()
    if viewer is None:
        return redirect(url_for("login"))
    db = get_db()
    target = db.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if target is not None:
        db.execute(
            "DELETE FROM blocks WHERE blocker_id = ? AND blocked_id = ?",
            (viewer["id"], target["id"]),
        )
        db.commit()
    return redirect(url_for("profile", username=username))


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


@app.route("/notes")
def notes():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    held = db.execute(
        """
        SELECT gift_notes.id, gift_notes.title, gift_notes.description,
               gift_notes.contact_info, gift_notes.expires_at,
               users.username AS original_author
        FROM gift_notes
        JOIN users ON users.id = gift_notes.original_author_id
        WHERE gift_notes.current_holder_id = ?
          AND gift_notes.redeemed_at IS NULL
          AND gift_notes.expires_at > strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
        ORDER BY gift_notes.id DESC
        """,
        (user["id"],),
    ).fetchall()
    sent_expired = db.execute(
        """
        SELECT gift_notes.id, gift_notes.title
        FROM gift_notes
        WHERE gift_notes.original_author_id = ?
          AND gift_notes.redeemed_at IS NULL
          AND gift_notes.expires_at <= strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
        ORDER BY gift_notes.id DESC
        """,
        (user["id"],),
    ).fetchall()
    return render_template("notes.html", held=held, sent_expired=sent_expired)


def _note_owned_by(db, note_id, user_id):
    return db.execute(
        "SELECT * FROM gift_notes WHERE id = ? AND current_holder_id = ?"
        " AND redeemed_at IS NULL",
        (note_id, user_id),
    ).fetchone()


@app.route("/notes/<int:note_id>/pass", methods=["POST"])
def pass_note(note_id):
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    note = _note_owned_by(db, note_id, user["id"])
    if note is None:
        return redirect(url_for("notes"))
    recipient_username = request.form.get("recipient", "").strip()
    recipient = db.execute(
        "SELECT id FROM users WHERE username = ?", (recipient_username,)
    ).fetchone()
    if recipient is not None:
        db.execute(
            "UPDATE gift_notes SET current_holder_id = ? WHERE id = ?",
            (recipient["id"], note_id),
        )
        thread_id = find_or_create_thread(db, user["id"], recipient["id"])
        db.execute(
            "INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
            (thread_id, user["id"], f'Passed you a gift note: "{note["title"]}"'),
        )
        db.commit()
    return redirect(url_for("notes"))


@app.route("/notes/<int:note_id>/redeem", methods=["POST"])
def redeem_note(note_id):
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    note = _note_owned_by(db, note_id, user["id"])
    if note is None:
        return redirect(url_for("notes"))
    author = db.execute(
        "SELECT username FROM users WHERE id = ?", (note["original_author_id"],)
    ).fetchone()
    db.execute(
        "UPDATE gift_notes SET redeemed_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        (note_id,),
    )
    db.execute(
        "INSERT INTO posts (author_name, author_id, body, kind) VALUES (?, ?, ?, 'redemption')",
        (author["username"], note["original_author_id"], note["title"]),
    )
    db.execute(
        "INSERT INTO notifications (user_id, message) VALUES (?, ?)",
        (
            note["original_author_id"],
            f'Your gift note "{note["title"]}" was redeemed by {user["username"]}.',
        ),
    )
    db.commit()
    return redirect(url_for("notes"))


@app.route("/notes/<int:note_id>/renew", methods=["POST"])
def renew_note(note_id):
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    note = db.execute(
        """
        SELECT * FROM gift_notes
        WHERE id = ? AND original_author_id = ? AND redeemed_at IS NULL
          AND expires_at <= strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
        """,
        (note_id, user["id"]),
    ).fetchone()
    if note is None:
        return redirect(url_for("notes"))
    recipient_username = request.form.get("recipient", "").strip()
    recipient = db.execute(
        "SELECT id FROM users WHERE username = ?", (recipient_username,)
    ).fetchone()
    if recipient is not None:
        db.execute(
            """
            INSERT INTO gift_notes
                (title, description, contact_info, original_author_id,
                 current_holder_id, expires_at)
            VALUES (?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '+30 days'))
            """,
            (
                note["title"],
                note["description"],
                note["contact_info"],
                user["id"],
                recipient["id"],
            ),
        )
        db.commit()
    return redirect(url_for("notes"))


@app.route("/notifications")
def notifications():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    items = db.execute(
        "SELECT message, created_at FROM notifications WHERE user_id = ? ORDER BY id DESC",
        (user["id"],),
    ).fetchall()
    db.execute(
        "UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user["id"],)
    )
    db.commit()
    return render_template("notifications.html", items=items)


def unread_notification_count():
    user = current_user()
    if user is None:
        return 0
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) AS n FROM notifications WHERE user_id = ? AND is_read = 0",
        (user["id"],),
    ).fetchone()
    return row["n"]


@app.context_processor
def inject_unread_count():
    return {"unread_notifications": unread_notification_count()}


@app.route("/notes/new", methods=["GET", "POST"])
def new_note():
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        contact_info = request.form.get("contact_info", "").strip()
        recipient_username = request.form.get("recipient", "").strip()
        if not (title and description and contact_info and recipient_username):
            return render_template("new_note.html", error="Fill in every field.")
        db = get_db()
        recipient = db.execute(
            "SELECT id FROM users WHERE username = ?", (recipient_username,)
        ).fetchone()
        if recipient is None:
            return render_template(
                "new_note.html", error="No user with that username."
            )
        db.execute(
            """
            INSERT INTO gift_notes
                (title, description, contact_info, original_author_id,
                 current_holder_id, expires_at)
            VALUES (?, ?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '+30 days'))
            """,
            (title, description, contact_info, user["id"], recipient["id"]),
        )
        thread_id = find_or_create_thread(db, user["id"], recipient["id"])
        db.execute(
            "INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
            (thread_id, user["id"], f'Sent you a gift note: "{title}"'),
        )
        db.commit()
        return redirect(url_for("notes"))
    return render_template("new_note.html")


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
