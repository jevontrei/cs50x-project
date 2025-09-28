import sqlite3


def init_db():
    con = sqlite3.connect("maps.db")

    # create tables
    # don't need "autoincrement" for PKs in sqlite
    con.execute("""
                create table if not exists places (
                    id integer primary key,
                    name text not null,
                    country text,
                    lat real,
                    long real
                )
                """)
    # seed
    con.execute("""
                insert or ignore into places (
                    name, country, lat, long
                )
                values 
                ('Brisbane', 'Australia', -27.47, 153.03),
                ('Bali', 'Indonesia', -8.41, 115.19),
                ('Bangkok', 'Thailand', 13.76, 100.50),
                ('Negombo', 'Sri Lanka', 7.21, 79.85),
                ('Hong Kong', 'Hong Kong', 22.29, 114.12)
                """)  # each set of () is a new row

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
    # TODO: find if/where "Brisbane line" is appearing on the map
    con.execute("""
                insert or ignore into shapes (
                    name, type, color, geometry
                )
                values
                ('Brisbane domain', 'polygon', 'red', 
                '{
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [153.0, -27.4],
                            [153.1, -27.4],
                            [153.1, -27.5],
                            [153.0, -27.5],
                            [153.0, -27.4]
                        ]
                    ]
                }'
                ),
                ('Brisbane line', 'linestring', 'green',
                '{
                    "type": "LineString",
                    "coordinates": [
                        [0,   0],
                        [180, 0]
                    ]
                }'
                )
                """)

    con.commit()  # write changes to file/disk
    con.close()


if __name__ == "__main__":
    init_db()
    print("db is initted!")
