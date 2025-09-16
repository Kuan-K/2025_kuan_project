#!/usr/bin/env python3
import os, sys

def tree(dir_path, prefix=""):
    entries = sorted([e for e in os.listdir(dir_path) if not e.startswith(".")])
    for i, name in enumerate(entries):
        path = os.path.join(dir_path, name)
        connector = "└─ " if i == len(entries) - 1 else "├─ "
        print(prefix + connector + name)
        if os.path.isdir(path):
            extension = "   " if i == len(entries) - 1 else "│  "
            tree(path, prefix + extension)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(root)
    tree(root)
