from typing import List

import cv2
import numpy as np

from src.Point import Point
from src.Helpers import Colors


class Line:
	def __init__(self, A: Point = None, B: Point = None, coords: List[float] = None):
		self._slope = None
		if coords is not None:
			if (type(coords) is not list or not len(coords)):
				self.A = None
				self.B = None
			else:
				self.A = Point(coords[0], coords[1])
				self.B = Point(coords[2], coords[3])
		else:
			self.A = A
			self.B = B

	def __str__(self):
		return f"d: A = {self.A}; B = {self.B}"

	def get(self):
		return [*self.A.get(), *self.B.get()]

	@property
	def magnitude(self):
		return np.math.sqrt(
			(self.B.x - self.A.x) ** 2 + (self.B.y - self.A.y) ** 2)

	@property
	def slope(self):
		if (self._slope is None):
			x = self.B.x - self.A.x
			y = self.B.y - self.A.y
			self._slope =  x / y if y != 0 else 0
		return self._slope

	@property
	def y_intercept(self):
		return self.A.y - self.slope * self.A.x

	def draw(self,
			 img: np.ndarray,
			 color: List[int] = Colors.green(),
			 thickness: int = 3):
		cv2.line(img, self.A.get(), self.B.get(), color, thickness)


