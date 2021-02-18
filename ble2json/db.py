import sqlite3
from flask import current_app, g


def dict_factory(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def connect(db_path):
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = dict_factory
    return conn


def get_conn():
    if "conn" not in g:
        g.conn = connect(current_app.config["DB_PATH"])

    return g.conn


def pop_conn(e=None):
    conn = g.pop("conn", None)

    if conn is not None:
        conn.close()


def init(app):
    app.teardown_appcontext(pop_conn)

    with app.app_context():
        conn = get_conn()

        with current_app.open_resource("schema.sql") as f:
            conn.executescript(f.read().decode("utf8"))

        conn.commit()
