"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

import random


class Colors:
	@classmethod
	def white(cls): return [255, 255, 255]

	@classmethod
	def blue(cls): return [0, 0, 255]

	@classmethod
	def green(cls): return [0, 255, 0]

	@classmethod
	def red(cls): return [255, 0, 0]

	@classmethod
	def purple(cls): return [255, 0, 100]

	@classmethod
	def cian(cls): return [255, 200, 0]

	@classmethod
	def pink(cls): return [156, 127, 254]

	@classmethod
	def rand_color(cls):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		return r, g, b
