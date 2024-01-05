import sqlite3

from flask import Flask, g, render_template, request

app = Flask(__name__)


DATABASE = 'test_db.db'
CITIES = {
    1: "Kyiv",
    2: "Lviv",
    3: "Khmelnitskiy",
    4: "Kharkiv",
    5: "Dnipro",
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_db():
    cr = sqlite3.connect(DATABASE)
    cr.execute("""
        CREATE TABLE IF NOT EXISTS participants
            (name VARCHAR(128), email VARCHAR(128), city INT, order_name VARCHAR(128), phone VARCHAR(32)) 
    """)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        city = request.form.get("city")
        phone = request.form.get("phone")
        order = request.form.get("order")
        cr = get_db()
        cr.execute("""
            INSERT INTO participants (name, email, city, phone, order_name) VALUES (?,?,?,?,?)
        """, (name, email, city, phone, order))
        cr.commit()
        return render_template("index.html")

    else:
        return render_template("join.html", cities=CITIES)


@app.route('/participants/')
def participants():
    cr = get_db().cursor()
    cr.execute("SELECT * FROM participants")
    data = cr.fetchall()
    return render_template("participants.html", participants=data, cities=CITIES)


if __name__ == "__main__":
    create_db()
    app.run()
