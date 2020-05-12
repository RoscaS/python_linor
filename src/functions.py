import math
from typing import Tuple

import cv2
import numpy as np

from src.GUI import GUI
from src.Helpers import Colors
from src.Line import Line
from src.Point import Point
from src.Settings import settings
from src.grab import capture_screen_region


def capture_window():
	resolution = settings["resolution"]
	x_offset = settings["x-offset"]
	y_offset = settings["y-offset"]
	return capture_screen_region(region=(x_offset, y_offset, *resolution))

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


def strategy(lines: Tuple[Line or None, Line or None]) -> Point or None:
	if GUI.vanishing_point_strategy:
		return vanishing_strategy(lines)
	else:
		return lane_strategy(lines)


def vanishing_strategy(lines: Tuple[Line or None, Line or None]) -> Point or None:
	if not None in [lines]:
		intersection = lines[0].intersects(lines[1])
		return intersection
	return None

def lane_strategy(lines: Tuple[Line or None, Line or None]) -> Point or None:
	pass

