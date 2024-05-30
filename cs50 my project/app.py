import os
import pandas as pd
import plotly.graph_objects as go

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from plotly.offline import plot

from helpers import apology, login_required, lookup, usd
from sollow import ss_capital_per_worker, ss_output_per_worker, get_sollowdf


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite growth database
db = SQL("sqlite:///growth.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if request.method == "GET":

        return render_template("index.html")

    else:
        apology("TODO")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Require
    name = request.form.get("username")
    password = request.form.get("password")
    check = request.form.get("confirmation")
    var = "/register"

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        # Ensure username was submitted
        if not name:
            return apology("must provide username")

    # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        elif password != check:
            return apology("the password don't match. Check it.")

        dbName = db.execute("SELECT username FROM users WHERE username=?", name)

        if not dbName:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                       name, generate_password_hash(password))
            flash("You are register sucessufuly!")
            return render_template("login.html")

        else:
            return apology("this name already exist, choose another")


@app.route("/growth", methods=["GET"])
@login_required
def growth():

        return render_template("growth.html")


@app.route("/pwt", methods=["GET", "POST"])
@login_required
def pwt():

    if request.method == "GET":
    # Execute a consulta para obter os dados
        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        countries = set()
        for row  in data:
            countries.add(row['country'])
        sorted_countries = sorted(list(countries))
        return render_template("pwt.html",data=data,countries=sorted_countries)


    if request.method == "POST":

        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        countries = set()
        for row  in data:
            countries.add(row['country'])

        sorted_countries = sorted(list(countries))

        country = request.form.get('countries')
        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id WHERE country=?', country)

        return render_template("pwt.html", data=data, countries=sorted_countries)

@app.route ("/graphics", methods = ["GET", "POST"])
@login_required
def graphics():
    if request.method == "GET":
        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        countries = set()
        for row  in data:
            countries.add(row['country'])

        sorted_countries = sorted(list(countries))

        return render_template("graphics.html", countries=sorted_countries)

    if request.method == "POST":
        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        countries = set()
        for row  in data:
            countries.add(row['country'])

        sorted_countries = sorted(list(countries))



        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        df = pd.DataFrame(data)
        country1 = request.form.get("country1")
        country2 = request.form.get("country2")
        df_filtered1 = df[df['country']==country1]
        df_filtered2 = df[df['country']==country2]

        # Adicione os gráficos de linha

        fig1 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['rgdpe'], mode='lines', name=country1))
        fig1.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['rgdpe'], mode='lines', name=country2))

        fig1.update_layout(title_text="Expenditure-side real GDP at chained PPPs (in mil. 2017US$)", title_x=0.5)
        fig1.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig2 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['popul'], mode='lines', name=country1))
        fig2.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['popul'], mode='lines', name=country2))
        fig2.update_layout(title_text="Population (in millions)", title_x=0.5)
        fig2.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig3 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['emp'], mode='lines', name=country1))
        fig3.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['emp'], mode='lines', name=country2))
        fig3.update_layout(title_text="Number of persons engaged (in millions)", title_x=0.5)
        fig3.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig4 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['hc'], mode='lines', name=country1))
        fig4.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['hc'], mode='lines', name=country2))
        fig4.update_layout(title_text="Human capital index, based on years of schooling and returns to education", title_x=0.5)
        fig4.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig5 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['cn'], mode='lines', name=country1))
        fig5.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['cn'], mode='lines', name=country2))
        fig5.update_layout(title_text="Capital stock at current PPPs (in mil. 2017US$)", title_x=0.5)
        fig5.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig6 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['rtfpna'], mode='lines', name=country1))
        fig6.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['rtfpna'], mode='lines', name=country2))
        fig6.update_layout(title_text="TFP at constant national prices (2017=1)", title_x=0.5)
        fig6.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig7 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['delta'], mode='lines', name=country1))
        fig7.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['delta'], mode='lines', name=country2))
        fig7.update_layout(title_text="Average depreciation rate of the capital stock", title_x=0.5)
        fig7.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig8 = go.Figure(go.Scatter(x=df_filtered1['year'], y=df_filtered1['csh_i'], mode='lines', name=country1))
        fig8.add_trace(go.Scatter(x=df_filtered2['year'], y=df_filtered2['csh_i'], mode='lines', name=country2))
        fig8.update_layout(title_text="Share of gross capital formation at current PPPs", title_x=0.5)
        fig8.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )


        # Salve o gráfico como um arquivo HTML
        fig1_html = plot(fig1, output_type='div')
        fig2_html = plot(fig2, output_type='div')
        fig3_html = plot(fig3, output_type='div')
        fig4_html = plot(fig4, output_type='div')
        fig5_html = plot(fig5, output_type='div')
        fig6_html = plot(fig6, output_type='div')
        fig7_html = plot(fig7, output_type='div')
        fig8_html = plot(fig8, output_type='div')

        return render_template('graphics.html', fig1=fig1_html,fig2=fig2_html, fig3=fig3_html, fig4=fig4_html, \
                               fig5=fig5_html, fig6=fig6_html, fig7=fig7_html,fig8=fig8_html, countries=sorted_countries)


@app.route ("/sollow", methods = ["GET", "POST"])
@login_required
def sollow():
    return render_template("sollow.html")


@app.route("/results", methods = ["GET", "POST"])
@login_required
def change_data():
    if request.method == "GET":
        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')
        countries = set()
        for row  in data:
            countries.add(row['country'])

        sorted_countries = sorted(list(countries))

        return render_template("results.html", countries=sorted_countries)

    if request.method == "POST":
        pwt_data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')

        countries = set()
        for row in pwt_data:
            countries.add(row['country'])

        sorted_countries = sorted(list(countries))

        pwt_data = pd.DataFrame(pwt_data)

        pwt_data = get_sollowdf(pwt_data)

        pwt = pwt_data

        country1 = request.form.get("country1")
        country2 = request.form.get("country2")

        pwt_country1 = pwt[pwt['country']==country1]
        pwt_country2 = pwt[pwt['country']==country2]


        fig1 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['gdp_growth_rate'], mode='lines', name=country1))
        fig1.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['gdp_growth_rate'], mode='lines', name=country2))

        fig1.update_layout(title_text="GDP growth rate", title_x=0.5)
        fig1.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig1_html = plot(fig1, output_type='div')


        fig2 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['savings_rate'], mode='lines', name=country1))
        fig2.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['savings_rate'], mode='lines', name=country2))

        fig2.update_layout(title_text="Savings rate", title_x=0.5)
        fig2.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig2_html = plot(fig2, output_type='div')


        fig3 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['pop_growth_rate'], mode='lines', name=country1))
        fig3.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['pop_growth_rate'], mode='lines', name=country2))

        fig3.update_layout(title_text="Population growth rate", title_x=0.5)
        fig3.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig3_html = plot(fig3, output_type='div')


        fig4 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['technological_progress'], mode='lines', name=country1))
        fig4.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['technological_progress'], mode='lines', name=country2))

        fig4.update_layout(title_text="Technological progress", title_x=0.5)
        fig4.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig4_html = plot(fig4, output_type='div')


        fig5 = go.Figure(go.Scatter(x=pwt_country1['year'], y=pwt_country1['capital_stock'], mode='lines', name=country1))
        fig5.add_trace(go.Scatter(x=pwt_country2['year'], y=pwt_country2['capital_stock'], mode='lines', name=country2))

        fig5.update_layout(title_text="Capital stock", title_x=0.5)
        fig5.add_annotation(
            text=country1 + " x " + country2,
            font=(dict(size=16)),
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False
        )

        fig5_html = plot(fig5, output_type='div')




        return render_template("results.html", countries=sorted_countries, fig1=fig1_html, fig2=fig2_html, fig3=fig3_html, \
                               fig4=fig4_html, fig5=fig5_html )



@app.route("/analysis", methods = ["GET", "POST"])
@login_required
def analisys():

    if request.method == "GET":

        data = db.execute("SELECT DISTINCT year FROM pennworld JOIN countries ON country_id = id")

        year = set()

        for row  in data:
            year.add(row['year'])

        sorted_year = sorted(list(year))

        return render_template("analysis.html", year=sorted_year)

    if request.method == "POST":

        year = request.form.get("year")

        data = db.execute('SELECT *, countrycode, country FROM pennworld JOIN countries ON country_id = id')

        df = pd.DataFrame(data)

        pwt = get_sollowdf(df)

        # Define alpha (output elasticity of capital)
        alpha = 1/3

        # Initialize the sollow list

        sollow = []

        # Iterate over the rows in the dataframe
        for index, row in pwt.iterrows():
            country = row['country']
            year = row['year']
            s = row['savings_rate']
            delta = row['capital_stock']
            n = row['pop_growth_rate']
            g = row['technological_progress']

        # Calculate k* and y*
            k_star = ss_capital_per_worker(s, delta, n, g, alpha)
            y_star = ss_output_per_worker(k_star, alpha)

        # Append the results to the sollow list
            sollow.append({
                'country': country,
                'year': year,
                'k_star': k_star,
                'y_star': y_star
            })

        sollow_year = sollow

    return render_template("analysis.html", sollow=sollow_year)



