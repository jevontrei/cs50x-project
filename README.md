
# 2025 CS50x Final Project: Mapsing

https://github.com/jevontrei/cs50x-project

---

## Intro

Mapsing is named thusly because that's what Gollum would call it. It is a simple web app that mostly takes place on one page. It uses OpenStreetMap (via Leaflet.js) to create an interactive website for mapping purposes. 

Mapsing was mostly designed with travel in mind. I made it for  my partner and I to use as a travel itinerary planning tool for an actual upcoming overseas trip. I also chose this project topic so I could learn more about geospatial tools, which may help me with my work in industrial pollution analysis/consulting.

---

## How to use Mapsing

Install `uv`:

- https://docs.astral.sh/uv/getting-started/installation/

Install `sqlite3`. This depends on your OS. You may already have it, but if not:

- https://sqlite.org/download.html

Create the `maps.db` file:

```sh
sqlite3 maps.db
```

Now initialise your database with the boilerplate seed data:

```sh
# Create tables and seed data
uv run python db.py        

# Run this when you need fresh start
uv run python db_reset.py  
```

Run the app:

```sh
uv run flask --app app.py --debug run
```

---

## Video Demo

https://...

---

## Tech / resources used

- `Python`/`Flask`, for the backend
- `JavaScript`/`HTML`/`CSS`/`Bootstrap`, for the frontend
- `SQLite`, for the database
- `Jinja`, for templating
- `OpenStreetMap` (OSM), for maps
- `Leaflet.js`, to get `OpenStreetMap` happening
- `Leaflet.draw`, to enable drawing shapes on the map
- `Nominatim`, for searching coordinates using place names
- `uv`, for environment management
- `git`, for version control
- `Netlify`, for deploying the site
- `Claude AI`, for learning

I chose Python and Flask because they are the tools I am most familiar with, having made very basic web apps before. The JavaScript in this project is minimal - just enough to get the thing working. 

Despite Postgres being the only database I had previously worked with (and only to a modest extent), I chose SQLite because it was introduced in CS50x and it seemed simple and approachable. I like that it is just a humble little `.db` file on my computer. Very transparent!

I have been using `uv` recently and I find it a wonderful and simple way to work with the Python environment.

Claude has proved to be a very useful teacher through this process. Where I have used Claude, I have also worked hard to understand the code or the tool that is being suggested, and I hope that is reflected in my code comments. My goal is to learn about software and gain experience. Claude was mostly used for Leaflet, which was entirely new to me.

---

## Places and shapes

The basic functionality is based on places and shapes. I chose to give them a parent-child relationship because that's how I think about it, and that's how I actually tend to structure my travel information in my personal notes/spreadsheets/calendars. I wanted a higher-level category (places) so that you're not looking at a huge mess of points, linestrings and polygons. They (shapes) should be organised into broader groups (places), e.g. Seattle, Singapore, and Tokyo.

### Places

Places are major locations or destinations (usually cities). Places can be points only (no linestrings or polygons). 

By default, several shapes are seeded into the database by `init_db()`. The user can easily remove seed places if desired. As already mentioned, the `places` SQLite table is the parent table to `shapes`. 

Places can be added with a simple form, which uses Nominatim to geocode places, i.e. search coordinates by place name.

### Shapes

Shapes are like sub-places. They are points of interest, or routes between places, etc. They can be points, lines, or polygons. Polygons are useful for highlighting a region, e.g. "here's the Chinatown part of the city that I am particularly interested in visiting and eating at".

Similarly to places, several shapes are seeded into the database by `init_db()`. Delete them as you wish! The `shapes` table in the database is the child/foreign-key table to the `places` table. 

The user can draw shapes into the map using `Leaflet.draw`. 

---

## Files

### `app.py`

This is the central script of the project. It creates an instance of a Flask app, and defines a function for geocoding (searching coordinates by place name) places, and defines all of our routes.

### `main.py`

Created when the `uv` project is initialised, but not used beyond that.

### `db.py`

This file simply defines one function, `init_db()`, that is called when the user runs either of these commands:

- `uv run python db.py`
- `uv run python db_reset.py`

The function `init_db()` creates a connection to the SQLite database, creates SQLite tables for `places` and `shapes`, and seeds them with basic example data.

### `db_reset.py`

This simply drops the `places` and `shapes` tables before calling `init_db()`.

### `maps.db`

The actual SQLite database file that contains our places and shapes information!

### `static/seedPlaces.json`

A collection of places in `json` format. E.g.:

```json
  {
      "name": "Seattle",
    "country": "United States",
    "lat": 47.61,
    "long": -122.33,
    "end_date": "2025-07-15"
  },
```

### `static/seedShapes.json`

A collection of shapes in `json` format. This is slightly more involved than `seedPlaces.json`, because we have multiple types of shapes: points, linestrings, and polygons. The `geometry` part of each `json` entry contains part of  what's needed to handle the full GeoJSON format in functions like `toGeoJSON()` in `drawshape.html` and `geoJSON()` in `index.html`.

Polygon example:

```json
    {
        "name": "Seattle domain",
        "type": "polygon",
        "color": "red",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-122.3, 47.6],
                    [-122.2, 47.6],
                    [-122.2, 47.5],
                    [-122.3, 47.5],
                    [-122.3, 47.6]
                ]
            ]
        },
        "place_id": 1,
        "category": "region of interest"
    },
```

Linestring example:

```json
    {
        "name": "Dubai to Seattle",
        "type": "linestring",
        "color": "blue",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [55.27, 25.20],
                [-122.33, 47.61]
            ]
        }
    }
```

### `static/css/styles.css`

Some very basic CSS to style the webpage, mostly using Flexbox.

### `templates/index.html`

This is the primary page for Mapsing, and it extends the Jinja template `layout.html`. It shows three main elements: your map, your places, and your shapes.

The OpenStreetMap map is the main feature of the page, and it shows all of your places and shapes. Clicking on a place or shape shows its name, which is implemented using `bindPopup()`. The map is implemented using `Leaflet.js`.

Places are summarised in a table below the map. In a form below that, the user can add a place by searching for it with Nominatim.

Shapes are also summarised in a table. You can add a shape by entering some basic details in the shapes form and then clicking `Do it`, which takes you to `drawshape.html`.

### `templates/drawshape.html`

This is the only other page in Mapsing. It also extends `layout.html`. When the user wants to create their own shape (point, line, or polygon), they first enter a shape name (and optionally some other parameters) in the `Add a shape` form in `index.html`. That takes you to `drawshape.html`, which has a map that you can draw shapes on.The drawing functionality is implemented with `Leaflet.draw`.

### `templates/layout.html`

The Jinja template for the other HTML pages. It specifies everything except the `<main>` element.

---

## Routes

`/`

The main page. For GET and POST requests: getting all places and shapes from the database, OR submitting the `Add a place` form. 

`/drawshape`

For POST requests, to draw a shape on the map and add it to the database.

`/saveshape`

For POST requests, to save a shape to the database. This gets called from `drawshape.html` when the user clicks the `Save Shape` button.

`/deleteplace`

For POST requests, to remove a place from the database.

`/deleteshape`

For POST requests, to remove a shape from the database.

---

## Future TODOs

Note: TODOs are scattered through the code. This is intentional, as I expect to keep working on this project after submission.

- Add place re-ordering

- Responsive design - mobile!

- Seeded shapes data has hard-coded place_id FKs; this will break - redesign it!

- Implement proper env/flaskenv (environment variables)

- Add "zoom to shape/place" functionality

- Show all shapes and places in drawshape.html

- `geocode_place()`: add error handling because if you search nonsense, it will crash: TypeError

- I removed a function that may be useful for the `drawshape` and `saveshape` routes one day:

```py
def build_geojson(shape_id):
    row = con.execute(
        "SELECT name, color, geometry FROM shapes WHERE id=?", (shape_id,)
    ).fetchone()

    return {
        "type": "Feature",
        "properties": {"name": row[0], "color": row[1]},
        "geometry": json.loads(row[2]),  # just the geometry part
    }
```
