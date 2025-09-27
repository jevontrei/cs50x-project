import sqlite3


def init_db():
    con = sqlite3.connect("maps.db")

    # TODO drop table first? to avoid duplicates

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
                create table if not exists shapes (
                    id integer primary key,
                    name text,
                    type text not null,
                    geometry text,
                    color text default 'blue'
                )
                """)  # available types: point, linestring, polygon
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
                ('Brisbane line', 'line', 'green',
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
