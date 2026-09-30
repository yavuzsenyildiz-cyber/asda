"""Ayar dosyasına (sources.yaml) göre çalışan genel tarayıcı.

Her kaynak için CSS seçicileri sources.yaml'da tanımlanır. robots.txt'e uyulur,
istekler arasında bekleme yapılır, engellenen (403/429) siteler atlanır.
"""
import re, time, urllib.parse, urllib.robotparser, os
import requests, yaml
from bs4 import BeautifulSoup
import db

UA = "ParselTakip/1.0 (kisisel arastirma; robots.txt'e uyar)"
SOURCES_PATH = os.environ.get("PARSEL_SOURCES", os.path.join(os.path.dirname(__file__), "sources.yaml"))


def parse_number(text):
    """'1.250.000 TL' -> 1250000.0 ; '2.500,5 m²' -> 2500.5 ; '1,5 milyon' -> 1500000"""
    if not text:
        return None
    t = text.lower().replace("\xa0", " ")
    mult = 1
    if "milyon" in t:
        mult = 1_000_000
    elif "bin" in t:
        mult = 1_000
    m = re.search(r"\d[\d.,]*", t)
    if not m:
        return None
    s = m.group(0).rstrip(".,")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) != 3 else s.replace(",", "")
    elif "." in s:
        parts = s.split(".")
        if len(parts[-1]) == 3 or len(parts) > 2:
            s = s.replace(".", "")
    try:
        return float(s) * mult
    except ValueError:
        return None


def split_location(text):
    """'İstanbul / Silivri', 'Silivri, İstanbul', 'İstanbul - Silivri - Mah' -> (il, ilçe)"""
    if not text:
        return None, None
    parts = [p.strip() for p in re.split(r"[/,\-–|>]", text) if p.strip()]
    if not parts:
        return None, None
    city = parts[0]
    district = parts[1] if len(parts) > 1 else None
    return city, district


def extract(node, spec):
    if not spec:
        return None
    if isinstance(spec, str):
        spec = {"sel": spec}
    el = node.select_one(spec["sel"]) if spec.get("sel") else node
    if el is None:
        return None
    val = el.get(spec["attr"]) if spec.get("attr") else el.get_text(" ", strip=True)
    if val and spec.get("regex"):
        m = re.search(spec["regex"], val)
        val = m.group(1) if m and m.groups() else (m.group(0) if m else None)
    return val.strip() if isinstance(val, str) else val


def robots_ok(url, cache={}):
    p = urllib.parse.urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    rp = cache.get(base)
    if rp is None:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = requests.get(base + "/robots.txt", headers={"User-Agent": UA}, timeout=10)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])
        cache[base] = rp
    return rp.can_fetch(UA, url)


def parse_listing(html, base_url, src):
    soup = BeautifulSoup(html, "html.parser")
    f = src["fields"]
    items = []
    for node in soup.select(src["item"]):
        link = extract(node, f.get("url"))
        if not link:
            continue
        url = urllib.parse.urljoin(base_url, link)
        city, district = split_location(extract(node, f.get("location")))
        items.append({
            "source": src["name"],
            "url": url,
            "title": extract(node, f.get("title")),
            "listing_type": src.get("type", "satilik"),
            "price": parse_number(extract(node, f.get("price"))),
            "area_m2": parse_number(extract(node, f.get("area"))),
            "city": city,
            "district": district,
            "zoning": extract(node, f.get("zoning")),
            "deadline": extract(node, f.get("deadline")),
        })
    return items


def run_source(src):
    """Bir kaynağı tarar. (bulunan, yeni, hata) döner."""
    found = new = 0
    err = None
    delay = float(src.get("delay", 3))
    max_pages = int(src.get("max_pages", 3))
    try:
        for start in src["start_urls"]:
            for page in range(1, max_pages + 1):
                url = start.replace("{page}", str(page))
                if not robots_ok(url):
                    err = f"robots.txt izin vermiyor: {url}"
                    break
                r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "tr"}, timeout=20)
                if r.status_code in (403, 429, 503):
                    err = f"Site isteği engelledi (HTTP {r.status_code}): {url}"
                    break
                r.raise_for_status()
                items = parse_listing(r.text, url, src)
                if not items:
                    break
                with db.conn() as c:
                    for it in items:
                        found += 1
                        new += db.upsert(c, it)
                if "{page}" not in start:
                    break
                time.sleep(delay)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    return found, new, err


def load_sources():
    with open(SOURCES_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh).get("sources", [])


def run_all(only=None):
    results = []
    for src in load_sources():
        if not src.get("enabled", False):
            continue
        if only and src["name"] != only:
            continue
        started = db.now()
        found, new, err = run_source(src)
        with db.conn() as c:
            c.execute("INSERT INTO runs(source,started,finished,found,new,error) VALUES(?,?,?,?,?,?)",
                      (src["name"], started, db.now(), found, new, err))
        results.append({"source": src["name"], "found": found, "new": new, "error": err})
    return results


if __name__ == "__main__":
    db.init()
    for r in run_all():
        print(r)
