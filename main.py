from flask import Flask, request
from brain import *
import sqlite3
from password import create_new

app = Flask(__name__)
conn = sqlite3.connect("userdata.db")
cur = conn.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS userdata(
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            key TEXT NOT NULL
        )
        """)
conn.commit()
conn = sqlite3.connect("passwordbase.db")
cur = conn.cursor()
cur.execute("""
                CREATE TABLE IF NOT EXISTS passwordbase(
                    id integer primary key autoincrement, 
                    name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    pass_id VARCHAR(255) NOT NULL,
                    pass_key TEXT NOT NULL
                )
                """)
conn.commit()

@app.route("/")
def index():
    return "Home"
@app.route("/create_pass_mass")
def create_pass_mass():
    uid = request.args.get("uid", default="", type=str)
    key = request.args.get("key", default="", type=str)
    return create_mass(uid,key)

@app.route("/delete_cell")
def delete_cell():
    pass_key = request.args.get("pass_key", default="", type=str)

    return delete_cell_event(pass_key)

@app.route("/update_pass_cell")
def update_pass_cell():
    o_pass = request.args.get("pass_key", default="", type=str)
    n_log = request.args.get("new_log", default="", type=str)
    n_pass = request.args.get("new_pass", default="", type=str)
    key = request.args.get("key_up", type=str)

    return update_cell_pass_table(o_pass,n_log,n_pass,key)

@app.route("/refresh_table")
def refresh_table_event():
    uid_refresh = request.args.get("uid_refresh", default="", type=str)
    key = request.args.get("key", default="", type="")
    return create_mass(uid_refresh, key)

@app.route("/need_password")
def create_pass():
    length = request.args.get("length", default="", type=int)
    characters = request.args.get("characters", default='', type=str)
    new_password = create_new(length,characters)
    return str(new_password)

@app.route("/save_pass_in_base")
def save_pwd():
    name = request.args.get("password_name", default="", type=str)
    pwd = request.args.get("new_password", default='', type=str)
    user = request.args.get("user_id", default='', type=str)
    key = request.args.get("key", default="",type=str)
    return save_pass_in_base(name,pwd,user,key)

@app.route("/save_account")
def save_account(): 
    log = request.args.get("save_login", default="", type=str)
    pwd = request.args.get("save_password", default="", type=str)
    return save_account_start(log,pwd)

@app.route("/login")
def login():
    log = request.args.get("Login", default="", type=str)
    pwd = request.args.get("Password", default="", type=str)
    return button_functions(log,pwd)

@app.route("/table")
def get_table():

    return {'login1':"pass1", }

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')