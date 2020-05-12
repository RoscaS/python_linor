import ffmpeg

class MetaData(object):
	def __init__(self, path_video, width = 0, height = 0, total_frames = 0):
		if path_video is not None:
			self.path_video = path_video
			self.width = self._width()
			self.height = self._height()
			self.total_frames = self._total_frames()
		else:
			self.path_video = path_video
			self.width = width
			self.height = height
			self.total_frames = total_frames

	@classmethod
	def from_screen(cls, width, height):
		return cls(None, width, height, -1)

	@classmethod
	def from_video(cls, path_video):
		return cls(path_video)

	def _width(self):
		return self.all_infos()['width']

	def _height(self):
		return self.all_infos()['height']

	def _total_frames(self):
		return self.all_infos()['nb_frames']

	def all_infos(self):
		probe = ffmpeg.probe(self.path_video)
		video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
		return video_stream
