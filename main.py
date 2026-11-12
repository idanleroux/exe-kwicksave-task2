import flask
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = flask.Flask(__name__)
app.secret_key = "dev-secret-key" # Change when added to production

def get_user_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_product_db():
    conn = sqlite3.connect("product.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create users table
with get_user_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

# Create product table
with get_product_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE NOT NULL,
            price INT NOT NULL
        )
    """)

def get_product():
    prod_lst = sqlite3.connect("product.db")
    db.execute("""
        SELECT * FROM product
        """)
    return prod_lst


@app.route("/")
def index():
    products = get_product()
    return flask.render_template("index.html", products=products)
    print(products)

@app.route("/login", methods=["GET", "POST"])
def login():

    if flask.request.method == "POST":

        email = flask.request.form["email"]
        password = flask.request.form["password"]

        with get_user_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):

            flask.session["user_id"] = user["id"]

            return flask.redirect("/")

        return "Invalid email or password"
    print("login working")
    return flask.render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if flask.request.method == "POST":

        email = flask.request.form["email"]
        password = flask.request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            with get_user_db() as db:
                db.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hashed_password)
                )

            return flask.redirect("/login")

        except sqlite3.IntegrityError:
            return "email already exists"
    print("signup working")
    return flask.render_template("signup.html")


@app.route("/search")
def search():
    return flask.render_template("search.html")

@app.route("/admin")
def admin():
    return flask.render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)