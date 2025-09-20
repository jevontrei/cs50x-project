import sqlite3

def init_db():
    con = sqlite3.connect("maps.db")
    
    # create tables
    con.execute('''
                create table if not exists places (
                    id integer primary key autoincrement,
                    name text not null,
                    country text,
                    lat real,
                    long real
                )
                ''')
    
    # seed
    con.execute('''
                insert or ignore into places (
                    name, country, lat, long
                )
                values 
                ('Brisbane', 'Australia', -27.47, 153.03),
                ('Bali', 'Indonesia', -8.41, 115.19),
                ('Bangkok', 'Thailand', 13.76, 100.50)
                ''')

    con.commit()  # write changes to file/disk
    con.close()
    
if __name__ == "__main__":
    init_db()
    print("db is initted!")
    