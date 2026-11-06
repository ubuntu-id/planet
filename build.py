#!/usr/bin/env python3
"""Bangun Planet Ubuntu-ID menjadi situs statis di public/.

Membaca config.ini (format lama Planet Venus), mengambil semua feed,
lalu merender index.html, rss20.xml, dan opml.xml dengan template Jinja2.
"""
import configparser
import shutil
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import feedparser
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
OUT = ROOT / "public"
THEME_DIRS = ("css", "images", "heads")
AGENT = "PlanetUbuntuID/2.0 (+https://github.com/ubuntu-id/planet)"

TIMEOUT = 15


def load_config():
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(ROOT / "config.ini", encoding="utf-8")
    return cp


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            d = feedparser.parse(r.read(), response_headers={"content-location": r.geturl()})
    except Exception as e:
        print(f"GAGAL  {url}: {e}", file=sys.stderr)
        return url, None
    if d.bozo and not d.entries:
        print(f"GAGAL  {url}: {d.get('bozo_exception')}", file=sys.stderr)
        return url, None
    return url, d


def to_dt(entry):
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if not t:
        return None
    return datetime(*t[:6], tzinfo=timezone.utc)


def entry_content(entry):
    if entry.get("content"):
        return entry.content[0].value
    return entry.get("summary", "")


def main():
    cp = load_config()
    planet = cp["Planet"]
    feeds = [s for s in cp.sections() if s.startswith(("http://", "https://"))]
    per_feed = planet.getint("new_feed_items", 5)
    per_page = planet.getint("items_per_page", 20)
    date_fmt = planet.get("date_format", "%d %b %Y %I:%M %p")
    day_fmt = planet.get("new_date_format", "%d %b %Y")
    now = datetime.now(timezone.utc)

    with ThreadPoolExecutor(16) as ex:
        results = list(ex.map(fetch, feeds))

    items, channels = [], []
    for url, d in results:
        sec = cp[url]
        face = sec.get("face", "anon.png")
        if not (ROOT / "heads" / face).exists():
            face = "anon.png"
        ch = {"url": url, "name": sec.get("name", url), "link": "", "title": sec.get("name", url)}
        if d:
            ch["link"] = d.feed.get("link", "")
            ch["title"] = d.feed.get("title", ch["name"])
            for e in d.entries:
                dt = to_dt(e)
                if not dt or dt > now:
                    continue
                items.append({
                    "dt": dt,
                    "id": e.get("id") or e.get("link", ""),
                    "link": e.get("link", ""),
                    "title": e.get("title", "(tanpa judul)"),
                    "title_plain": e.get("title", ""),
                    "content": entry_content(e),
                    "category": ", ".join(t.term for t in e.get("tags", []) if t.get("term")),
                    "channel_name": ch["name"],
                    "channel_title": ch["title"],
                    "face": face,
                })
        channels.append(ch)

    # Batasi per feed, lalu urutkan global terbaru dulu.
    by_feed = {}
    for it in sorted(items, key=lambda i: i["dt"], reverse=True):
        by_feed.setdefault(it["channel_name"], []).append(it)
    items = sorted((i for v in by_feed.values() for i in v[:per_feed]),
                   key=lambda i: i["dt"], reverse=True)[:per_page]

    last_day = None
    for it in items:
        day = it["dt"].strftime(day_fmt)
        it["new_date"] = day if day != last_day else ""
        last_day = day
        it["date"] = it["dt"].strftime(date_fmt)
        it["date_822"] = format_datetime(it["dt"])

    channels.sort(key=lambda c: c["name"].lower())
    ctx = {
        "name": planet["name"],
        "link": planet["link"],
        "owner_name": planet.get("owner_name", ""),
        "owner_email": planet.get("owner_email", ""),
        "items": items,
        "channels": channels,
        "now_822": format_datetime(now),
    }

    # Autoescape aktif untuk semua *.j2; konten feed sudah disanitasi feedparser.
    env = Environment(loader=FileSystemLoader(ROOT), autoescape=select_autoescape(["j2"]))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "ubuntu").mkdir(parents=True)
    for tpl, target in (("index.html.j2", "index.html"),
                        ("rss20.xml.j2", "rss20.xml"),
                        ("opml.xml.j2", "opml.xml")):
        (OUT / target).write_text(env.get_template(tpl).render(**ctx), encoding="utf-8")
    shutil.copy(ROOT / "style.css", OUT / "ubuntu" / "style.css")
    for d in THEME_DIRS:
        shutil.copytree(ROOT / d, OUT / "ubuntu" / d)
    shutil.copy(ROOT / "images" / "favicon.ico", OUT / "favicon.ico")

    ok = sum(1 for _, d in results if d)
    print(f"Selesai: {len(items)} entri, {ok}/{len(feeds)} feed berhasil -> {OUT}")


if __name__ == "__main__":
    main()
