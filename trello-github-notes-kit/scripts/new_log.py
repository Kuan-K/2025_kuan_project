#!/usr/bin/env python3
import argparse, os, datetime

ap = argparse.ArgumentParser()
ap.add_argument("--date", default=datetime.date.today().isoformat())
ap.add_argument("--goals", default="Goal 1|study_notes/study-note-1.md,Goal 2|study_notes/study-note-2.md")
args = ap.parse_args()

goals = []
for g in args.goals.split(","):
    g = g.strip()
    if not g: 
        continue
    if "|" in g:
        text, path = g.split("|", 1)
    else:
        text, path = g, "study_notes/study-note-1.md"
    goals.append((text.strip(), path.strip()))

lines = [f"{args.date}:\n", "\nShort term goals:"]
for i, (text, path) in enumerate(goals, start=1):
    lines.append(f"{i}. [{text}](../{path})")
lines += [
    "\nDaily logs:",
    "1. hh:mm-hh:mm: [Task 1](../study_notes/study-note-1.md#1-task-1)",
    "   (Status: TODO/Doing/Done)",
    "   Summary: ...",
    "",
    "2. hh:mm-hh:mm: [Task 2](../study_notes/study-note-1.md#2-task-2)",
    "   (Status: TODO/Doing/Done)",
    "   Summary: ...",
]
out = f"trello_mirror/{args.date}.md"
os.makedirs("trello_mirror", exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("Wrote " + out)
