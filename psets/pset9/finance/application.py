import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    quotes = db.execute("SELECT * FROM quotes WHERE user=?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    for i in range(len(quotes)):
        quotes[i]["price"] = lookup(quotes[i]["symbol"])["price"]
        quotes[i]["symbol"] = quotes[i]["symbol"].upper()
        quotes[i]["name"] = lookup(quotes[i]["symbol"])["name"]
    return render_template("index.html", cash=cash, quotes=quotes)
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if symbol == "":
            return apology("Missing symbol")

        symbol = symbol.upper()

        if shares == "":
            return apology("Missing shares")

        if lookup(symbol) == None:
            return apology("Invalid symbol")

        cost = int(shares) * lookup(symbol)["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        if cash < cost:
            return apology("Can't afford")

        db.execute("UPDATE users SET cash=? WHERE id=?", cash - cost, session["user_id"])

        sharesindb = db.execute("SELECT shares FROM quotes WHERE user=? AND symbol=?", session["user_id"], symbol)
        if len(sharesindb) != 0:
            db.execute("UPDATE quotes SET shares=? WHERE user=? AND symbol=?",
                       sharesindb[0]["shares"] + int(shares), session["user_id"], symbol)
        else:
            db.execute("INSERT INTO quotes (user, symbol, shares) VALUES (?, ?, ?)", session["user_id"], symbol, shares)
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, shares, lookup(symbol)["price"])
    else:
        return render_template("buy.html")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE id=?", session["user_id"])
    return render_template("history.html", history=history)
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quoteinfo = lookup(request.form.get("symbol"))
        if not quoteinfo == None:
            quote = quoteinfo['symbol']
            price = quoteinfo['price']
            name = quoteinfo['name']
            return render_template("quoted.html", quote=quote, price=price, name=name)
        else:
            return apology("Invalid symbol")
    else:
        return render_template("quote.html")
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        psw = request.form.get("password")
        conf = request.form.get("confirmation")

        if username == "":
            return apology("Missing username")

        if psw == "123456" or psw == "qwerty" or psw == "123456789" or psw == "password" or psw == "12345678" or psw == "1234567" or psw == "12345" or psw == "iloveyou" or psw == "111111" or psw == "123123":
            return apology("Password is not secure")

        if psw == conf:
            check_username = db.execute("SELECT username FROM users WHERE username=?", username)
            if len(check_username) == 0:
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(psw))
            else:
                return apology("Username is not available")
        else:
            return apology("Passwords don't match")
    else:
        return render_template("register.html")
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if symbol is None:
            return apology("Missing symbol")
        if shares == "":
            return apology("Missing shares")

        # if type(shares) != int or shares < 1:
        # return apology("Invalid shares")

        shares = int(shares)
        symbol = symbol.upper()

        haveshares = db.execute("SELECT * FROM quotes WHERE user=? AND symbol=?", session["user_id"], symbol)[0]["shares"]
        if haveshares < shares:
            return apology("Too many shares")
        cost = round(lookup(symbol)["price"] * shares, 2)
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        if haveshares == shares:
            db.execute("DELETE FROM quotes WHERE user=? AND symbol=?", session["user_id"], symbol)
            db.execute("UPDATE users SET cash=? WHERE id=?", cash + cost, session["user_id"])

        sharesindb = db.execute("SELECT shares FROM quotes WHERE user=? AND symbol=?", session["user_id"], symbol)
        db.execute("UPDATE quotes SET shares=? WHERE user=? AND symbol=?", haveshares - shares, session["user_id"], symbol)
        db.execute("UPDATE users SET cash=? WHERE id=?", cash + cost, session["user_id"])
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, 0 - shares, lookup(symbol)["price"])
    else:
        quotes = db.execute("SELECT * FROM quotes WHERE user=?", session["user_id"])
        return render_template("sell.html", quotes=quotes)
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
