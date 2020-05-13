"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

from typing import List, Tuple

import cv2
import numpy as np

from src.objects.Line import Line
from src.objects.Point import Point


class Image:
	"""
	Representation of an image.
	Contain usefull processing methodes used around the program
	and some abstractions to make it easy to use with cv2.
	"""

	RHO = 1
	THETA = np.pi / 180
	THRESHOLD = 80
	MIN_LINE_LENGTH = 1
	MAX_LINE_LENGTH = 150

	def __init__(self, pixels):
		self._gray = None
		self._gaussian = None
		self._canny = None
		self._edges = None
		self._lines = None

		self.pixels = pixels

	@property
	def np(self) -> np.ndarray:
		return cv2.cvtColor(self.pixels, cv2.COLOR_BGR2RGB)

	def gray(self) -> object:
		if self._gray is None:
			self._gray = Image(cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY))
		return self._gray

	def gaussian_blur(self, kernel: Tuple[int] = (5, 5)) -> object:
		if self._gaussian is None:
			self._gaussian = Image(cv2.GaussianBlur(self.pixels, kernel, 0))
		return self._gaussian

	def canny(self, low_bound: int = 80, high_bound: int = 110) -> object:
		if self._canny is None:
			self._canny = Image(cv2.Canny(self.pixels, threshold1=low_bound, threshold2=high_bound))
		return self._canny

	def edges(self) -> object:
		if self._edges is None:
			gray = self.gray()
			blurred = gray.gaussian_blur()
			canny = blurred.canny()
			self._edges = canny
		return self._edges

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
