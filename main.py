from flask_socketio import SocketIO, join_room
from flask import Flask, render_template, request, session, redirect  
import mysql.connector as sql 
import string, random 
import pandas as pd
from data import Storage

app = Flask(__name__)
io = SocketIO(app)
root = sql.connect(host='localhost', passwd='onep', user='root', database='auction')
cur = root.cursor() 
store = Storage()

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
#     name = request.form.get("name")
#     type_ = request.form.get("visibility")
#     item = request.form.get("item")
#     starting_price = request.form.get("starting_price")
#     code = gen_code(7)
#     id = random.randint(10000, 99999)

    # sql_cmd = f'INSERT INTO info VALUES ({id}, "{code}", "{name}", "{item}", "{type_}", "{starting_price}")'
    # cur.execute(sql_cmd)
    # root.commit() 

    return render_template("index.html")

@io.on("create")
def createe(data):
    name = data["username"]
    code = data["code"]
    price = data["price"]
    type_ = data["type"]
    item = data["item"]

    # session.setdefault(code, {})
    # session[code]["names"] = []
    # session[code]["starter"] = name

    # print(session)

    data = store.addCode(code)
    store.addInfo(code, name,item, type_, price)

# @io.on("join")
# def join(data):
#     name = data["username"]
#     code = data["code"]

#     join_room(code)

#     session[code]["starter"]
#     session[code]["name"].append(name) 

@app.route("/aucroom/<code>")
def chatroom(code):
    info = store.getInfo(code)
    return render_template("aucroom.html", title=info["item"], starter=info["name"], members=info["names"])

if __name__ == "__main__":
    io.run(app, port=8000, debug=True, allow_unsafe_werkzeug=True)
