from typing import List

import cv2
import numpy as np

from src import Point
from src.Helpers import Colors


class Line:
	def __init__(self, A: Point, B: Point):
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
		x = self.B.x - self.A.x
		y = self.B.y - self.A.y
		return x / y if y != 0 else 0

	def draw(self,
			 img: np.ndarray,
			 color: List[int] = Colors.green(),
			 thickness: int = 3):
		cv2.line(img, self.A.get(), self.B.get(), color, thickness)


