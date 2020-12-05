"""
Author:     Cody Hawkins
Date:       12/4/2020
Class:      5420
File:       LUT.py
Desc:       Create equalized look up table and probability
            table, return both
"""


def get_Lut(image):
    # made LUT its own function so i could reuse it for the
    # other histogram functions.
    transformation = [0 for x in range(256)]
    LUT = [0 for x in range(256)]
    probs =[]

    R, C = image.shape[:2]
    # get counts of unique pixel values
    for i in range(R):
        for j in range(C):
            transformation[image[i][j]] += 1

    # equalize pixel values and place in Look Up Table
    for i in range(len(transformation)):
        transformation[i] = transformation[i] / image.size
        probs.append(transformation[i])
        if i > 0:
            transformation[i] += transformation[i - 1]

    for i in range(len(transformation)):
        LUT[i] = int(transformation[i] * 255)

    return probs, LUT