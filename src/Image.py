from typing import List, Tuple

import cv2
import numpy as np

from src.Line import Line
from src.Point import Point
from src.Settings import settings


class Image:
	RHO = 1
	THETA = np.pi / 180
	THRESHOLD = 80
	MIN_LINE_LENGTH = 1
	MAX_LINE_LENGTH = 150

	def __init__(self, pixels):
		self.pixels = pixels

	@property
	def np(self) -> np.ndarray:
		return cv2.cvtColor(self.pixels, cv2.COLOR_BGR2RGB)

	def gray(self) -> object:
		return Image(cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY))

	def gaussian_blur(self, kernel: Tuple[int] = (5, 5), sigma: int = 3) -> object:
		return Image(cv2.GaussianBlur(self.pixels, kernel, sigma))

	def canny(self, low_bound: int = 80, high_bound: int = 110) -> object:
		return Image(cv2.Canny(self.pixels, threshold1=low_bound, threshold2=high_bound))

	def edges(self) -> object:
		gray = self.gray()
		blurred = gray.gaussian_blur()
		canny = blurred.canny()
		return canny

	def find_lines(self) -> List[Line] or None:
		raw = cv2.HoughLinesP(self.pixels,
							  Image.RHO,
							  Image.THETA,
							  Image.THRESHOLD,
							  np.ndarray([]),
							  Image.MIN_LINE_LENGTH,
							  Image.MAX_LINE_LENGTH)

		if (raw is not None):
			lines = []
			for el in raw:
				x1, y1, x2, y2 = el[0]
				lines.append(Line(Point(x1, y1), Point(x2, y2)))
			return lines
		return None



