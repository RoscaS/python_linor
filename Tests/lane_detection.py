import cv2
import numpy as np

from Tests.grab import grab_screen
from src.Helpers import Colors
from src.Image import Image
from src.Line import Line
from src.Point import Point
from src.Settings import settings


MASK = [
	Point(10, 650),  # top right
	Point(1000, 650),  # bottom right
	Point(900, 480),  # bottom left
	Point(100, 480),  # top left
]

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


def process(image):
	processed = image.edges()
	processed = roi(processed.pixels, [np.array([i.get() for i in MASK])])
	return Image(processed)


def vanishing_strategy():
	pass

def lane_strategy():
	pass





lines_overlay = True
polygon_overlay = False

def main():
	screen_cap = grab_screen(region=(7, 33, 1019, 792))
	original = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2RGB)
	processed = Image(original).edges()
	masked = Image(roi(processed.pixels, [np.array([i.get() for i in MASK])]))
	lines = masked.find_lines()

	canvas = np.zeros_like(original)

	if lines_overlay:
		if lines is not None:
			for line in lines:
				line.draw(canvas)

	combo_image = cv2.addWeighted(original, 1, canvas, 0.4, 2)

	if polygon_overlay:
		draw_polygon(combo_image, MASK)

	# both = np.concatenate((combo_image, processed.np), axis=1)
	# cv2.imshow('Window', both)

	cv2.imshow('Window', combo_image)


# last_time = 0

while (True):
	main()

	# fps = "fps: {}".format(1 / (time.time() - last_time))
	# last_time = time.time()
	# print(fps)

	key = cv2.waitKey(25) & 0xff

	if key == ord('q'):
		cv2.destroyAllWindows()
		break

	elif key == ord('1'):
		lines_overlay = not lines_overlay

	elif key == ord('2'):
		polygon_overlay = not polygon_overlay

