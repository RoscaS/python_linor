from abc import ABC, abstractmethod

class Strategy(ABC):
	@abstractmethod
	def do_algorithme(self, data: list):
		pass

class means_lines(Strategy):
	def do_algorithme(self, lane_data: list):
		pass


class means_points(Strategy):
	def do_algorithme(self, lane_data: list):
		pass
