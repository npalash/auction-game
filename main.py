from flask_socketio import SocketIO, join_room, leave_room
from flask import Flask, render_template
import mysql.connector as sql 
import string, random 
import pandas as pd

app = Flask(__name__)
io = SocketIO(app)
root = sql.connect(host='localhost', passwd='onep', user='root', database='testing')
cur = root.cursor() 

def gen_code(length):
    characters = string.ascii_letters + string.digits 
    code = random.choices(characters, k=length)
    return "".join(code)

@app.route("/")
def home():
    sq = pd.read_sql_query('select * from info where TYPE = "public"', con=root)
    
    auctions_data = []
    
    for i in range(0, len(sq)):
        auctions_data.append({"item": sq.loc[i, 'ITEM'], "starter": sq.loc[i, 'USERNAME'], "price":format(sq.loc[i, 'PRICE'], ","), "code": sq.loc[i, 'CODE']})
    return render_template("index.html", auctions=auctions_data)

@app.route("/create_auction")
def create_auction():
    return render_template("index.html")

@io.on("create")
def createe(data):
    name = data["username"]
    code = data["code"]
    price = data["price"]
    type_ = data["type"]
    item = data["item"]
    idd = random.randrange(100000000, 999999999)
    cur.execute(f'INSERT INTO info VALUES ({idd}, "{code}", "{name}", "{item}", "{type_}", "{price}");')
    join_room(code)
    root.commit()

@io.on("join")
def join(data):
    join_room(data["code"])

@app.route("/aucroom/<code>")
def chatroom(code):
    sq = pd.read_sql_query('select * from info where TYPE = "public"', con=root) 
    starter = sq.loc[sq['CODE'] == code, 'USERNAME'].iloc[0]
    item = sq.loc[sq['CODE'] == code, 'ITEM'].iloc[0]
    return render_template("aucroom.html", title=item, starter=starter)

@io.on("send_message")
def handle_message(data):
    code = data["code"]
    msg = data["msg"]
    username = data["username"]
    io.emit("receive_message", {"msg": msg, "username": username}, room=code)

@io.on("leave")
def leave(data):
    leave_room(data["code"])

if __name__ == "__main__":
    io.run(app, port=5000, debug=True, allow_unsafe_werkzeug=True)
