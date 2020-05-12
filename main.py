import random

import cv2
import numpy as np

from src.GUI import GUI
from src.Image import Image
from src.Point import Point
from src.functions import roi, draw_polygon, capture_window, strategy

MASK = [
	Point(10, 650),  # top right
	Point(1000, 650),  # bottom right
	Point(900, 480),  # bottom left
	Point(100, 480),  # top left
]


def rand_color():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return r, g, b


def main():

	# Image capture
	screen_cap = capture_window()
	original = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2RGB)
	canvas = np.zeros_like(original)

	# Image processing
	grayed = Image(original).gray()
	blurred = grayed.gaussian_blur()
	processed = blurred.canny()
	masked = Image(roi(processed.pixels, [np.array([i.get() for i in MASK])]))

	# Data transformation
	lines = masked.find_lines()

	# Strategy
	strategy(lines, canvas)

	# Handle result window
	if GUI.lines_overlay:
		if lines is not None:
			for line in lines:
				pass
				# line.draw(canvas, color=rand_color())
				# line.draw(canvas)

	combo_image = cv2.addWeighted(original, 1, canvas, 0.4, 2)
	if GUI.polygon_overlay:
		draw_polygon(combo_image, MASK)

	#### GUI ####

	# Handle texts
	GUI.draw(combo_image)

	# Handle split image layout
	if GUI.process_overlay:
		left = combo_image

		if GUI.grayed_overlay:
			right = grayed.np
		elif GUI.blured_overlay:
			right = blurred.np
		elif GUI.processed_overlay:
			right = processed.np
		elif GUI.masked_overlay:
			right = masked.np
		else:
			right = original

		both = np.concatenate((left, right), axis=1)
		cv2.imshow('Linor window', both)
	else:
		cv2.imshow('Linor window', combo_image)


if __name__ == '__main__':

	while (True):
		main()

		key = cv2.waitKey(25) & 0xff

		if key == ord('q'):
			cv2.destroyAllWindows()
			break

		elif key == ord('1'):
			GUI.lines_overlay = not GUI.lines_overlay

		elif key == ord('2'):
			GUI.polygon_overlay = not GUI.polygon_overlay

		elif key == ord('s'):
			GUI.vanishing_point_strategy = not GUI.vanishing_point_strategy

		elif key == ord('3'):
			GUI.clear_overlays()
			GUI.process_overlay = not GUI.process_overlay

		elif key == ord('4') and GUI.process_overlay:
			GUI.clear_overlays()
			GUI.grayed_overlay = not GUI.grayed_overlay

		elif key == ord('5') and GUI.process_overlay:
			GUI.clear_overlays()
			GUI.blured_overlay = not GUI.blured_overlay

		elif key == ord('6') and GUI.process_overlay:
			GUI.clear_overlays()
			GUI.processed_overlay = not GUI.processed_overlay

		elif key == ord('7') and GUI.process_overlay:
			GUI.clear_overlays()
			GUI.masked_overlay = not GUI.masked_overlay



# last_time = 0
# while (True):
# 	main()
#
# 	fps = "fps: {}".format(1 / (time.time() - last_time))
# 	last_time = time.time()
# print(fps)
