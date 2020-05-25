import sqlite3

#connection object [establish connection]
conn = sqlite3.connect('insights.db')
#cursor object [for executing queries]
c = conn.cursor()

try:
    c.execute('DROP TABLE records')
    c.execute('DROP TABLE forms')
except:
    pass

c.execute("""
CREATE TABLE forms (
    formid INTEGER NOT NULL PRIMARY KEY,
    desc TEXT NOT NULL
) """)

c.execute("""
CREATE TABLE records (
    recordid INTEGER NOT NULL PRIMARY KEY,
    formid INTEGER NOT NULL,
    latitude TEXT,
    longitude TEXT,
    postcode TEXT,
    url TEXT,
    FOREIGN KEY(formid) REFERENCES forms(formid)
) """)

formvals = [(2,"PPE Suppliers"),(4,"Incoming Data - collects twitter, sms and email requests"),(5,"Volunteers"),(6,"PPE Needs"),(9,"Good News - good stories about PPE needs being met")]

c.executemany('INSERT INTO forms VALUES(?,?)',formvals)

conn.commit()
conn.close()
