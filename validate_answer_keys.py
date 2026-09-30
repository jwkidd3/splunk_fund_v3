#!/usr/bin/env python3
"""
Answer-Key and Literal-Value Validation

The other two validators check structure and field *names*. This one closes the
gaps that let broken content through:

1. Every literal `field=value` filter in every lab AND both presentations is
   resolved against the actual generated data. Searches written with inline
   backticks (Lab 2) are checked too, not just fenced ```spl blocks.
2. Every data-derived answer-key value is recomputed from the data files and
   must still appear in its lab.

Run after regenerating data or editing labs:
    python3 validate_answer_keys.py
"""

import collections
import csv
import glob
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA = Path(__file__).parent / "labs" / "data"

# Query text that is deliberately not a course-data search
SKIP_QUERY = ("index=_audit", "/services/", "should be", "both work")
# Right-hand sides that are field names or aliases, not literal values
SKIP_VALUE = {"productId", "product_name", "price", "ProductName", "Price",
              "now", "Default"}


def load():
    access = (DATA / "access_30DAY.log").read_text().splitlines()
    db = list(csv.DictReader((DATA / "db_audit_30DAY.csv").open()))
    products = {r["productId"]: r for r in csv.DictReader((DATA / "products.csv").open())}
    return access, db, products


def path_of(line):
    m = re.search(r'"(?:GET|POST) ([^ ?"]+)', line)
    return m.group(1).split("/")[-1] if m else None


def first(pattern, line):
    m = re.search(pattern, line)
    return m.group(1) if m else None


def domains(access, db):
    blob = "\n".join(access)
    return {
        "action": set(re.findall(r"action=(\w+)", blob)),
        "status": set(re.findall(r'" (\d{3}) ', blob)),
        "file": set(filter(None, (path_of(l) for l in access))),
        "categoryId": set(re.findall(r"categoryId=(\w+)", blob)),
        "productId": set(re.findall(r"productId=([\w-]+)", blob)),
        "clientip": set(l.split(" ")[0] for l in access),
        "Type": set(r["Type"] for r in db),
        "sourcetype": {"access_combined_wcookie", "linux_secure", "db_audit"},
        "index": {"main", "_audit", "_internal"},
        "host": {"web_application", "web_server", "database"},
    }


def check_filters(dom):
    """Every literal field=value in labs and slides must exist in the data."""
    bad = []
    for path in sorted(glob.glob("labs/*.md")) + sorted(glob.glob("presentations/*.html")):
        text = Path(path).read_text()
        queries = (re.findall(r"```(?:spl|bash)?\n(.*?)```", text, re.S)
                   + re.findall(r"`([^`\n]{4,200})`", text)      # Lab 2 style
                   + re.findall(r"<code>(.*?)</code>", text, re.S))
        for q in queries:
            if any(s in q for s in SKIP_QUERY):
                continue
            for field, value in re.findall(r'\b(\w+)\s*=\s*"?([\w.\-/*]+)"?', q):
                if field not in dom or "*" in value or value in SKIP_VALUE:
                    continue
                if value not in dom[field]:
                    bad.append((os.path.basename(path), f"{field}={value}"))
    return sorted(set(bad))


def expected(access, db, products):
    """Recompute every data-derived answer-key value."""
    blob = "\n".join(access)
    ok = [l for l in access if '" 200 ' in l]
    buy = [l for l in ok if path_of(l) == "success.do"]
    files = collections.Counter(path_of(l) for l in ok)

    sessions = collections.defaultdict(set)
    for l in access:
        sid = first(r"JSESSIONID=(\w+)", l)
        if sid:
            sessions[l.split(" ")[0]].add(sid)
    top_ip_sessions = max((len(v), k) for k, v in sessions.items())

    forbidden = collections.Counter(l.split(" ")[0] for l in access if '" 403 ' in l)

    bandwidth = collections.Counter()
    for l in ok:
        b = first(r'" 200 (\d+) ', l)
        if b:
            bandwidth[path_of(l)] += int(b)

    revenue = collections.Counter()
    for l in buy:
        pid = first(r"productId=([\w-]+)", l)
        if pid in products:
            revenue[products[pid]["product_name"]] += float(products[pid]["price"])

    sold = collections.Counter(first(r"productId=([\w-]+)", l) for l in buy)
    carted = collections.Counter(first(r"productId=([\w-]+)", l)
                                 for l in access if "action=addtocart" in l)

    return [
        ("lab5", "best-selling product", sold.most_common(1)[0][0]),
        ("lab5", "cart.do (status=200)", f"{files['cart.do']:,}"),
        ("lab5", "success.do (status=200)", f"{files['success.do']:,}"),
        ("lab5", "top IP by sessions", top_ip_sessions[1]),
        ("lab5", "that IP's session count", f"{top_ip_sessions[0]:,}"),
        ("lab5", "least-bandwidth file", min(bandwidth.items(), key=lambda x: x[1])[0]),
        ("lab6", "top 403 IP", forbidden.most_common(1)[0][0]),
        ("lab6", "that IP's 403 count", str(forbidden.most_common(1)[0][1])),
        ("lab6", "total 403 events", f"{sum(forbidden.values()):,}"),
        ("lab6", "units sold", f"{len(buy):,}"),
        ("lab6", "cart additions", f"{len(re.findall('action=addtocart', blob)):,}"),
        ("lab6", "purchases", f"{len(re.findall('action=purchase', blob)):,}"),
        ("lab6", "unique sessions", f"{len(set().union(*sessions.values())):,}"),
        ("lab7", "top carted product", carted.most_common(1)[0][0]),
        ("lab8", "top revenue product", revenue.most_common(1)[0][0]),
        ("lab8", "top revenue amount", f"{revenue.most_common(1)[0][1]:,.2f}"),
    ]


def check_funnel(access):
    """The funnel must narrow: views > cart additions > purchases."""
    blob = "\n".join(access)
    views = sum(1 for l in access if "/product.screen" in l)
    adds = len(re.findall("action=addtocart", blob))
    buys = len(re.findall("action=purchase", blob))
    return views, adds, buys, views > adds > buys


def check_window(access, preset_days=30):
    """The whole dataset must sit inside the search preset the labs tell students
    to use. The answer keys are computed over every event in the file, so if the
    preset no longer reaches the oldest event, students see smaller numbers than
    the keys claim. Returns (oldest, newest, events_outside, slack_days)."""
    stamps = [datetime.strptime(re.search(r"\[([^\]]+)\]", l).group(1),
                                "%d/%b/%Y:%H:%M:%S") for l in access]
    oldest, newest = min(stamps), max(stamps)
    cutoff = datetime.now() - timedelta(days=preset_days)
    outside = sum(1 for t in stamps if t < cutoff)
    slack = (oldest - cutoff).total_seconds() / 86400
    return oldest, newest, outside, slack


def main():
    os.chdir(Path(__file__).parent)
    access, db, products = load()
    dom = domains(access, db)
    failures = 0

    print("\n🔎 Literal field=value filters (labs + presentations)")
    bad = check_filters(dom)
    for path, pair in bad:
        print(f"  ❌ {path}: {pair} does not exist in the data")
    if not bad:
        print("  ✓ every literal filter resolves to real data")
    failures += len(bad)

    print("\n🔑 Answer-key values")
    lab_text = {p.name: p.read_text() for p in Path("labs").glob("*.md")}
    for lab, label, value in expected(access, db, products):
        found = any(value in t for name, t in lab_text.items() if name.startswith(lab))
        if found:
            print(f"  ✓ {lab}: {label} = {value}")
        else:
            print(f"  ❌ {lab}: {label} should be {value} — not found in the lab")
            failures += 1

    print("\n📉 Conversion funnel")
    views, adds, buys, sane = check_funnel(access)
    print(f"  {'✓' if sane else '❌'} views {views:,} > cart {adds:,} > purchases {buys:,}"
          f"  ({100 * buys / adds:.1f}% conversion)")
    failures += 0 if sane else 1

    print("\n📅 Data window vs the 'Last 30 days' preset the labs use")
    oldest, newest, outside, slack = check_window(access)
    print(f"  data spans {oldest.date()} → {newest.date()}"
          f"  (newest event {(datetime.now() - newest).total_seconds() / 3600:.0f}h old)")
    if outside:
        print(f"  ❌ {outside:,} events fall outside 'Last 30 days' — students will see "
              f"smaller counts than the answer keys claim.")
        print("     Fix: cd labs/data && python3 generate_course_data.py")
        failures += 1
    else:
        print(f"  ✓ all {len(access):,} events are inside the preset "
              f"({slack:.1f} days of slack left)")
        if slack < 1:
            print("  ⚠️  under 1 day of slack — regenerate before delivering the class")

    print("\n" + "=" * 62)
    if failures:
        print(f"❌ {failures} problem(s) found")
        return 1
    print("✅ Answer keys and literal values all match the generated data")
    return 0


if __name__ == "__main__":
    sys.exit(main())
