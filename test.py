# requires: pip install fonttools
# run in folder with fonts: python list_fonts.py

import os, csv
from fontTools.ttLib import TTFont

out = "fonts_extended.csv"

def get_name(font, nameID):
    try:
        for r in font["name"].names:
            if r.nameID == nameID:
                return r.toUnicode()
    except:
        pass
    return ""

with open(out, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(
        f,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        lineterminator="\n"
    )

    writer.writerow(["filename", "font_name", "designer", "description", "license", "license_url"])

    for file in os.listdir("."):
        if file.lower().endswith((".ttf", ".otf")):
            try:
                font = TTFont(file)
                writer.writerow([
                    file,
                    get_name(font, 4),   # full font name
                    get_name(font, 9),   # designer / studio
                    get_name(font, 10),  # description
                    get_name(font, 13),  # license
                    get_name(font, 14)   # license URL
                ])
            except:
                writer.writerow([file, "", "", "", "", ""])
