#!/usr/bin/env python3
"""Privacy-invariant regression tests for the bot framework.

Guards the Mission.md hard privacy rules that Fact extraction, Overlap
engine, and Coordinator bots all depend on: bots only ever read bot
threads, and a bot-authored message never repeats anything about one
person to another beyond a self-stated offer and a username.

Run: python3 build/test_privacy.py
"""
import base64
import io
import os
import re
import shutil
import sqlite3
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as appmod


def make_client(tmpdir, tag):
    appmod.DB_PATH = os.path.join(tmpdir, f"site-{tag}.db")
    appmod.SECRET_KEY_PATH = os.path.join(tmpdir, f"secret-{tag}")
    appmod.app.secret_key = "test-secret"
    appmod.init_db()
    return appmod.app.test_client()


def fake_id_png(seed_text):
    """A tiny unique PNG standing in for a real hand-drawn ID, so each
    test user gets a distinct image_hash."""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (16, 16), "white")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), seed_text[:2], fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def signup_and_login(client, username):
    """Signs up via the real PNG-based /signup flow, then logs in for
    real via /login by re-uploading the same PNG bytes."""
    png_data_url = fake_id_png(username)
    client.post("/signup", data={"username": username, "image_data": png_data_url})
    png_bytes = base64.b64decode(png_data_url.split(",", 1)[1])
    client.post(
        "/login",
        data={"id_png": (io.BytesIO(png_bytes), "my-id.png")},
        content_type="multipart/form-data",
    )


def bot_thread_id(client):
    r = client.get("/messages")
    return re.search(r"/messages/(\d+)", r.get_data(as_text=True)).group(1)


def test_assert_bot_thread_raises_on_human_thread():
    tmpdir = tempfile.mkdtemp()
    try:
        carol = make_client(tmpdir, "assert")
        signup_and_login(carol, "carol")
        dave = appmod.app.test_client()
        signup_and_login(dave, "dave")
        carol.post("/messages/new", data={"username": "dave"})
        import sqlite3

        db = sqlite3.connect(appmod.DB_PATH)
        db.row_factory = sqlite3.Row
        t = db.execute(
            "SELECT * FROM message_threads WHERE is_bot_thread = 0"
        ).fetchone()
        db.close()
        try:
            appmod.assert_bot_thread(t)
        except appmod.BotPrivacyViolation:
            pass
        else:
            raise AssertionError("assert_bot_thread did not raise on a human thread")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_facts_never_extracted_from_human_thread():
    tmpdir = tempfile.mkdtemp()
    try:
        carol = make_client(tmpdir, "facts")
        signup_and_login(carol, "carol")
        dave = appmod.app.test_client()
        signup_and_login(dave, "dave")
        r = carol.post("/messages/new", data={"username": "dave"}, follow_redirects=True)
        thread_id = r.request.path.split("/")[-1]
        # Bot-looking phrasing sent in a human-to-human thread.
        carol.post(
            f"/messages/{thread_id}",
            data={"body": "I have a couch to give away, I'm in Portland, reach me at foo@example.com"},
        )
        import sqlite3

        db = sqlite3.connect(appmod.DB_PATH)
        db.row_factory = sqlite3.Row
        count = db.execute("SELECT COUNT(*) c FROM user_facts").fetchone()["c"]
        db.close()
        assert count == 0, f"expected no facts from a human-to-human thread, got {count}"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_coordinator_notice_leaks_nothing_extra():
    tmpdir = tempfile.mkdtemp()
    try:
        carol = make_client(tmpdir, "coord")
        signup_and_login(carol, "carol")
        dave = appmod.app.test_client()
        signup_and_login(dave, "dave")

        dave.post(f"/messages/{bot_thread_id(dave)}", data={"body": "I have a couch to give away"})
        ct = bot_thread_id(carol)
        carol.post(
            f"/messages/{ct}",
            data={"body": "I need a couch for my apartment, I'm in Seattle, reach me at carol@example.com"},
        )
        r = carol.get(f"/messages/{ct}")
        text = r.get_data(as_text=True)
        # The coordinator notice must name the offer + dave's username...
        assert "couch to give away" in text
        assert "@dave" in text
        # ...but a bot must never surface one person's private facts
        # inside a message routed to someone else. Dave never stated a
        # city or contact info as part of his offer, so neither should
        # ever appear anywhere in carol's thread with the bot.
        assert "dave@example.com" not in text
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    tests = [
        test_assert_bot_thread_raises_on_human_thread,
        test_facts_never_extracted_from_human_thread,
        test_coordinator_notice_leaks_nothing_extra,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print("ALL PRIVACY TESTS PASSED")


if __name__ == "__main__":
    main()
