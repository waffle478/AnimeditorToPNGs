
"""
This is a converter for Animeditor save files. It pukes out PNG images from the save file so you can use
    any other (just one) program to convert it to a (fuckin') HD video

Made by: Csabi 2022. 09. 25.
"""

import re
from PIL import Image as im
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def hex_to_rgba(value):
    if value == "0":
        value = "0xff000000"
    value = value.split('0x')[1]

    while len(value) != 8:
        value = f"0{value}"

    return tuple(int(value[i:i + 2], 16) for i in (2, 4, 6, 0))

Tk().withdraw()
file = askopenfilename(filetypes=[("Default Qpa save file", '*.qp4')])
qpaFile = open(file, 'r')
lines = qpaFile.readlines()
qpaFile.close()

rgbList = dict(frames=[])
tempRows = dict(rows=[])

frameStart = False

frame = 0

for lin in lines:
    lin = lin.strip()
    if lin == "frame({":
        frameStart = True
        tempRows = dict(rows=[]) #{f"{frame}": []}

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

imgCount = 0

for frames in rgbList['frames']:
    for rows in frames['rows']:
        for row in rows:
            if row:
                rgbImage.append((hex_to_rgba(row)))

    img.putdata(rgbImage)
    rgbImage = list()
    img.save(fr"images\img{imgCount}.png")
    imgCount += 1

print("Done C:")
