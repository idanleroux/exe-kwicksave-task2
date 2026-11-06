import flask
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = flask.Flask(__name__)
app.secret_key = "dev-secret-key" # Change when added to production

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create users table
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if flask.request.method == "POST":

        username = flask.request.form["username"]
        password = flask.request.form["password"]

        with get_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):

            flask.session["user_id"] = user["id"]

            return flask.redirect("/dashboard")

        return "Invalid username or password"

    return flask.render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if flask.request.method == "POST":

        username = flask.request.form["username"]
        password = flask.request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            with get_db() as db:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password)
                )

            return flask.redirect("/login")

        except sqlite3.IntegrityError:
            return "Username already exists"

    return flask.render_template("signup.html")


@app.route("/search")
def search():
    return flask.render_template("search.html")

@app.route("/admin")
def admin():
    return flask.render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)