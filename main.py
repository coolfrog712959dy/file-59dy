#!/usr/bin/env python3
"""File deduplication utility."""

import os
import hashlib
import argparse
import sys

def file_hash(path, block_size=65536):
    """Return SHA256 hash of the file at *path*."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                h.update(block)
    except OSError as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return None
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Find and optionally delete duplicate files.")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--delete", action="store_true", help="Delete duplicates, keep first instance")
    args = parser.parse_args()

    hashes = {}
    for root, _, files in os.walk(args.directory):
        for name in files:
            path = os.path.join(root, name)
            h = file_hash(path)
            if h:
                hashes.setdefault(h, []).append(path)

    for h, paths in hashes.items():
        if len(paths) > 1:
            print(f"Duplicate group ({h}):")
            for p in paths:
                print(f"  {p}")
            if args.delete:
                for p in paths[1:]:
                    try:
                        os.remove(p)
                        print(f"  Deleted {p}")
                    except OSError as e:
                        print(f"  Could not delete {p}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()