import hashlib
import sqlite3
from cryptography.fernet import *



def button_functions(log, pwd):
    pwd = pwd.encode()
    pwd = hashlib.sha256(pwd).hexdigest()
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (log, pwd))
    if cur.fetchall():
        key = cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (log, pwd))
        key = key.fetchall()[0][2]
        conn.commit()
        return str(key)
    else:
        conn.commit()
        return str(0)


def save_account_start(log,pwd):
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    login, password = log, hashlib.sha256(pwd.encode()).hexdigest()
    cur.execute("SELECT username FROM userdata WHERE username = ?", [login, ])
    if cur.fetchall():
        conn.commit()
        return str(0)
    else:
        key = Fernet.generate_key()
        key = key.decode("utf-8")
        cur.execute("INSERT INTO userdata (username, password, key) VALUES (?, ?, ?)", (login, password,key))
        conn.commit()
        return str(1)

def save_pass_in_base(name,pwd,user, key):
    conn = sqlite3.connect("passwordbase.db")
    cur = conn.cursor()
    key2 = key.encode(encoding = 'utf-8')
    f = Fernet(key2)
    token = f.encrypt(bytes(pwd, "utf-8"))  # шифрование данных
    keyfern = Fernet.generate_key()
    keyfern = keyfern.decode("utf-8")
    cur.execute("INSERT INTO passwordbase (name, password, pass_id, pass_key) VALUES (?, ?, ?, ?)",
                (name, token, user, keyfern))
    conn.commit()
    return str(1)

def create_mass(uid,key):
    value_mass = [["NAME", "PASSWORD", "EDIT", "KEY"]]
    conn = sqlite3.connect("passwordbase.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    r = cur.execute("SELECT name, password, pass_key FROM passwordbase WHERE pass_id = ?", (uid,))
    rows = r.fetchall()
    key2 = key.encode(encoding='utf-8')
    f = Fernet(key2)
    result_list = [list(rows1) for rows1 in rows]
    for i in result_list:
        cur_password = f.decrypt(i[1])
        cur_password = cur_password.decode("utf-8")
        cur_name = i[0]
        keyfern = i[2]
        value_mass.append([cur_name, cur_password, "OPTION", keyfern])
    conn.commit()
    return value_mass


def delete_cell_event(pass_key):
    conn = sqlite3.connect("passwordbase.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("DELETE FROM passwordbase WHERE pass_key = ?", (pass_key,))
    conn.commit()
    return "1"

def update_cell_pass_table(pass_key,n_log,n_pass,key):
    conn = sqlite3.connect("passwordbase.db")
    cur = conn.cursor()
    key2 = key.encode(encoding='utf-8')
    f = Fernet(key2)
    new = f.encrypt(bytes(n_pass, "utf-8"))
    cur.execute('UPDATE passwordbase SET name = ?, password = ? WHERE pass_key = ?',
                [n_log, new, pass_key])
    conn.commit()
    return "1"

def refresh_table_event_brain(user_id, key):
    value_mass = [["NAME", "PASSWORD", "EDIT", "key"]]
    conn = sqlite3.connect("passwordbase.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    for r in cur.execute("SELECT * FROM passwordbase"):
        if r["pass_id"] == user_id:
            cur_name = r["name"]
            token = r["password"]
            f = Fernet(key)
            cur_password = f.decrypt(token)
            value_mass.append([cur_name, cur_password, "OPTION"])

    conn.commit()
    return value_mass