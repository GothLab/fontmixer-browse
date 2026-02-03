"""
Merge per-folder font JSON files into a single JSON and delete originals.

Input files: any *.json in the root that match top-level folder names.
Output file: fonts_merged.json

Usage:
  python merge_fonts_json.py
"""

import json
import os


def is_folder_json(root: str, filename: str) -> bool:
    if not filename.lower().endswith(".json"):
        return False
    if filename.lower() == "fonts_merged.json":
        return False
    base = filename[:-5]
    return os.path.isdir(os.path.join(root, base))


def main() -> None:
    root = os.getcwd()
    merged: dict[str, list[dict]] = {}

    for filename in os.listdir(root):
        if is_folder_json(root, filename):
            key = filename[:-5]
            path = os.path.join(root, filename)
            with open(path, "r", encoding="utf-8") as f:
                merged[key] = json.load(f)

    output_path = os.path.join(root, "fonts_merged.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    # Delete original per-folder JSON files
    for filename in os.listdir(root):
        if is_folder_json(root, filename):
            os.remove(os.path.join(root, filename))


if __name__ == "__main__":
    main()