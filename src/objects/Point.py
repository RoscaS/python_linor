"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""


from typing import Iterable, List, Tuple

import cv2
import numpy as np

from src.tools.Helpers import Colors


class Point:
	"""
	Representation of a point.
	Contain some abstractions to make it easy to use with cv2.

	A Point is defined by two int components. For some applications,
	the `get` method returns a tuple containing both components.
	"""

	def __init__(self, x=0, y=0, point: Iterable = None):
		point = point if point is not None else x, y
		self.x = int(point[0])
		self.y = int(point[1])

	def __str__(self) -> str:
		return f"({self.x}; {self.y})"

	def get(self) -> Tuple[int, int]:
		"""
		Get a tuple containing self's components
		:return: (x, y)
		"""
		return (self.x, self.y)

	def draw(self,
			 image: np.ndarray,
			 ray: int = 2,
			 color: List[int] = Colors.green(),
			 thickness: int = 3) -> None:
		"""
		Draw self on `img`
		:param image: image to draw on
		:param ray: of the circle that represent this point
		:param color:
		:param thickness:
		"""
		cv2.circle(image, self.get(), ray, color, thickness)

	@classmethod
	def average(cls, points: List[object]) -> object or None:
		"""
		Point that is the average of the points inside `points`
		:param points: points to average
		:return: resulting `Point`
		"""
		if list is None or len(points) <= 0:
			return None
		average = np.median([i.get() for i in points], axis=0).tolist()
		return Point(point=average)
