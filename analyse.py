import os
import time

import numpy
from mss import mss

import numpy as np
import cv2
from PIL import Image

from arrow import Arrow
from pretreatment import zone_mask, color_mask, morpho_process, apply_canny, \
	apply_gaussian
from metadata import MetaData
from draw import draw_infos, draw_arrow
from trapeze import Trapeze

from Tests.Line import Point
from numpy import ones, vstack
from numpy.linalg import lstsq


def find_lines(image, rho=1, theta=np.pi / 180, threshold=150,
			   min_line_length=20, max_line_gap=15):
	# get lines with Hough algo
	return cv2.HoughLinesP(image, rho, theta, threshold, np.array([]),
						   min_line_length, max_line_gap)


def intersect_droit(l1, l2):
	m1 = (l1[3] - l1[1]) / (l1[2] - l1[0])
	b1 = l1[3] - m1 * l1[2]

	m2 = (l2[3] - l2[1]) / (l2[2] - l2[0])
	b2 = l2[3] - m2 * l2[2]

	x = (b1 - b2) / (m2 - m1)
	y = m1 * x + b1

	return Point(x, y)


def separate_lines(lines):
	ys = []
	for i in lines:
		for ii in i:
			ys += [ii[1], ii[3]]
	min_y = min(ys)
	max_y = 600
	new_lines = []
	line_dict = {}

	for c, i in enumerate(lines):
		for xyxy in i:
			# These four lines:
			# modified from http://stackoverflow.com/questions/21565994/method
			# -to-return-the-equation-of-a-straight-line-given-two-points
			# Used to calculate the definition of a line, given two sets of
			# coords.
			x_coords = (xyxy[0], xyxy[2])
			y_coords = (xyxy[1], xyxy[3])
			A = vstack([x_coords, ones(len(x_coords))]).T
			m, b = lstsq(A, y_coords)[0]

			# Calculating our new, and improved, xs
			x1 = (min_y - b) / m
			x2 = (max_y - b) / m

			line_dict[c] = [m, b, [int(x1), min_y, int(x2), max_y]]
			new_lines.append([int(x1), min_y, int(x2), max_y])

	final_lanes = {}

	for key in line_dict:
		final_lanes_copy = final_lanes.copy()
		m = line_dict[key][0]
		b = line_dict[key][1]
		line = line_dict[key][2]

		if len(final_lanes) == 0:
			final_lanes[m] = [[m, b, line]]

		else:
			found_copy = False

			for other_ms in final_lanes_copy:

				if not found_copy:
					if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
						if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(
								b) > abs(
								final_lanes_copy[other_ms][0][1] * 0.8):
							final_lanes[other_ms].append([m, b, line])
							found_copy = True
							break
					else:
						final_lanes[m] = [[m, b, line]]

	line_counter = {}

	for lanes in final_lanes:
		line_counter[lanes] = len(final_lanes[lanes])

	top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[
				::-1][:2]

	lane1_id = top_lanes[0][0]
	lane2_id = top_lanes[1][0]

	pt = average_point([final_lanes[lane1_id], final_lanes[lane2_id]])
	# print(f"x : {pt.x}; y : {pt.y}")
	return pt


# return average_lane(final_lanes[lane1_id]), average_lane(final_lanes[
# lane2_id])

def average_point(all_lanes):
	ptsx = []
	ptsy = []
	for rlane in all_lanes[0]:
		for llane in all_lanes[1]:
			rh = rlane[2][1] - rlane[2][3]
			lh = llane[2][1] - llane[2][3]
			if abs(rh) > 50 and abs(lh) > 50:
				pt = intersect_droit(rlane[2], llane[2])
				ptsx.append(pt.x)
				ptsy.append(pt.y)

	return Point(np.mean(ptsx), np.mean(ptsy))


def average_lane(lane_data):
	x1s = []
	y1s = []
	x2s = []
	y2s = []
	for data in lane_data:
		h = data[2][1] - data[2][3]
		if abs(h) > 50:
			x1s.append(data[2][0])
			y1s.append(data[2][1])
			x2s.append(data[2][2])
			y2s.append(data[2][3])

	return [int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)),
			int(np.mean(y2s))]


def process_img(image, meta):
	processed_img = image

	processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2HSV)
	processed_img = cv2.cvtColor(processed_img, cv2.COLOR_HSV2RGB)
	processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)

	# filtre gaussian
	processed_img = apply_gaussian(processed_img, sigmax=3)
	# cv2.imshow('gaussian', processed_img)

	# Canny
	processed_img = apply_canny(processed_img, 80, 110)
	# cv2.imshow('canny', processed_img)

	# Erode, dilate
	processed_img = morpho_process(processed_img)
	cv2.imshow('morph', processed_img)

	# mask zone trapeze
	trapeze = Trapeze(meta.width, meta.height)
	vertices = [np.array([trapeze.hl2, trapeze.hl3, trapeze.hr3, trapeze.hr2], np.int32)]

	processed_img = zone_mask(processed_img, vertices)
	cv2.imshow('final', processed_img)
	return processed_img


def screen_record():
	x, y, w, h = 0, 50, 1024, 768
	meta = MetaData.from_screen(w - x, h - y)
	arrow = Arrow(meta.width)
	last_time = 0
	with mss() as sct:
		# Part of the screen to capture
		monitor = {"top": y, "left": x, "width": w, "height": h}
		while True:
			frame = numpy.array(sct.grab(monitor))
			try:
				processed_img = process_img(frame, meta)
				lines = find_lines(processed_img)
				p = separate_lines(lines)
				cv2.circle(frame, (int(p.x), int(p.y)), 2, [0, 255, 255], 10)
				arrow.add_point(int(p.x))
			except:
				pass

			draw_arrow(frame, arrow, meta.width)
			cv2.imshow("OpenCV/Numpy normal", frame)

			fps = "fps: {}".format(1 / (time.time() - last_time))
			last_time = time.time()
			print(fps)

			# Press "q" to quit
			if cv2.waitKey(50) & 0xFF == ord("q"):
				cv2.destroyAllWindows()
				break


def video_record(video):
	meta = MetaData.from_video(video)
	cap = cv2.VideoCapture(video)
	arrow = Arrow(meta.width)
	cpt_frame = 0
	while cap.isOpened():
		ret, frame = cap.read()
		cpt_frame += 1
		if ret:
			try:
				processed_img = process_img(frame, meta)
				lines = find_lines(processed_img)
				l1, l2 = separate_lines(lines)
				p = intersect_droit(l1, l2)
				arrow.add_point(int(p.x))

				processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

				cv2.imshow('window', processed_img)
				draw_infos(frame, p, l1, l2)
				draw_arrow(frame, arrow, meta.width)
				cv2.imshow('window', frame)

			except:
				pass
		# draw_arrow(frame, arrow, meta.width)

		# cv2.imshow('window', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	screen_record()
	# video_record("./resources/road.mp4")
	exit(0)
