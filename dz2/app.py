from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title = "index")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title = "Контакти")


@app.route('/about')
def about():
    return render_template("about.html", title = "Про нас")


if __name__ == '__main__':
    app.run(debug=True)
