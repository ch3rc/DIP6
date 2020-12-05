"""
Author:     Cody Hawkins
Date:       11/25/2020
Class:      5420
Proj:       Assignment 6
Desc:       Highlight a rectangle area of an image
            get the equalized histogram of highlighted
            area and dim the rest of the image.
"""

import os
import sys
import getopt
import cv2 as cv
import numpy as np
from find_image import img_path

ref_point = []
drawing = False
image = None
ix, iy = -1, -1


def help():
    print("\t\t------HELP--------\n")
    print("To run, please provide an image name")
    print("Highlight a rectangle area in the image")
    print("The highlighted area will then get focused in")
    print("The rest of the image will be blurred")
    print("Press q to quit the program")


def picture_selection(event, x, y, flags, param):
    global ref_point, image, drawing, ix, iy

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        # get initial points
        ref_point = [(x, y)]
        ix, iy = ref_point[0]

    elif event == cv.EVENT_MOUSEMOVE:
        # while holding the left mouse button down draw a rectangle
        if drawing:
            copy = image.copy()
            cv.rectangle(copy, (ix, iy), (x, y), (255, 0, 0), 1)
            cv.imshow("image", copy)

    elif event == cv.EVENT_LBUTTONUP:
        (x_ref, y_ref) = ref_point[0]

        drawing = False

        # if you start from any position but top left, switch starting and ending points
        if x_ref > x:
            (x, x_ref) = (x_ref, x)
        if y_ref > y:
            (y, y_ref) = (y_ref, y)

        if len(image.shape) == 2:
            # create copy of original image
            temp = image.copy()
            # mask for dimming image
            rectangle = np.full((image.shape[0], image.shape[1]), 0.75, dtype=np.float32)
            image = image.astype(np.float32)
            image = image * rectangle
            image = image.astype(np.uint8)
            # equalized portion of image highlighted by rectangle
            equ = cv.equalizeHist(temp[y_ref:y, x_ref:x])
            # add equalized image to dimmed image
            image[y_ref:y, x_ref:x] = equ
            cv.imshow("image", image)

        elif len(image.shape) == 3:
            temp = image.copy()
            rectangle = np.full((image.shape[0], image.shape[1], 3), 0.75, dtype=np.float32)
            image = image.astype(np.float32)
            image = image * rectangle
            image = image.astype(np.uint8)
            # convert BGR to HSV
            temp = cv.cvtColor(temp, cv.COLOR_BGR2HSV)
            H, S, V = cv.split(temp[y_ref:y, x_ref:x])
            # equalize value channel
            V_equ = cv.equalizeHist(V)
            # convert back to BGR
            equ = cv.cvtColor(cv.merge((H, S, V_equ)), cv.COLOR_HSV2BGR)
            image[y_ref:y, x_ref:x] = equ
            cv.imshow("image", image)


def pic_highlight(args):
    img_name = args[0]
    search_directory = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"
    img = img_path(img_name, search_directory)

    try:
        global image
        image = cv.imread(img)
        cv.namedWindow("image")
        cv.setMouseCallback("image", picture_selection)

        cv.imshow("image", image)
        key = cv.waitKey(0) & 0xFF
        if key == 113:
            cv.destroyAllWindows()
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
        pic_highlight(args)
    elif len(args) == 0:
        print("Image name not provided! Please see instructions.\n")
        help()
    elif len(args) > 1:
        print("Too many image names provided! Please see instructions.\n")
        help()


if __name__ == "__main__":
    main()