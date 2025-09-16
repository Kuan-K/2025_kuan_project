#!/usr/bin/env python3
import sys, re, unicodedata
def slugify(s: str) -> str:
    s = s.strip().lower()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[^\w\s\-一-鿿]+", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mkanchor.py \"<heading text>\"")
        sys.exit(1)
    print(slugify(" ".join(sys.argv[1:])))
