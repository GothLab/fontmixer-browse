"""
Create per-folder CSV files (3 columns) from font metadata.

Requirements:
  pip install fonttools

Usage:
  Run from the root folder that contains font subfolders:
    python list_fonts_3col.py
"""

import csv
import os
from collections import defaultdict

from fontTools.ttLib import TTFont


def get_name(font: TTFont, name_id: int) -> str:
    try:
        for record in font["name"].names:
            if record.nameID == name_id:
                return record.toUnicode()
    except Exception:
        pass
    return ""


def merge_details(font: TTFont) -> str:
    parts = [
        get_name(font, 10),  # description
        get_name(font, 13),  # license
        get_name(font, 14),  # license URL
        get_name(font, 9),   # designer / studio
    ]
    parts = [p.strip() for p in parts if p.strip()]
    return " | ".join(parts)


def top_level_folder(root: str, path: str) -> str:
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    return parts[0] if parts else ""


def collect_fonts(root: str) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith((".ttf", ".otf")):
                full_path = os.path.join(dirpath, filename)
                folder = top_level_folder(root, full_path)
                groups[folder].append(full_path)
    return groups


def write_csv(root: str, folder: str, files: list[str]) -> None:
    output_path = os.path.join(root, f"{folder}.csv")
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(
            f,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writerow(["filename", "font_name", "details"])

        for file_path in sorted(files):
            filename = os.path.basename(file_path)
            try:
                font = TTFont(file_path)
                writer.writerow([
                    filename,
                    get_name(font, 4),  # full font name
                    merge_details(font),
                ])
            except Exception:
                writer.writerow([filename, "", ""])


def main() -> None:
    root = os.getcwd()
    groups = collect_fonts(root)
    for folder, files in groups.items():
        if folder and os.path.isdir(os.path.join(root, folder)):
            write_csv(root, folder, files)


if __name__ == "__main__":
    main()