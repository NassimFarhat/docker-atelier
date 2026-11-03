import os

import pymysql
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Docker avec Flask!"


@app.route("/health")
def health():
    return "OK"


@app.route("/db")
def db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "mysql"),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "flaskapp"),
            connect_timeout=3,
        )
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
        conn.close()
        return f"MySQL connecté, version {version}"
    except Exception as exc:
        return f"Erreur MySQL : {exc}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")