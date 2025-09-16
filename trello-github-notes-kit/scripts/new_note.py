#!/usr/bin/env python3
import argparse, os, re, unicodedata

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[^\w\s\-一-鿿]+", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s

ap = argparse.ArgumentParser()
ap.add_argument("title")
ap.add_argument("--tasks", default="Task 1,Task 2,Task 3")
ap.add_argument("--out", default="study_notes/study-note-new.md")
args = ap.parse_args()

tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
toc_lines = []
body_lines = []

for i, t in enumerate(tasks, start=1):
    heading = f"{i}. {t}"
    anchor = slugify(heading)
    toc_lines.append(f"{i}. [{t}](#{anchor})")
    body_lines += [
        "---",
        "",
        f"## {heading}",
        "Goal: ",
        "Status: TODO",
        "",
        "Steps",
        "- [ ] step 1",
        "",
        "Summary / Output",
        "- ...",
        ""
    ]

content = "# Study Note: " + args.title + "\n\n## TOC\n" + "\n".join(toc_lines) + "\n\n" + "\n".join(body_lines) + "\n"
os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, "w", encoding="utf-8") as f:
    f.write(content)
print("Wrote " + args.out)
