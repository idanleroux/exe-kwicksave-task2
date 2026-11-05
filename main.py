import flask

app = flask.Flask(__name__)
@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/login")
def login():
    return flask.render_template('login.html')

@app.route("/search")
def search():
    return flask.render_template('search.html')

@app.route("/admin")
def admin():
    return flask.render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)