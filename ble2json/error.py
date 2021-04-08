from time import time
from flask import abort, jsonify
from ble2json import db


def log(code, name, desc):
    conn = db.get_conn()    
    conn.execute("INSERT INTO error VALUES (?, ?, ?, ?)", (int(time()), code, name, desc))
    conn.commit()
    

def log_no_context(db_path, code, name, desc):
    conn = db.connect(db_path)    
    conn.execute("INSERT INTO error VALUES (?, ?, ?, ?)", (int(time()), code, name, desc))
    conn.commit()
    conn.close()


def get_all():
    conn = db.get_conn()
    return conn.execute("""SELECT
                           strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
                           code,
                           name,
                           description
                           FROM error""").fetchall()
                           

def check():
    errors = get_all()
    
    if errors:
        res = jsonify(errors)
        res.status_code = 500
        abort(res)

