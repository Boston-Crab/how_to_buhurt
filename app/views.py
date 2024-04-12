from flask import Flask, render_template, request
from app import app
import psycopg2


db_url = "postgres://buhurt_info_user:VT6haqJOmw27F8PCcMjOXU3AxnAIpiBi@dpg-cocm5ta0si5c73albsfg-a.frankfurt-postgres.render.com/buhurt_info"
conn = psycopg2.connect(db_url)

# conn = psycopg2.connect(
#     dbname="buhurt_info",
#     user="postgres",
#     password="postgres",
#     host="localhost",
#     port="5432"
# )

with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(50) NOT NULL,
            city VARCHAR(100) NOT NULL,
            description TEXT,
            website_1 VARCHAR(200),
            website_2 VARCHAR(200)
        )
    """)
    conn.commit()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/what_is_buhurt")
def introduction():
    return render_template("what_is_buhurt.html")

@app.route("/training")
def training_page():
    return render_template("training.html")

@app.route("/team_finder")
def team_finder_page():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT country FROM teams"
            )
            countries = cursor.fetchall()

    selected_country = request.args.get("country")

    with conn:
        with conn.cursor() as cursor:
            if selected_country:
                cursor.execute(
                    "SELECT name, country, city, website_1, website_2 FROM teams WHERE country = %s",
                    (selected_country,)
                )
            else:
                cursor.execute(
                    "SELECT name, country, city, website_1, website_2 FROM teams"
                )
            teams = cursor.fetchall()
    return render_template("team_finder.html", teams=teams, countries=countries)

@app.route("/armor")
def armor_page():
    return render_template("armor.html")