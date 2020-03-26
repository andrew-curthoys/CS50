import os
from collections import namedtuple

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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
    user_id = session['user_id']
    user_portfolio = db.execute("""SELECT
                                          stock_symbol,
                                          SUM(no_of_shares) as 'no_of_shares'
                                     FROM
                                          transactions
                                    WHERE
                                          user_id = :user_id
                                 GROUP BY
                                          stock_symbol""",
                                user_id=user_id
                                )

    # parse data from SQLite query to lists
    stocks = [row['stock_symbol'] for row in user_portfolio]
    no_of_shares = [row['no_of_shares'] for row in user_portfolio]

    # pull current prices for each stock in the user's portfolio
    prices = [lookup(row)['price'] for row in stocks]

    # total value of holdings
    total_value = [shares * price for shares, price in zip(no_of_shares, prices)]

    # get user's total cash available
    user_info = db.execute("SELECT username, cash FROM users WHERE id = :user_id",
                           user_id=user_id)
    cash_available = user_info[0]['cash']
    username = user_info[0]['username']

    # get user's total worth
    total_worth = cash_available + sum(total_value)

    # create a named tuple to store portfolio data
    Stock_data = namedtuple('Stock_data', 'symbol no_of_shares price total_value')

    # get stock information from the lists above & insert it into a list of named tuples
    table_data = [Stock_data(symbol, no_of_shares, usd(price), usd(total_value))
                  for symbol, no_of_shares, price, total_value in zip(stocks, no_of_shares, prices, total_value)]
    return render_template("table.html", table_data=table_data, username=username, current_cash=usd(cash_available), current_worth=usd(total_worth))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template('buy.html')
    if request.method == "POST":
        # error checking to make sure the user filled out the form completely and correctly
        symbol = request.form.get('symbol')
        if not symbol:
            return apology("Must input a stock symbol", 400)
        try:
            shares = int(request.form.get('shares'))
        except:
            return apology("Must provide a number of shares", 400)
        if not shares:
            return apology("Must provide a number of shares to buy", 400)
        if shares < 0:
            return apology("Must provide a positive number of shares", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("Stock symbol not found", 400)
        price = quote['price']
        total_price = price * shares

        # get user_id
        user_id = session['user_id']

        # query SQLite DB to get the amount of cash in the user's account
        cash_available = db.execute("SELECT cash FROM users WHERE id = :user_id",
                                    user_id=user_id)
        cash_available = cash_available[0]['cash']

        # check if user has enough money in their account
        if total_price > cash_available:
            return apology("Not enough monies!! :(", 400)

        # update amount of cash available for the user
        cash_available = cash_available - total_price

        # update users table with new amount of cash for user
        db.execute("""UPDATE users
                        SET cash = :cash_available
                        WHERE id = :user_id;""",
                   user_id=user_id,
                   cash_available=cash_available)

        # update transactions table with the information from the stock purchase
        db.execute("""INSERT INTO transactions (user_id, stock_symbol, no_of_shares, share_price, total_price, transaction_type)
                    VALUES (:user_id, :stock_symbol, :no_of_shares, :share_price, :total_price, 'PURCHASE')""",
                   user_id=user_id,
                   stock_symbol=symbol,
                   no_of_shares=shares,
                   share_price=price,
                   total_price=total_price)
        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # get requested username
    username_request = request.args.get('username', None)

    user = db.execute("""SELECT
                                username
                           FROM
                                users
                          WHERE
                                username = :username""",
                      username=username_request)

    if not user:
        return jsonify(True)
    return jsonify(False)


@app.route("/history")
@login_required
def history():
    # get current user's user ID
    user_id = session['user_id']

    # get current user's username
    user_info = db.execute("SELECT username FROM users WHERE id = :user_id",
                           user_id=user_id)
    username = user_info[0]['username']

    # query SQLite DB to get transaction data
    user_transactions = db.execute("""SELECT
                                             transaction_type,
                                             stock_symbol,
                                             share_price,
                                             no_of_shares,
                                             datetime
                                        FROM
                                             transactions
                                       WHERE
                                             user_id = :user_id
                                    """,
                                   user_id=user_id)

    # parse data from SQLite query to lists
    transaction_type_list = [row['transaction_type'] for row in user_transactions]
    stock_symbol_list = [row['stock_symbol'] for row in user_transactions]
    share_price_list = [row['share_price'] for row in user_transactions]
    no_of_shares_list = [row['no_of_shares'] for row in user_transactions]
    datetime_list = [row['datetime'] for row in user_transactions]

    # create a named tuple to store portfolio data
    User_transaction_data = namedtuple('User_transaction_data', 'transaction_type stock_symbol share_price no_of_shares datetime')

    # get stock information from the lists above & insert it into a list of named tuples
    history_data = [User_transaction_data(transaction_type, stock_symbol, usd(share_price), no_of_shares, datetime) for transaction_type, stock_symbol,
                    share_price, no_of_shares, datetime in zip(transaction_type_list, stock_symbol_list, share_price_list, no_of_shares_list, datetime_list)]
    return render_template("history.html", history_data=history_data, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    if request.method == "GET":
        return render_template('quote.html')
    if request.method == "POST":
        symbol = request.form.get('symbol')
        if not symbol:
            return apology("Must input a stock symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("Stock symbol not found", 400)
        symbol = quote['symbol']
        company = quote['name']
        price = usd(quote['price'])
        return render_template('quoted.html', symbol=symbol, company=company, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    # error checking to make sure all parts of the form are filled out
    if not username or not password or not confirmation:
        return apology("Please fill in all fields", 400)
    elif password != confirmation:
        return apology("Passwords must match", 400)
    else:
        user = db.execute("""SELECT
                                    username
                               FROM
                                    users
                              WHERE
                                    username = :username""",
                          username=username)

        if not user:
            # Insert user into database
            # first generate a password hash
            hash = generate_password_hash(password)
            db.execute("""INSERT INTO users (username, hash)
                        VALUES (:username, :hash)""",
                       username=username,
                       hash=hash)
            return redirect("/")
        else:
            return apology("Username already exists", 400)


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template('change_password.html')
    # get user ID
    user_id = session['user_id']
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirmation = request.form.get('confirmation')

    # error checking to make sure all parts of the form are filled out
    if not old_password or not new_password or not confirmation:
        return apology("Please fill in all fields", 400)
    elif new_password != confirmation:
        return apology("Passwords must match", 400)
    else:
        # check if old password matches password in DB
        old_password_db = db.execute('SELECT hash FROM users WHERE id = :user_id',
                                     user_id=user_id)
        old_password_db = old_password_db[0]['hash']

        old_password_check = check_password_hash(old_password_db, old_password)

        if not old_password_check:
            return apology("Old password does not match value in DB", 400)

    # Update user's password
    # first generate a password hash
    hash = generate_password_hash(new_password)
    # update users table with new password for user
    db.execute("""UPDATE users
                    SET hash = :hash
                    WHERE id = :user_id;""",
               hash=hash,
               user_id=user_id)
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session['user_id']
        user_portfolio = db.execute("""SELECT
                                              stock_symbol,
                                              SUM(no_of_shares) as 'no_of_shares'
                                         FROM
                                              transactions
                                        WHERE
                                              user_id = :user_id
                                     GROUP BY
                                              stock_symbol""",
                                    user_id=user_id
                                    )

        # parse data from SQLite query to lists
        stock_symbols = [row['stock_symbol'] for row in user_portfolio]

        return render_template('sell.html', stock_symbols=stock_symbols)
    if request.method == "POST":
        # error checking to make sure the user filled out the form completely and correctly
        symbol = request.form.get('symbol')
        if not symbol:
            return apology("Must input a stock symbol", 400)
        try:
            shares = int(request.form.get('shares'))
        except:
            return apology("Must provide a number of shares", 400)
        if not shares:
            return apology("Must provide a number of shares to sell", 400)
        if shares < 0:
            return apology("Must provide a positive number of shares", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("Stock symbol not found", 400)
        price = quote['price']
        total_price = price * shares

        # get user_id
        user_id = session['user_id']

        # query SQLite DB to get the number of shares in the user's account
        shares_available = db.execute("SELECT SUM(no_of_shares) as 'no_of_shares' FROM transactions WHERE user_id = :user_id AND stock_symbol = :symbol",
                                      user_id=user_id,
                                      symbol=symbol
                                      )
        shares_available = shares_available[0]['no_of_shares']

        # check that user has input stock symbol correctly
        if not shares_available:
            return apology("Stock symbol not found in portfolio", 400)

        # check if user has enough shares to sell
        if shares > shares_available:
            return apology("Not enough shares!! :(", 400)

        # update amount of cash available for the user
        cash_available = db.execute("SELECT cash FROM users WHERE id = :user_id",
                                    user_id=user_id
                                    )
        cash_available = cash_available[0]['cash']
        cash_available = cash_available + total_price

        # update users table with new amount of cash for user
        db.execute("""UPDATE users
                        SET cash = :cash_available
                        WHERE id = :user_id;""",
                   user_id=user_id,
                   cash_available=cash_available)

        # update transactions table with the information from the stock sale
        db.execute("""INSERT INTO transactions (user_id, stock_symbol, no_of_shares, share_price, total_price, transaction_type)
                    VALUES (:user_id, :stock_symbol, :no_of_shares, :share_price, :total_price, 'SALE')""",
                   user_id=user_id,
                   stock_symbol=symbol,
                   no_of_shares=-shares,
                   share_price=-price,
                   total_price=-total_price)
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
