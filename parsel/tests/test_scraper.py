import os, sys, threading, tempfile, http.server, socketserver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["PARSEL_DB"] = tempfile.mktemp(suffix=".db")

import db, scraper

PAGE1 = """<div class=l><h3>Silivri arsa</h3><a href="/i/1">x</a><span class=p>1.250.000 TL</span><span class=a>2.500 m²</span><span class=c>İstanbul / Silivri</span></div>
<div class=l><h3>Çeşme tarla</h3><a href="/i/2">x</a><span class=p>1,5 milyon TL</span><span class=a>3.400,5 m²</span><span class=c>İzmir - Çeşme</span></div>"""

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/robots.txt"):
            self.send_response(404); self.end_headers(); return
        body = PAGE1 if "page=1" in self.path else ""
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(body.encode())
    def log_message(self, *a): pass

def test_numbers():
    assert scraper.parse_number("1.250.000 TL") == 1250000
    assert scraper.parse_number("3.400,5 m²") == 3400.5
    assert scraper.parse_number("1,5 milyon TL") == 1500000
    assert scraper.parse_number("yok") is None
    assert scraper.split_location("İzmir - Çeşme") == ("İzmir", "Çeşme")

def test_run():
    srv = socketserver.TCPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    db.init()
    src = {"name": "Test", "type": "satilik", "delay": 0, "max_pages": 3,
           "start_urls": [f"http://127.0.0.1:{port}/list?page={{page}}"], "item": "div.l",
           "fields": {"title": {"sel": "h3"}, "url": {"sel": "a", "attr": "href"}, "price": {"sel": ".p"},
                      "area": {"sel": ".a"}, "location": {"sel": ".c"}}}
    found, new, err = scraper.run_source(src)
    assert (found, new, err) == (2, 2, None), (found, new, err)
    assert scraper.run_source(src)[1] == 0  # ikinci tarama yinelenen eklemez
    with db.conn() as c:
        rows = c.execute("SELECT * FROM parcels ORDER BY id").fetchall()
    assert rows[0]["price"] == 1250000 and rows[0]["city"] == "İstanbul" and rows[0]["district"] == "Silivri"
    assert rows[1]["price"] == 1500000 and rows[1]["area_m2"] == 3400.5
    assert rows[0]["url"] == f"http://127.0.0.1:{port}/i/1"
    srv.shutdown()

if __name__ == "__main__":
    test_numbers(); test_run(); print("OK")
