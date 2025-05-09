# user_db.py
# [Modul SQLite untuk user, saldo, transaksi]
import bcrypt
import json
import sqlite3
import numpy as np
import os
import pandas as pd
from datetime import datetime

EMB_FILE = "embeddings_db.npy"
USER_FILE = "users.json"
DB_FILE = "facepay.db"

def register_user(name, embedding, pin, image):
    users = load_json()
    uid = f"user_{len(users)+1}"
    pin_hash = bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()
    users[uid] = {"name": name, "saldo": 0, "pin": pin_hash, "failed": 0}
    save_json(users)
    embs = load_embeddings()
    embs.append(embedding)
    np.save(EMB_FILE, np.array(embs))
    cv2.imwrite(f"assets/{uid}.jpg", image)

def topup_saldo(name, amount):
    users = load_json()
    for uid, data in users.items():
        if data["name"] == name:
            data["saldo"] += int(amount)
    save_json(users)
    log_action(name, "Top Up", amount)

def process_payment(name):
    users = load_json()
    for uid, data in users.items():
        if data["name"] == name and data["saldo"] >= 1000:
            data["saldo"] -= 1000
            save_json(users)
            log_action(name, "Bayar", -1000)
            return True
    return False

def identify_user(embedding):
    embs = load_embeddings()
    users = load_json()
    min_dist = float("inf")
    min_uid = None
    for i, emb in enumerate(embs):
        dist = np.linalg.norm(embedding - emb)
        if dist < min_dist:
            min_dist = dist
            min_uid = list(users.keys())[i]
    if min_dist < 0.9:
        return users[min_uid]["name"], min_dist
    return None, None

def validate_pin(name, pin):
    users = load_json()
    for uid, data in users.items():
        if data["name"] == name:
            if data["failed"] >= 3:
                return "locked"
            if bcrypt.checkpw(pin.encode(), data["pin"].encode()):
                data["failed"] = 0
                save_json(users)
                return "valid"
            else:
                data["failed"] += 1
                save_json(users)
                return "invalid"
    return "notfound"

def reset_pin(name, new_pin):
    users = load_json()
    for uid, data in users.items():
        if data["name"] == name:
            data["pin"] = bcrypt.hashpw(new_pin.encode(), bcrypt.gensalt()).decode()
            data["failed"] = 0
            save_json(users)

def load_users():
    users = load_json()
    return pd.DataFrame([{"UID": k, **v} for k,v in users.items()])

def log_action(user, action, amount):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO log (user, action, amount, timestamp) VALUES (?, ?, ?, ?)",
              (user, action, amount, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_login(admin):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO login_log (user, timestamp) VALUES (?, ?)",
              (admin, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_logs():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM log", conn)
    conn.close()
    return df

def auth_admin(uname, pwd):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM admin WHERE username=?", (uname,))
    row = c.fetchone()
    if row and bcrypt.checkpw(pwd.encode(), row[0].encode()):
        return True
    return False

def load_json():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_json(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_embeddings():
    return list(np.load(EMB_FILE))
