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

from src.Point import Point
from src.Helpers import Colors


class Line:
	"""
	Representation of a line segment.
	Contain usefull math methodes used in the program and
	some abstractions to make it easy to use with cv2.

	A Line is defined by two Point objects. For some applications,
	the `get` method returns a list of all the points that defines
	the Line.
	"""

	def __init__(self,
				 A: Point = None,
				 B: Point = None,
				 coords: List[float] = None):
		self._slope = None
		self._y_intercept = None
		self._magnitude = None

		if coords is not None:
			if (type(coords) not in [list, tuple] or not len(coords)):
				self.A = None
				self.B = None
			else:
				coords = [int(i) for i in coords]
				self.A = Point(coords[0], coords[1])
				self.B = Point(coords[2], coords[3])
		else:
			self.A = A
			self.B = B

	def __str__(self) -> str:
		return f"d: A{self.A} \t B{self.B}" \
			   f"\tm = {round(self.slope, 2)} " \
			   f"\tb = {round(self.y_intercept, 2)}"

	def get(self) -> List[int]:
		"""
		Get a list containing all coords that define `self`
		:return: [A.x, A.y, B.x, B.y]
		"""
		return [*self.A.get(), *self.B.get()]

	@property
	def magnitude(self) -> float:
		"""
		Length of the `self`
		d^2 = a^2 + b^2
		Implements lazy loading
		:return: length of the segment
		"""
		if (self._slope is None):
			a = (self.B.x - self.A.x)
			b = (self.B.y - self.A.y)
			self._magnitude = np.math.sqrt(a ** 2 + b ** 2)
		return self._magnitude

	@property
	def slope(self) -> float:
		"""
		Slope of `self`
		y = mx + b
		=> m = dx/dy
		Implements lazy loading
		:return: m, the slope of `self`
		"""
		if (self._slope is None):
			y = self.B.y - self.A.y
			x = self.B.x - self.A.x
			self._slope = y / x if x != 0 else 0

		# x = self.B.x - self.A.x
		# y = self.B.y - self.A.y
		# self._slope =  x / y if y != 0 else 0
		return self._slope

	@property
	def y_intercept(self) -> float:
		"""
		Height where `self` intersects the y axis.
		y = mx + b
		=> b = y - mx
		Implements lazy loading
		:return: b, where `self` intersects the y axis
		"""
		if (self._y_intercept is None):
			self._y_intercept = self.A.y - self.slope * self.A.x
		return self._y_intercept

	def intersects(self, other: object) -> Point or None:
		"""
		Intersection point between `self` and `other`.
		y = mx +b
		=> m = dx/dy
		=> b = y - mx

		m1 * x + b1 = m2 * x + b2
		=> x = (b2 - b1) / (m1 - m2)
		=> y = m1 * x + b1 = m2 * x + b2
		:param other: another Line
		:return: Point of intersection
		"""
		m1 = self.slope
		m2 = other.slope

		if m1 == m2:
			return None

		b1 = self.y_intercept
		b2 = other.y_intercept

		x = (b2 - b1) / (m1 - m2)
		y = m1 * x + b1

		return Point(x, y)

	def draw(self,
			 image: np.ndarray,
			 color: List[int] = Colors.green(),
			 thickness: int = 3) -> None:
		"""
		Draw self on `img`
		:param image: image to draw on
		:param color:
		:param thickness:
		"""
		cv2.line(image, self.A.get(), self.B.get(), color, thickness)

	@classmethod
	def average(cls, lines: List[object]) -> object or None:
		"""
		Line that is the average of the lines inside `lines`
		:param lines: Lines to average
		:return: resulting `Line`
		"""
		if list is None or len(lines) <= 0:
			return None
		average = np.average([i.get() for i in lines], axis=0).tolist()
		return Line(coords=average)
