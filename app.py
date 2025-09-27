import click
import json
import requests
import sqlite3
import time
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

"""
TODO: 
- add/make/draw shapes
- add points with notes (e.g. a restaurant or forest we'd like to visit)
- add "start line"
- add dates to places
- add place re-ordering



"""

app = Flask(__name__)

## RESET DB
## don't run this here because you'll get duplicates; just run `uv run python db.py` in the terminal once, and drop/recreate as needed
# init_db()

DATABASE = "maps.db"


## move this fn (or just the code) inside an /addshape route?
def build_geojson(shape_id):
    row = con.execute(
        "SELECT name, color, geometry FROM shapes WHERE id=?", (shape_id,)
    ).fetchone()

    return {
        "type": "Feature",
        "properties": {"name": row[0], "color": row[1]},
        "geometry": json.loads(row[2]),  # Just the geometry part
    }


def geocode_place(place_name):
    """Get lat/lon for a place name using Nominatim"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "mapsing/1.0"}  # check/understand this

    response = requests.get(url, params=params, headers=headers)
    time.sleep(1)  # respect rate limit

    if response.json():
        data = response.json()[0]
        return float(data["lat"]), float(data["lon"])

    return None, None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        con = sqlite3.connect(DATABASE)
        places = con.execute(
            "select * from places"
        ).fetchall()  # without fetchall() we'd just have a sqlite cursor object
        con.close()
        return render_template("index.html", places=places)

    elif request.method == "POST":
        place_new = request.form.get("place_new")
        country_new = request.form.get("country_new")
        query = place_new + ", " + country_new

        # use nominatim to search for lat/lon based on the user's entered place name/s
        latlon = geocode_place(query)
        print(latlon)
        print(round(latlon[0], 2))
        print(round(latlon[1], 2))
        round(latlon[0], 2)
        round(latlon[1], 2)

        con = sqlite3.connect(DATABASE)
        places = con.execute(
            "insert into places (name, country, lat, long) values (?, ?, ?, ?)",
            (place_new, country_new, round(latlon[0], 2), round(latlon[1], 2)),
        )
        con.commit()  # write changes to file/disk
        con.close()

        return redirect("/")
        # return render_template("index.html", places=places)


@app.route("/delete", methods=["POST"])
def delete():
    place_id = request.form.get("place_id")
    con = sqlite3.connect(DATABASE)
    con.execute(
        "delete from places where id = ?", (place_id,)
    )  # must always pass a tuple (or a list), even if only one parameter
    con.commit()
    con.close()
    return redirect("/")


# DELET? SS by /addshape?
@app.route("/addline")  # methods=[""]
def add_line():
    place_id = request.form.get("place_id")
    con = sqlite3.connect(DATABASE)

    # TODO: create a shapes table to store lines and boxes etc, and query that
    con.execute("select * from shapes where place_id = ?", (place_id,))

    con.commit()
    con.close()

    return render_template("endline.html")  # THERE must be a simpler way than this


@app.route("/addshape", methods=["POST"])
def add_shape():
    shape_name = request.form.get("shape_name")
    shape_type = request.form.get("shape_type")
    shape_color = request.form.get("shape_color")

    # TODO use an enum to validate shape type
    # SHAPE_TYPES = ENUM
    # if shape_type not in SHAPE_TYPES:
    # return ...?

    return render_template(
        "drawshape.html",
        shape_name=shape_name,
        shape_type=shape_type,
        shape_color=shape_color,
    )


@app.route("/saveshape", methods=["POST"])
def save_shape():
    shape_name = request.form.get("shape_name")
    shape_type = request.form.get("shape_type")
    shape_color = request.form.get("shape_color")
    geometry = request.form.get("geometry")  # json?

    # TODO validate using enum here or in /addshape?

    shape_geometry = geometry  # TODO this instead: build_geojson(shape_id=)

    con = sqlite3.connect(DATABASE)
    con.execute(
        "insert into shapes (name, type, geometry, color) values (?, ?, ?, ?)",
        (shape_name, shape_type, shape_geometry, shape_color),
    )
    con.commit()
    con.close()

    return redirect("/")


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

        con = sqlite3.connect(DATABASE)
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
        con = sqlite3.connect(DATABASE)
        # try:
        places = con.execute("select * from places").fetchall()
        con.close()
        return render_template("distance.html", places=places)


# @app.route("/itinerary")
# def itinerary():
#     ...
