
from src.Line import Line


class Smoothing:

	def __init__(self, frames: int):
		self.frames = frames
		self.left_lines = [Line(coords=[0,0,0,0])]
		self.right_lines = [Line(coords=[0,0,0,0])]

	def add_left_line(self, line: Line):
		if len(self.left_lines) >= self.frames:
			self.left_lines.pop(0)
		self.left_lines.append(line)

	def add_right_line(self, line: Line):
		if len(self.right_lines) >= self.frames:
			self.right_lines.pop(0)
		self.right_lines.append(line)

	def get_left_line(self) -> Line:
		return Line.average(self.left_lines)

	def get_right_line(self) -> Line:
		return Line.average(self.right_lines)


