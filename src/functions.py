import math

import cv2
import numpy as np

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
		# i.draw(image, ray=2, color=color, thickness=5)
		if c < len(vertices):
			line = Line(i, vertices[(c + 1) % len(vertices)])
			line.draw(image, color, thickness=1)



def line_intersection(left, right):
	slope_left = left.slope
	slope_right = right.slope

	left_y_intercept = left.y_intercept
	right_y_intercept = right.y_intercept

	if (slope_left == slope_right):
		print("PARALLEL !")
		return None

	x = (right_y_intercept - left_y_intercept) / (slope_left - slope_right)
	y = slope_left * x + left_y_intercept

	return Point(x, ((762 - 55) / 2) -y)



def strategy(lines, image):
	if lines is None: return

	left_lines, right_lines = [], []
	left_line, right_line = None, None

	for line in lines:
		slope = line.slope

		if slope < 0:
			left_lines.append(line)
		elif slope > 0:
			right_lines.append(line)

	l_avg = np.average([i.get() for i in left_lines], axis=0).tolist()
	r_avg = np.average([i.get() for i in right_lines], axis=0).tolist()

	if (type(l_avg) is list):
		left_line = Line(coords=l_avg)
		left_line.draw(image, color=Colors.blue())

	if (type(r_avg) is list):
		right_line = Line(coords=r_avg)
		right_line.draw(image, color=Colors.blue())

	if not None in [left_line, right_line]:
		intersection = line_intersection(left_line, right_line)
		intersection.draw(image, color=Colors.blue())
		print(intersection)
		return intersection

	return None




def vanishing_strategy():
	pass

def lane_strategy():
	pass

