import time

import cv2

from src.Helpers import Colors


class GUI:
	_frames = 0
	_last_time = 0

	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = .8
	color = [255, 0, 0]
	thickness = 1

	DATA_COLUMN_START_TOP = 95
	top_offset = DATA_COLUMN_START_TOP
	top_margin = 20
	left_margin = 10
	line_height = 25

	vanishing_point_strategy = True

	lines_overlay = True
	polygon_overlay = False

	process_overlay = False
	grayed_overlay = False
	blured_overlay = False
	processed_overlay = False
	masked_overlay = False

	fps_counter = True


	@classmethod
	def draw(cls, image):
		GUI.show_fps(image)
		GUI.write_strategy(image)
		GUI.write_status(image)

	@classmethod
	def show_fps(cls, image):
		if not GUI.fps_counter: return
		fps = round(1 / (time.time() - cls._last_time), 2)
		GUI.write(image, f"frame: {cls._frames}", (10, cls.top_margin))
		GUI.write(image, f"fps: {fps}", (10, cls.top_margin + cls.line_height))
		GUI._last_time = time.time()
		GUI._frames += 1

	@classmethod
	def write_strategy(cls, image):
		position = (10,  cls.top_margin + 2 * cls.line_height + 10)
		strategy = "Vanising point" \
			if cls.vanishing_point_strategy \
			else "Lane center"

		GUI.write(image, f"(s) Strategy: {strategy}", position, Colors.green())

	@classmethod
	def write_status(cls, image):
		cls.top_offset = cls.DATA_COLUMN_START_TOP
		cls.left_margin = 10
		cls.append_col(image, f"(1) Lines overlay", cls.lines_overlay)
		cls.append_col(image, f"(2) Polygon overlay", cls.polygon_overlay)
		cls.append_col(image, f"(3) Process overlay", cls.process_overlay)
		cls.left_margin = 40
		cls.append_col(image, f"(4) Grayed overlay", cls.grayed_overlay)
		cls.append_col(image, f"(5) Blured overlay", cls.blured_overlay)
		cls.append_col(image, f"(6) Processed overlay", cls.processed_overlay)
		cls.append_col(image, f"(7) Masked overlay", cls.masked_overlay)

	@classmethod
	def append_col(cls, image, text, value):
		cls.top_offset += cls.line_height
		position = (cls.left_margin, cls.top_offset)
		color = Colors.green() if value else Colors.blue()
		cls.write(image, text, position, color)

	@classmethod
	def write(cls, image, text, position, color=None):
		color = cls.color if color == None else color
		cv2.putText(image, text, position, cls.font, cls.font_scale, color, cls.thickness)

	@classmethod
	def clear_overlays(cls):
		cls.grayed_overlay = False
		cls.blured_overlay = False
		cls.processed_overlay = False
		cls.masked_overlay = False
