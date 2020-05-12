import cv2
import numpy as np

from Tests.grab import grab_screen
from src.Image import Image
from src.Point import Point
from src.functions import roi, draw_polygon

MASK = [
	Point(10, 650),   # top right
	Point(1000, 650),  # bottom right
	Point(900, 480),  # bottom left
	Point(100, 480),  # top left
]

lines_overlay = True
polygon_overlay = False

process_overlay = False

grayed_overlay = False
blured_overlay = False
processed_overlay = False
masked_overlay = False


def clear_overlays():
	global grayed_overlay, blured_overlay, masked_overlay, processed_overlay
	grayed_overlay = False
	blured_overlay = False
	processed_overlay = False
	masked_overlay = False


def main():
	# Image capture
	screen_cap = grab_screen(region=(7, 33, 1019, 792))
	original = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2RGB)

	# Image processing
	grayed = Image(original).gray()
	blurred = grayed.gaussian_blur()
	processed = blurred.canny()
	masked = Image(roi(processed.pixels, [np.array([i.get() for i in MASK])]))

	# Data transformation
	lines = masked.find_lines()


	# Handle result window
	canvas = np.zeros_like(original)
	if lines_overlay:
		if lines is not None:
			for line in lines:
				line.draw(canvas)

	combo_image = cv2.addWeighted(original, 1, canvas, 0.4, 2)
	if polygon_overlay:
		draw_polygon(combo_image, MASK)


	# Handel split image layout
	if process_overlay:
		left = combo_image

		if grayed_overlay:
			right = grayed.np
		elif blured_overlay:
			right = blurred.np
		elif processed_overlay:
			right = processed.np
		elif masked_overlay:
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
			lines_overlay = not lines_overlay

		elif key == ord('2'):
			polygon_overlay = not polygon_overlay

		elif key == ord('3'):
			clear_overlays()
			process_overlay = not process_overlay

		elif key == ord('4') and process_overlay:
			clear_overlays()
			grayed_overlay = not grayed_overlay

		elif key == ord('5') and process_overlay:
			clear_overlays()
			blured_overlay = not blured_overlay

		elif key == ord('6') and process_overlay:
			clear_overlays()
			processed_overlay = not processed_overlay

		elif key == ord('7') and process_overlay:
			clear_overlays()
			masked_overlay = not masked_overlay





# last_time = 0
# while (True):
# 	main()
#
# 	fps = "fps: {}".format(1 / (time.time() - last_time))
# 	last_time = time.time()
	# print(fps)
