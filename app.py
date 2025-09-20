import click
import sqlite3
from haversine import haversine
from datetime import datetime
from db import init_db
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    g,
    current_app,
)

app = Flask(__name__)

# init_db()  # don't run this here because you'll get duplicates; just run `uv run python db.py` in the terminal once, and drop/recreate as needed


@app.route("/")
def index():
    con = sqlite3.connect("maps.db")
    places = con.execute(
        "select * from places"
    ).fetchall()  # without fetchall() we'd just have a sqlite cursor object
    con.close()
    return render_template("index.html", places=places)


@app.route("/distance", methods=["GET", "POST"])
def distance():
    if request.method == "POST":
        place1, place2 = None, None  # init places to enable while loop
        while not place1 or not place2:
            # TODO: understand when request.args.get() would be appropriate; -> this changes when you included method="post" in the <form> tag!
            place1 = request.form.get(
                "place1"
            )  # , 'Brisbane')  # can specify a default value (but the html is set to "required" anyway)
            place2 = request.form.get("place2")

        con = sqlite3.connect("maps.db")
        # try:
        places = con.execute(
            "select * from places where name = ? or name = ?", (place1, place2)
        ).fetchall()  # this returns a list of tuples

        # calc distance between places; haversine gets us the "great circle distance", i.e. it takes into account the shape of the earth
        latlon1 = (places[0][3], places[0][4])
        latlon2 = (places[1][3], places[1][4])

        dist_hsine = round(haversine(latlon1, latlon2), 1)
        print(place1, place2, dist_hsine)
        con.close()
        return render_template(
            "distanced.html",
            place1=place1,
            place2=place2,
            latlon1=latlon1,
            latlon2=latlon2,
            dist_hsine=dist_hsine,
        )

    elif request.method == "GET":
        con = sqlite3.connect("maps.db")
        # try:
        places = con.execute("select * from places").fetchall()
        con.close()
        return render_template("distance.html", places=places)


# @app.route("/itinerary")
# def itinerary():
#     ...
