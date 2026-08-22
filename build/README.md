# Running

```
pip install -r requirements.txt
python app.py
```

Serves on `127.0.0.1:5000`. First run auto-creates `db/site.db` from `db/schema.sql` + `db/seed.sql`.

# Behind nginx

This is a plain Flask dev server for now — fine locally, but for real deployment run it under a WSGI server (e.g. `gunicorn app:app`) bound to a local port, and reverse-proxy it from nginx:

```
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Static files (`/static/*`) can also be served directly by nginx instead of Flask once there's a real deploy, but that's an optimization, not a requirement.
