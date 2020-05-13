"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

import time
import cv2

from src.tools.Helpers import Colors
from src.objects.Line import Line
from src.objects.Point import Point
from settings import settings


class GUI:
	_frames = 0
	_last_time = 0

	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = .5
	color = [255, 0, 0]
	thickness = 1

	DATA_COLUMN_START_TOP = 95
	top_offset = DATA_COLUMN_START_TOP
	top_margin = 20
	left_margin = 10
	line_height = 15


	lines_overlay = True
	target_overlay = True
	polygon_overlay = False

	process_overlay = False
	grayed_overlay = False
	blured_overlay = False
	processed_overlay = False
	masked_overlay = False

	fps_counter = True

	buffer = settings["buffer"]

	mask_top_y = settings["mask_top_y"]
	mask_bottom_y = settings["mask_bottom_y"]

	mask_top_width = settings["mask_top_width"]
	mask_bottom_width = settings["mask_bottom_width"]

	@classmethod
	def draw(cls, image):
		GUI.show_fps(image)
		GUI.buffer_size(image)
		GUI.write_status(image)
		GUI.mask_text(image)

	@classmethod
	def show_fps(cls, image):
		if not cls.fps_counter:
			return
		fps = round(1 / (time.time() - cls._last_time), 2)
		cls.write(image, f"frame: {cls._frames}", (10, cls.top_margin))
		cls.write(image, f"fps: {fps}", (10, cls.top_margin + cls.line_height))
		cls._last_time = time.time()
		cls._frames += 1

	@classmethod
	def buffer_size(cls, image):
		cls.write(image, f"Buffer size: b <- {cls.buffer} -> n", (10, 70))

	@classmethod
	def write_status(cls, image):
		cls.top_offset = cls.DATA_COLUMN_START_TOP
		cls.left_margin = 10
		cls.append_col(image, f"1 Lines overlay", cls.lines_overlay)
		cls.append_col(image, f"2 Polygon overlay", cls.polygon_overlay)
		cls.append_col(image, f"3 Process overlay", cls.process_overlay)
		cls.left_margin = 40
		cls.append_col(image, f"4 Grayed overlay", cls.grayed_overlay)
		cls.append_col(image, f"5 Blured overlay", cls.blured_overlay)
		cls.append_col(image, f"6 Processed overlay", cls.processed_overlay)
		cls.append_col(image, f"7 Masked overlay", cls.masked_overlay)

	@classmethod
	def mask_text(cls, image):
		if not cls.polygon_overlay:
			return
		center = 512
		top_center = Point(center-50, cls.mask_top_y - 10)
		bottom_center =Point(center-50, cls.mask_bottom_y + 20)
		top_left = Point(5, cls.mask_top_y)
		bottom_left = Point(5, cls.mask_bottom_y)

		cls.write(image, f"y = {cls.mask_top_y}px", top_left.get(), Colors.white(), .3, 1)
		top_left.y += cls.line_height
		cls.write(image, f"down: u up: i", top_left.get(), Colors.white(), .3, 1)

		cls.write(image, f"y = {cls.mask_bottom_y}px", bottom_left.get(), Colors.white(), .3, 1)
		bottom_left.y += cls.line_height
		cls.write(image, f"down: j up: k", bottom_left.get(), Colors.white(), .3, 1)

		cls.write(image, f"y <- {cls.mask_top_width}px -> o", top_center.get(), Colors.white(), .3, 1)
		cls.write(image, f"h <- {cls.mask_bottom_width}px -> l", bottom_center.get(), Colors.white(), .3, 1)

	@classmethod
	def draw_target(cls, vanishing_point, hard_image, blended_image):
		if not cls.target_overlay:
			return
		max_width = settings["resolution"][0]
		height = settings["target_height"]
		center = Point(max_width / 2, height)

		center.draw(blended_image, 9, Colors.white(), 2)

		left = Point(200, height)
		right = Point(center.x - 11, height)
		Line(left, right).draw(blended_image, color=Colors.white(),
							   thickness=1)

		left = Point(center.x + 11, height)
		right = Point(max_width - 200, height)
		Line(left, right).draw(blended_image, color=Colors.white(),
							   thickness=1)

		indicator = vanishing_point
		indicator.y = height
		indicator.draw(hard_image, 1, Colors.blue(), 5)

		value = center.x - vanishing_point.x
		position = center
		position.x -= 14
		position.y -= 15
		cls.write(hard_image, f"{-value}", position.get(), Colors.white(), .5, 1)

	@classmethod
	def append_col(cls, image, text, value):
		cls.top_offset += cls.line_height
		position = (cls.left_margin, cls.top_offset)
		color = Colors.green() if value else Colors.blue()
		cls.write(image, text, position, color)

	@classmethod
	def write(cls, image, text, position, color=None, scale=None,
			  thickness=None):
		color = cls.color if color == None else color
		scale = cls.font_scale if scale == None else scale
		thickness = cls.thickness if thickness == None else thickness
		cv2.putText(image, text, position, cls.font, scale, color, thickness)

	@classmethod
	def clear_overlays(cls):
		cls.grayed_overlay = False
		cls.blured_overlay = False
		cls.processed_overlay = False
		cls.masked_overlay = False
