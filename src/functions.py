import math

import cv2
import numpy as np

from src.GUI import GUI
from src.Helpers import Colors
from src.Line import Line
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
		# i.draw(image, ray=2, color=color, thickness=5)
		if c < len(vertices):
			line = Line(i, vertices[(c + 1) % len(vertices)])
			line.draw(image, color, thickness=1)


def strategy(lines, image):
	if GUI.vanishing_point_strategy:
		vanishing_strategy(lines, image)
	else:
		lane_strategy(lines, image)


def vanishing_strategy(lines, image):
	if lines is None:
		return None

	left_lines = [i for i in lines if i.slope < 0]
	right_lines = [i for i in lines if i.slope > 0]

	left_average = Line.average(left_lines)
	right_average = Line.average(right_lines)

	if left_average is not None:
		left_average.draw(image, color=Colors.blue())

	if right_average is not None:
		right_average.draw(image, color=Colors.blue())

	if not None in [left_average, right_average]:
		intersection = left_average.intersects(right_average)
		intersection.draw(image, color=Colors.blue(), thickness=5)

		return intersection

	return None

def lane_strategy(lines, image):
	pass

