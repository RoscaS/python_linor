import cv2
import numpy as np

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



def vanishing_strategy():
	pass

def lane_strategy():
	pass

