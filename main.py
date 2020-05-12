import random

import cv2
import numpy as np

from src.GUI import GUI
from src.Helpers import Colors
from src.Image import Image
from src.Line import Line
from src.Point import Point
from src.Settings import settings
from src.Smoothing import Smoothing
from src.functions import roi, draw_polygon, capture_window, strategy

smoothing = Smoothing(settings["smoothing"])




def rand_color():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return r, g, b



def main():

	max_width = settings['resolution'][0]
	top_width = GUI.mask_top_width
	bottom_width = GUI.mask_bottom_width

	x = (max_width - top_width) / 2

	top_left = x
	top_right = max_width - x

	xx = (max_width - bottom_width) / 2

	bottom_left = xx
	bottom_right = max_width - xx

	MASK = [
		Point(top_left, GUI.mask_top_y),
		Point(bottom_left, GUI.mask_bottom_y),

		Point(bottom_right, GUI.mask_bottom_y),
		Point(top_right, GUI.mask_top_y),

	]

	# Image capture
	screen_cap = capture_window()
	original = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2RGB)
	canvas = np.zeros_like(original)

	# Image processing
	grayed = Image(original).gray()
	blurred = grayed.gaussian_blur()
	processed = blurred.canny()
	masked = Image(roi(processed.pixels, [np.array([i.get() for i in MASK])]))


	if GUI.lines_overlay:

		# Data transformation
		lines = masked.find_lines()

		if lines is not None:

			left_lines = [i for i in lines if i.slope < 0]
			right_lines = [i for i in lines if i.slope > 0]

			left_average = Line.average(left_lines)
			right_average = Line.average(right_lines)

			if left_average is not None:
				smoothing.add_left_line(left_average)
				# left_average.draw(canvas)

			if right_average is not None:
				smoothing.add_right_line(right_average)
				# right_average.draw(canvas)

			# left_line = smoothing.get_left_line()
			# right_line = smoothing.get_right_line()

		lines = smoothing.get_left_line(), smoothing.get_right_line()
		intersection = strategy(lines)

		lines[0].draw(canvas, thickness=15)
		lines[1].draw(canvas, thickness=15)
		intersection.draw(canvas, thickness=5)

		# if not None in [left_average, right_average]:
			# 	intersection = strategy((left_average, right_average), canvas)





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



		elif key == ord('u'):
			GUI.mask_top_y += 10
		elif key == ord('i'):
			GUI.mask_top_y -= 10

		elif key == ord('j'):
			GUI.mask_bottom_y += 10
		elif key == ord('k'):
			GUI.mask_bottom_y -= 10

		elif key == ord('y'):
			GUI.mask_top_width -= 20
		elif key == ord('o'):
			GUI.mask_top_width += 20

		elif key == ord('h'):
			GUI.mask_bottom_width -= 20
		elif key == ord('l'):
			GUI.mask_bottom_width += 20



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
