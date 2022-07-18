#!/usr/bin/env python3

import os
import csv
import xml.dom.minidom


X_TRANSLATE = (23.233, 78.333334, 133.433)
Y_TRANSLATE = (26.110997, 108.21131, 190.311)

CARD_TEMPLATE_FILE = str(os.getcwd()) + "/sniðmát/55x82.svg"
DATABASE_FILE = str(os.getcwd()) + "/gagnasafn.csv"
IMAGE_DIR = str(os.getcwd()) + "/myndir"
PRINTABLES_DIR = str(os.getcwd()) + "/printables"
A4_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1">
{content}
</svg>
"""


def get_card_template():
    DOMTree = xml.dom.minidom.parse(CARD_TEMPLATE_FILE)
    g = DOMTree.documentElement.getElementsByTagName("g")[0]
    return g.toxml()


def open_database():
    with open(DATABASE_FILE) as f:
        database = csv.DictReader(f)
        rows = list(database)
    return rows


def get_image_url(number):
    files = os.listdir(IMAGE_DIR)
    image = [img for img in files if img.startswith(f"{number:03}")]
    if not image:
        return ""
    image_url = f"file://{IMAGE_DIR}/{image[0]}"
    return image_url


def fill_template(template, row):
    number = int(row["Númer Dýrs"])
    if row["Afkvæmi avg"] != "":
        offsprings = row["Afkvæmi avg"]
    else:
        offsprings = row["Afkvæmi min"] + " - " + row["Afkvæmi max"]

    if row["Líftími avg"] != "":
        longevity = row["Líftími avg"]
    else:
        longevity = row["Líftími min"] + " - " + row["Líftími max"]

    if row["Þyngd avg"] != "":
        weight = row["Þyngd avg"]
    else:
        weight = row["Þyngd min"] + " - " + row["Þyngd max"]

    if row["Lengd avg"] != "":
        length = row["Lengd avg"]
    else:
        length = row["Lengd min"] + " - " + row["Lengd max"]

    scientific_name_length = str(len(row["Fræðiheiti"].strip().replace(" ", "")))

    output = template
    output = output.replace("#CARD_NUMBER", str(number))
    output = output.replace("#NAME", row["Nafn Dýrs"])
    output = output.replace("#SCIENTIFIC_NAME_LENGTH", scientific_name_length)
    output = output.replace("#SCIENTIFIC_NAME", row["Fræðiheiti"])
    output = output.replace("#OFFSPRINGS", offsprings)
    output = output.replace("#LONGEVITY", longevity)
    output = output.replace("#FEET", row["Fætur"])
    output = output.replace("#WEIGHT", weight)
    output = output.replace("#LENGTH", length)
    #output = output.replace("#IMAGE_REFERENCE", row["Vísun í mynd á spjaldi"])
    output = output.replace("#IMAGE_URL", get_image_url(number))
    return output


def main():
    card_template = get_card_template()
    rows = open_database()
    groups = [fill_template(card_template, row) for row in rows]

    printable = 1
    start = 0
    end = 9

    while start < len(groups):
        page = groups[start:end]
        content = []
        for i, card in enumerate(page):
            t_x = X_TRANSLATE[i % 3]
            t_y = Y_TRANSLATE[i // 3]
            content.append(f'<g transform="translate({t_x}, {t_y})">{card}</g>')

        a4_svg = A4_TEMPLATE.format(content="\n".join(content))
        with open(f"{PRINTABLES_DIR}/page_{printable:02}.svg", "w") as f:
            f.write(a4_svg)

        printable += 1
        start += 9
        end += 9


main()
