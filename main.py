"""
This is a converter for Animeditor save files. It pukes out PNG images from the save file so you can use
    any other (just one) program to convert it to a (fuckin') HD video

Made by: Csabi 2022. 09. 25.
"""

import re
import os
import argparse
from PIL import Image as im


def hex_to_rgba(value):
    if value == "0":
        value = "0xff000000"
    value = value.split('0x')[1]

    while len(value) != 8:
        value = f"0{value}"

    return tuple(int(value[i:i + 2], 16) for i in (2, 4, 6, 0))


argParser = argparse.ArgumentParser()

argParser.add_argument("-f", "--file", help="Enter a qp4 format file location")

args = argParser.parse_args()

lines = ""

try:
    qpaFile = open(args.file, 'r')
    lines = qpaFile.readlines()
    qpaFile.close()
except IOError:
    print("Could not open file")
    exit(-1)

rgbList = dict(frames=[])
tempRows = dict(rows=[])

frameStart = False

frame = 0

for lin in lines:
    lin = lin.strip()
    if lin == "frame({":
        frameStart = True
        tempRows = dict(rows=[])  # {f"{frame}": []}

    end = re.search("},1000\\)", lin)
    if end:
        frameStart = False
        frame += 1

        rgbList["frames"].append(tempRows)
        continue

    if frameStart:
        rowVals = lin.split(",")
        rowVals.pop(len(rowVals) - 1)

        if not tempRows["rows"]:
            tempRows["rows"] = [rowVals]
        else:
            tempRows["rows"].append(rowVals)

img = im.new("RGBA", (32, 26), (255, 0, 0, 255))

rgbImage = list()

imgCount = 1

# Check whether the specified path exists or not
path = "images"

if not os.path.exists(path):
    # Create a new directory because it does not exist

    os.makedirs(path)
    print("Created images directory")

for frames in rgbList['frames']:
    for rows in frames['rows']:
        for row in rows:
            if row:
                rgbImage.append((hex_to_rgba(row)))

    img.putdata(rgbImage)
    rgbImage = list()
    imgIndex = imgCount + 1
    img.save(fr"{path}\img{imgIndex}.png")
    imgCount += 1

print("Done C:")

"""Not used currently.. needs to be checked."""
"""for frames in rgbList['frames']:
    if len(frames['rows'][1]) == 32:
        for row in frames['rows']:
            for rgb in row:
                if rgb:
                    rgbImage.append((hex_to_rgba(rgb)))
        img.putdata(rgbImage)
        rgbImage = list()
        img.save(fr"images\img{imgCount}.png")
        imgCount += 1

    elif len(frames['rows'][1]) > 32:
        for i in range(0, len(frames['rows'][1]) - 32, 2):
            for row in frames['rows']:
                if row:
                    for x in range(32):
                        rgbImage.append(hex_to_rgba(row[x + i]))
            img.putdata(rgbImage)
            rgbImage = list()
            img.save(fr"images\img{imgCount}.png")
            imgCount += 1
        continue"""
