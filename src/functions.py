"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

from typing import Tuple

import cv2
import numpy as np

from src.GUI import GUI
from src.tools.Helpers import Colors
from src.objects.Line import Line
from src.objects.Point import Point
from settings import settings
from src.tools.capture import capture_screen_region


def capture_window():
	resolution = settings["resolution"]
	x_offset = settings["x-offset"]
	y_offset = settings["y-offset"]
	return capture_screen_region(region=(x_offset, y_offset, *resolution))


def compute_mask():
	max_width = settings['resolution'][0]
	top_width = GUI.mask_top_width
	bottom_width = GUI.mask_bottom_width

	left = (max_width - top_width) / 2
	right = (max_width - bottom_width) / 2
	top_left = left
	top_right = max_width - left
	bottom_left = right
	bottom_right = max_width - right

	return [
		Point(top_left, GUI.mask_top_y),
		Point(bottom_left, GUI.mask_bottom_y),
		Point(bottom_right, GUI.mask_bottom_y),
		Point(top_right, GUI.mask_top_y),
	]


def roi(image, polygons):
	mask = np.zeros_like(image)
	cv2.fillPoly(mask, polygons, 255)
	masked = cv2.bitwise_and(image, mask)
	return masked


def draw_polygon(image, vertices, color=Colors.blue()):
	for c, i in enumerate(vertices):
		if c < len(vertices):
			line = Line(i, vertices[(c + 1) % len(vertices)])
			line.draw(image, color, thickness=1)


def compute_averages(lines):
	left_lines = [i for i in lines if i.slope < 0]
	right_lines = [i for i in lines if i.slope > 0]
	return Line.average(left_lines), Line.average(right_lines)

def update_smoothing(lines, smoothing):
	if lines[0] is not None:
		smoothing.add_left_line(lines[0])

	if lines[1] is not None:
		smoothing.add_right_line(lines[1])

def compute_vanishing_point(lines: Tuple[Line or None, Line or None]) -> Point:
	if not None in [lines]:
		intersection = lines[0].intersects(lines[1])
		return intersection or Point(0, 0)
	return Point(0, 0)

