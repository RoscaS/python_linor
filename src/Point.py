from typing import Iterable, List

import cv2
import numpy as np

from src.Helpers import Colors


class Point:
	def __init__(self, x=0, y=0, point: Iterable = None):
		point = point if point is not None else x, y
		self.x = int(point[0])
		self.y = int(point[1])

	def __str__(self):
		return f"({self.x}; {self.y})"

	def get(self):
		return (self.x, self.y)

	def draw(self,
			 img: np.ndarray,
			 ray: int = 2,
			 color: List[int] = Colors.red(),
			 thickness: int = 3):
		cv2.circle(img, self.get(), ray, color, thickness)
