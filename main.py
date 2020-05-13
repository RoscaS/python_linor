"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

import cv2
import numpy as np

from src.GUI import GUI
from src.tools.Helpers import Colors
from src.objects.Image import Image
from src.tools.Smoothing import Smoothing
from src.functions import (
	roi,
	draw_polygon,
	capture_window,
	compute_mask,
	compute_vanishing_point, compute_averages,
	update_smoothing
)


def main():
	"""
	Entry point. Main part of the program loop.
	"""
	mask = compute_mask()

	# Screen capture;
	screen_cap = capture_window()
	original = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2RGB)
	canvas = np.zeros_like(original)

	# Image processing
	grayed = Image(original).gray()
	blurred = grayed.gaussian_blur()
	processed = blurred.canny()
	masked = Image(roi(processed.pixels, [np.array([i.get() for i in mask])]))

	lines = masked.find_lines()
	color = Colors.green()

	# Computing
	if lines is not None:
		update_smoothing(compute_averages(lines), smoothing)
	else:
		color = Colors.blue()

	smoothed_lines = smoothing.get_left_line(), smoothing.get_right_line()
	vanishing_point = compute_vanishing_point(smoothed_lines)

	# Lines overlay
	if GUI.lines_overlay:
		smoothed_lines[0].draw(canvas, color=color, thickness=15)
		smoothed_lines[1].draw(canvas, color=color, thickness=15)
		vanishing_point.draw(canvas, color=color, thickness=5)

	# Target overlay
	if GUI.target_overlay:
		GUI.draw_target(vanishing_point, original, canvas)

	# Merge original image & overlay
	combo_image = cv2.addWeighted(original, 1, canvas, 0.4, 2)
	if GUI.polygon_overlay:
		draw_polygon(combo_image, mask)

	GUI.draw(combo_image)

	# Split image layout
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
	smoothing = Smoothing()

	while (True):

		buffer_increment = 5

		if GUI.buffer <= 1:
			GUI.buffer = 1
			buffer_increment = 4

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

		elif key == ord('b'):
			GUI.buffer -= buffer_increment
			smoothing.buffer = GUI.buffer
		elif key == ord('n'):
			GUI.buffer += buffer_increment
			smoothing.buffer = GUI.buffer



		elif key == ord('1'):
			GUI.lines_overlay = not GUI.lines_overlay

		elif key == ord('2'):
			GUI.polygon_overlay = not GUI.polygon_overlay

		elif key == ord('s'):
			GUI.vanishing_point_strategy = not GUI.vanishing_point_strategy

		elif key == ord('t'):
			GUI.target_overlay = not GUI.target_overlay


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



