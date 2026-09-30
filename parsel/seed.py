"""İlk açılışta arayüzün boş görünmemesi için ÖRNEK kayıtlar ekler (demo=1, arayüzde işaretli)."""
import db

DEMO = [
    ("Silivri'de yola cepheli imarlı arsa", "satilik", 4_250_000, 620, "İstanbul", "Silivri", "Konut imarlı"),
    ("Çeşme Alaçatı'da zeytinlikli tarla", "satilik", 6_800_000, 3400, "İzmir", "Çeşme", "Tarla"),
    ("Kırıkkale'de ticari imarlı arsa", "satilik", 1_900_000, 1100, "Kırıkkale", "Merkez", "Ticari"),
    ("Antalya Kumluca sera arazisi", "satilik", 2_300_000, 5200, "Antalya", "Kumluca", "Tarım"),
    ("Milli Emlak ihalesi: hazine arsası", "ihale", 950_000, 830, "Ankara", "Polatlı", "Konut imarlı"),
    ("TOKİ arsa satış ihalesi", "ihale", 3_100_000, 1450, "Bursa", "Nilüfer", "Konut+Ticaret"),
    ("Belediye ihalesi: 2 parsel", "ihale", 780_000, 640, "Samsun", "Atakum", "Konut imarlı"),
]

def run():
    db.init()
    with db.conn() as c:
        if c.execute("SELECT COUNT(*) FROM parcels").fetchone()[0]:
            return
        for i, (t, lt, p, a, city, d, z) in enumerate(DEMO):
            db.upsert(c, {"source": "ÖRNEK VERİ", "url": f"https://ornek.invalid/{i}", "title": t,
                          "listing_type": lt, "price": p, "area_m2": a, "city": city, "district": d,
                          "zoning": z, "deadline": "2025-12-01" if lt == "ihale" else None, "demo": 1})
