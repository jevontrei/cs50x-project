
# 2025 CS50x Final Project: Mapsing

Author: Joel von Treifeldt

## Video Demo:  https://...

## TODO
- add POI with notes (e.g. a restaurant or forest we'd like to visit)
- add place re-ordering
- responsive design - mobile!
- seeded shapes data has hard-coded place_id FKs; this will break - redesign it!
- figure out env/flaskenv (environment variables)
- add zoom to shape/place functionality

## Tech / resources used

- Python/Flask, for the backend
- JavaScript/HTML/CSS/Bootstrap, for the frontend
- SQLite, for the database
- Jinja, for templating
- Open Street Maps
- Leaflet.js, to get Open Street Maps happening
- Leaflet.draw, to enable drawing shapes on the map
- Nominatim, for searching for coordinates using place names
- uv, for environment management
- git, for version control
- Netlify, for deploying the site
- Claude AI, for learning

## Description

Mapsing is a simple project that uses Open Street Maps (via Leaflet.js) to create an interactive website for mapping purposes, optionally as a travel itinerary. Mapsing mostly takes place on one page. The basic functionality is based on places and shapes.

### Places

Places are major locations or destinations (usually cities). Places can be points only (no linestrings or polygons). 

By default, several shapes are seeded into the database by `init_db()`. The `places` SQLite table is the parent table to `shapes`. 

Places can be added with a simple form, which uses Nominatim to geocode, i.e. search coordinates by place name.

### Shapes

Shapes are like sub-places. They are points of interest, or routes between places, etc. They can be points, lines, or polygons. 

Similarly to places, several shapes are seeded into the database by `init_db()`. The `shapes` table in the database is the child/foreign-key table to the `places` table. 

The user can draw shapes into the map using Leaflet.draw. 

### OSM

### Leaflet.js and Leaflet.draw

A map is 

### Nominatim

Search


---

## Routes

`/`

`/deleteplace`

`/deleteshape`

`/drawshape`

`/saveshape`


---

## How To

Ensure you have `uv` and `sqlite3` installed. Create the `maps.db` file if necessary:
```bash
sqlite3 maps.db
```

Now initialise your database with the boilerplate seed data:

```bash
# Create tables and seed data
uv run python db.py        

# When you need fresh start
uv run python db_reset.py  
```

