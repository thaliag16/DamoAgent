#!/usr/bin/env python3
"""adsearch — search Aswath Damodaran's blog, Musings on Markets (683+ posts since 2008).

  adsearch.py nvidia                  posts mentioning Nvidia, newest first
  adsearch.py "young companies" -n 20
  adsearch.py --recent 10             the latest posts

Uses the public Blogger feed for aswathdamodaran.blogspot.com. The same posts appear
on his Substack (aswathdamodaran.substack.com). Read the post itself (WebFetch the URL)
before relying on it: this tool only finds it.
"""
import argparse
import html
import re
import json
import urllib.parse
import urllib.request

FEED = "https://aswathdamodaran.blogspot.com/feeds/posts/summary?alt=json"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("terms", nargs="*")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--recent", type=int)
    a = p.parse_args()
    n = a.recent or a.n
    url = f"{FEED}&max-results={n}"
    if a.terms and not a.recent:
        url += "&q=" + urllib.parse.quote(" ".join(a.terms))
    req = urllib.request.Request(url, headers={"User-Agent": "damostack/1.0"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    entries = data["feed"].get("entry", [])
    if not entries:
        print("No posts found. Try fewer or different words.")
    for e in entries:
        link = next(x["href"] for x in e["link"] if x["rel"] == "alternate")
        summ = re.sub(r"\s+", " ", html.unescape(e.get("summary", {}).get("$t", ""))).strip()[:220]
        print(f"{e['published']['$t'][:10]}  {e['title']['$t']}\n  {link}\n  {summ}…\n")


if __name__ == "__main__":
    main()
