import cv2

from src.Helpers import Colors


class GUI:
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = .8
	color = [255, 0, 0]
	thickness = 1

	DATA_COLUMN_START_TOP = 60
	top_offset = DATA_COLUMN_START_TOP
	left_margin = 10
	line_height = 25


	lines_overlay = True
	polygon_overlay = False

	process_overlay = False
	grayed_overlay = False
	blured_overlay = False
	processed_overlay = False
	masked_overlay = False

	fps_text = True

	@classmethod
	def clear_overlays(cls):
		cls.grayed_overlay = False
		cls.blured_overlay = False
		cls.processed_overlay = False
		cls.masked_overlay = False

	@classmethod
	def write_status(cls, image):
		cls.append_col(image, f"(1) Lines overlay", cls.lines_overlay)
		cls.append_col(image, f"(2) Polygon overlay", cls.polygon_overlay)
		cls.append_col(image, f"(3) Process overlay", cls.process_overlay)
		cls.left_margin = 40
		cls.append_col(image, f"(4) Grayed overlay", cls.grayed_overlay)
		cls.append_col(image, f"(5) Blured overlay", cls.blured_overlay)
		cls.append_col(image, f"(6) Processed overlay", cls.processed_overlay)
		cls.append_col(image, f"(7) Masked overlay", cls.masked_overlay)
		cls.top_offset = cls.DATA_COLUMN_START_TOP
		cls.left_margin = 10

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
