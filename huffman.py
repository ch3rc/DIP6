"""
Author:     Cody Hawkins
Date:       11/25/2020
Class:      5420
Proj:       Assignment 6
Desc:       Get histogram LUT and then
            convert LUT values into huffman codes
            write to a file and find the entropy and
            compression ratio
"""

import os
import sys
import getopt
import cv2 as cv
import numpy as np
from find_image import img_path
from LUT import get_Lut
from huff_algo import huffman_encode
from collections import defaultdict
import math


def help():
    print("\t\t------HELP--------\n")
    print("To run, please provide an image name")
    print("Program writes huffman codes to a file")
    print("Entropy and compression ration are then calculated")


def L_avg_bits(codes, probs):
    holder = []
    for p in codes:
        holder.append((probs[p[0]], len(p[1])))

    # Lavg bit length
    Lavg = 0.0
    for prob, length in holder:
        Lavg += prob * length

    return Lavg


def comp_R(avg):
    return 8 / avg


def entropy(probs):
    sum = 0.0
    for prob in probs:
        if prob != 0:
            sum += prob * math.log2(prob)

    return sum * (-1)


def huffman_codes(args):
    img_name = args[0]
    search_directory = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"
    img = img_path(img_name, search_directory)
    try:
        # read in image as grayscale
        image = cv.imread(img, 0)
        probs, lut = get_Lut(image)

        frequency = defaultdict(int)

        # Frequency count of pixel intensities
        for num in lut:
            frequency[num] += 1

        # Remove zeros from frequency count
        del frequency[0]

        codes = huffman_encode(frequency)

        # write pixel #, length and huffman code to txt file
        with open("huffman.txt", "w") as f:
            for i in range(len(lut)):
                if lut[i] == 0:
                    f.write("Pixel #: {}\t Pixel length: {}\t Binary value: {}\n".format(i, 0, ''))
                else:
                    for p in sorted(codes):
                        if p[0] == lut[i]:
                            f.write("Pixel #: {}\t Pixel length: {}\t Binary value: {}\n".format(i, len(p[1]), p[1]))
        f.close()

        Lavg = L_avg_bits(codes, probs)

        print("Lavg {:.2f} compression ratio {:.2f} entropy {:.2f}".format(Lavg, comp_R(Lavg), entropy(probs)))

    except cv.error as err:
        print(err)
        sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(1)
        else:
            assert False, "Unhandled Option!"

    if len(args) == 1:
        huffman_codes(args)
    elif len(args) == 0:
        print("Image name not provided! Please see instructions.\n")
        help()
    elif len(args) > 1:
        print("Too many image names provided! Please see instructions.\n")
        help()


if __name__ == "__main__":
    main()