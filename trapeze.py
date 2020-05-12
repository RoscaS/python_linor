class Trapeze:
	def __init__(self, width, height):
		self.hl1 = [0, height]
		self.hl2 = [0, height / 5 * 4]
		self.hl3 = [width / 3, height / 2]
		self.hr1 = [width, height]
		self.hr2 = [width, height / 5 * 4]
		self.hr3 = [width / 3 * 2,height / 2]
