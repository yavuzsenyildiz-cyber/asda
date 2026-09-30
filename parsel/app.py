import csv, io, threading, os
from flask import Flask, jsonify, request, send_from_directory, Response
import db, scraper

app = Flask(__name__, static_folder="static")
scan_state = {"running": False, "last": []}


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/parcels")
def parcels():
    a = request.args
    where, args = [], []
    if a.get("q"):
        where.append("(title LIKE ? OR city LIKE ? OR district LIKE ? OR zoning LIKE ?)")
        args += [f"%{a['q']}%"] * 4
    for col in ("city", "source", "listing_type", "status"):
        if a.get(col):
            where.append(f"{col}=?"); args.append(a[col])
    for key, col, op in (("min_price", "price", ">="), ("max_price", "price", "<="),
                         ("min_area", "area_m2", ">="), ("max_area", "area_m2", "<=")):
        if a.get(key):
            where.append(f"{col} {op} ?"); args.append(float(a[key]))
    if a.get("hide_rejected", "1") == "1" and not a.get("status"):
        where.append("status != 'rejected'")
    order = {"price": "price", "area": "area_m2", "ppm2": "price/area_m2", "new": "first_seen DESC",
             "deadline": "deadline"}.get(a.get("sort", "new"), "first_seen DESC")
    if order in ("price", "area_m2", "price/area_m2", "deadline"):
        order += " ASC"
    sql = "SELECT * FROM parcels" + (" WHERE " + " AND ".join(where) if where else "") + f" ORDER BY {order} LIMIT 1000"
    with db.conn() as c:
        rows = [dict(r) for r in c.execute(sql, args)]
    for r in rows:
        r["price_per_m2"] = round(r["price"] / r["area_m2"]) if r["price"] and r["area_m2"] else None
    return jsonify(rows)


@app.get("/api/facets")
def facets():
    with db.conn() as c:
        cities = [r[0] for r in c.execute("SELECT DISTINCT city FROM parcels WHERE city IS NOT NULL ORDER BY city")]
        sources = [r[0] for r in c.execute("SELECT DISTINCT source FROM parcels ORDER BY source")]
        demo = c.execute("SELECT COUNT(*) FROM parcels WHERE demo=1").fetchone()[0]
    return jsonify({"cities": cities, "sources": sources, "demo": demo})


@app.patch("/api/parcels/<int:pid>")
def update(pid):
    data = request.get_json(force=True)
    sets, args = [], []
    if "status" in data:
        if data["status"] not in ("new", "shortlist", "rejected"):
            return jsonify(error="gecersiz durum"), 400
        sets.append("status=?"); args.append(data["status"])
    if "note" in data:
        sets.append("note=?"); args.append(str(data["note"])[:2000])
    if not sets:
        return jsonify(error="bos"), 400
    with db.conn() as c:
        c.execute(f"UPDATE parcels SET {', '.join(sets)} WHERE id=?", args + [pid])
    return jsonify(ok=True)


@app.post("/api/parcels")
def add_manual():
    d = request.get_json(force=True)
    if not d.get("url"):
        return jsonify(error="link gerekli"), 400
    city, district = scraper.split_location(d.get("location"))
    item = {"source": "Elle eklendi", "url": d["url"], "title": d.get("title") or d["url"],
            "listing_type": d.get("listing_type", "satilik"),
            "price": scraper.parse_number(str(d.get("price", ""))), "area_m2": scraper.parse_number(str(d.get("area", ""))),
            "city": city, "district": district, "zoning": d.get("zoning"), "deadline": d.get("deadline")}
    with db.conn() as c:
        db.upsert(c, item)
    return jsonify(ok=True)


@app.post("/api/scrape")
def scrape():
    if scan_state["running"]:
        return jsonify(error="tarama zaten çalışıyor"), 409

    def job():
        scan_state["running"] = True
        try:
            scan_state["last"] = scraper.run_all()
        finally:
            scan_state["running"] = False
    threading.Thread(target=job, daemon=True).start()
    return jsonify(started=True)


@app.get("/api/scrape/status")
def scrape_status():
    enabled = [s["name"] for s in scraper.load_sources() if s.get("enabled")]
    with db.conn() as c:
        runs = [dict(r) for r in c.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 10")]
    return jsonify(running=scan_state["running"], last=scan_state["last"], enabled=enabled, runs=runs)


@app.delete("/api/demo")
def delete_demo():
    with db.conn() as c:
        c.execute("DELETE FROM parcels WHERE demo=1")
    return jsonify(ok=True)


@app.get("/api/export.csv")
def export():
    with db.conn() as c:
        rows = c.execute("SELECT source,listing_type,title,city,district,price,area_m2,zoning,deadline,url,note FROM parcels WHERE status='shortlist'").fetchall()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Kaynak", "Tür", "Başlık", "İl", "İlçe", "Fiyat", "m²", "İmar", "Son tarih", "Link", "Not"])
    for r in rows:
        w.writerow(list(r))
    return Response("﻿" + buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=secilen_parseller.csv"})


if __name__ == "__main__":
    db.init()
    if os.environ.get("PARSEL_SEED", "1") == "1":
        import seed; seed.run()
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
