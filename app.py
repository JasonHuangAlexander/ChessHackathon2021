from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    session,
    abort,
)
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
    UserMixin,
)
import json
import os
import logging
import engines


# logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_url_path="/static")
app.config["SECRET_KEY"] = os.urandom(16)
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
# also need hard reload (ctrl + shift + R) in chrome browser to reload static files
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# flask_login by default redirects using 'http', which will result in errors like:
# This request has been blocked; the content must be served over HTTPS.
# https://stackoverflow.com/questions/14810795/flask-url-for-generating-http-url-instead-of-https
# fix this by setting the preferred url scheme to 'https'
app.config["PREFERRED_URL_SCHEME"] = "https"

app.logger.debug("start app server")
# app.logger.debug(app.config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    app.logger.debug("load_user - user_id: " + user_id)
    return User


# We're just going to have one anonymous user for now. The password is looked up
# from the os environment, which is set as a webapp setting on Azure.

class User(UserMixin):
    id = "anonymous"
    name = "anonymous"
    password = os.environ.get("APP_KEY")

@app.route("/")
@login_required
def home():
    app.logger.debug("home")
    map_key = os.environ.get("MAP_KEY")
    polling_interval = int(os.environ.get("POLLING_INTERVAL", 10000))
    return render_template("index.html", map_key=map_key, polling_interval=polling_interval)


@app.route("/login")
def login():
    app.logger.debug("login")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    app.logger.debug("login_post")

    password = request.form["password"]
    user = User()

    if user.password == password:
        login_user(user, remember=False)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    app.logger.debug("logout")
    logout_user()
    return render_template("login.html")


@app.route("/make_move", methods=["POST"])
@login_required
def make_move():
    app.logger.debug("make_move")

    params_json = request.get_json(force=True)
    board = str(params_json["board"])
    algo = str(params_json["algo"])
    app.logger.debug("board: " + board + ", algo: " + algo)

    fen = engines.make_move(board, algo)
    app.logger.debug("fen: " + fen)
    board = {"fen": fen}
    return json.dumps(board)


if __name__ == "__main__":
    app.logger.debug("main")
    app.run(debug=True, host="0.0.0.0", port=4000)