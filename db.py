import json
import sqlite3


def init_db():
    con = sqlite3.connect("maps.db")

    # create places table
    # don't need "autoincrement" for PKs in sqlite
    con.execute("""
                create table if not exists places (
                    id integer primary key,
                    name text not null,
                    country text,
                    lat real,
                    long real,
                    start_date,
                    end_date
                )
                """)
    # seed places
    with open("static/seedPlaces.json", "r") as f:
        place_seeds = json.load(f)
        for place in place_seeds:
            con.execute(
                """
                INSERT OR IGNORE INTO places (name, country, lat, long, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    place["name"],
                    place["country"],
                    place["lat"],
                    place["long"],
                    place.get("start_date"),
                    place.get("end_date"),
                ),
            )

    # create shapes table
    con.execute("""
                CREATE TABLE if not exists shapes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,  -- 'point', 'linestring', 'polygon'
                geometry TEXT,  -- GeoJSON (or rather part thereof? check this)
                color TEXT,
                place_id INTEGER,  -- optional; links to parent place (city)
                category TEXT,  -- 'restaurant', 'route', 'area', etc; include this to enable aggregating, e.g. "all our routes added up to 100000 km"
                notes TEXT,
                FOREIGN KEY (place_id) REFERENCES places (id)
                )
                """)

    # seed shapes
    with open("static/seedShapes.json", "r") as f:
        shape_seeds = json.load(f)
        # TODO: find if/where "Brisbane line" is appearing on the map
        # pay attention to lat/long order; geojson use long/lat, while leaflet uses lat/long
        for shape in shape_seeds:
            con.execute(
                """
                INSERT INTO shapes (name, type, geometry, color, place_id, category, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                 """,
                (
                    shape["name"],
                    shape["type"],
                    json.dumps(shape["geometry"]),  # Convert dict back to JSON string
                    shape["color"],
                    shape.get("place_id"),
                    shape.get("category"),
                    shape.get("notes"),
                ),
            )

    con.commit()  # write all changes to file/disk
    con.close()


if __name__ == "__main__":
    init_db()
    print("db is initted!")
