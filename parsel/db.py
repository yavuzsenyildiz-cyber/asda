import sqlite3, os, datetime

DB_PATH = os.environ.get("PARSEL_DB", os.path.join(os.path.dirname(__file__), "parsel.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS parcels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  url TEXT NOT NULL UNIQUE,
  title TEXT,
  listing_type TEXT DEFAULT 'satilik',
  price REAL,
  area_m2 REAL,
  city TEXT,
  district TEXT,
  zoning TEXT,
  deadline TEXT,
  status TEXT DEFAULT 'new',
  note TEXT DEFAULT '',
  demo INTEGER DEFAULT 0,
  first_seen TEXT,
  last_seen TEXT
);
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT, started TEXT, finished TEXT, found INTEGER, new INTEGER, error TEXT
);
"""

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.executescript(SCHEMA)

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def upsert(c, item):
    """item: dict. Returns True if the parcel is new. status/note of existing rows are kept."""
    t = now()
    row = c.execute("SELECT id FROM parcels WHERE url=?", (item["url"],)).fetchone()
    if row:
        c.execute(
            "UPDATE parcels SET title=?, price=?, area_m2=?, city=?, district=?, zoning=?, deadline=?, last_seen=? WHERE id=?",
            (item.get("title"), item.get("price"), item.get("area_m2"), item.get("city"),
             item.get("district"), item.get("zoning"), item.get("deadline"), t, row["id"]))
        return False
    c.execute(
        "INSERT INTO parcels(source,url,title,listing_type,price,area_m2,city,district,zoning,deadline,demo,first_seen,last_seen)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (item["source"], item["url"], item.get("title"), item.get("listing_type", "satilik"),
         item.get("price"), item.get("area_m2"), item.get("city"), item.get("district"),
         item.get("zoning"), item.get("deadline"), item.get("demo", 0), t, t))
    return True
