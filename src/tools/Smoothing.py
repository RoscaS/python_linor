"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

from src.objects.Line import Line
from settings import settings


class Smoothing:
	"""
	Buffer that makes things silky smooth.
	"""

	def __init__(self):
		self.buffer = settings["buffer"]
		self.left_lines = [Line(coords=[0, 0, 0, 0])]
		self.right_lines = [Line(coords=[0, 0, 0, 0])]

	def add_left_line(self, line: Line):
		if len(self.left_lines) >= self.buffer:
			self.left_lines.pop(0)
		self.left_lines.append(line)

	def add_right_line(self, line: Line):
		if len(self.right_lines) >= self.buffer:
			self.right_lines.pop(0)
		self.right_lines.append(line)

	def get_left_line(self) -> Line:
		return Line.average(self.left_lines)

	def get_right_line(self) -> Line:
		return Line.average(self.right_lines)
