#! /home/singh/.virtualenvs/cv/bin/python

import cv2
import numpy as np


def get_centers(frame):
    gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=35, minRadius=0, maxRadius=200)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
    return circles
