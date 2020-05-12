# def main_old():
# 	screen = grab_screen(region=(7, 33, 1019, 792))
# 	new_image = proceesed_img(screen)
# 	lines = find_lines(new_image)
#
# 	left_lines_coords = []
# 	right_lines_coords = []
#
#
#
# 	image_ = Image(screen).process()
# 	lines_ = image_.find_lines()
#
# 	left_lines, right_lines = [], []
#
#
# 	if lines is not None:
# 		for line in lines:
# 			x1, y1, x2, y2 = line[0]
# 			m = (x2 - x1) / (y2 - y1)
#
# 			if m < 0:
# 				left_lines_coords.append([x1, y1, x2, y2])
# 			# and if n < m > p: pas interessant
# 			elif m > 0:
# 				# and if n < m > p: pas interessant
# 				right_lines_coords.append([x1, y1, x2, y2])
#
# 		l_avg = np.average(left_lines_coords, axis=0)
# 		r_avg = np.average(right_lines_coords, axis=0)
#
# 		l = l_avg.tolist()
# 		r = r_avg.tolist()
#
# 		# print("\noriginal")
# 		# print(l)
# 		# print(r)
#
#
# 		# main()
#
# 		# print(l)
# 		# print(r)
#
# 		try:
# 			# with the finded slope and intercept, this is used to find
# 			# the value of point x on both left and right line
# 			# the center point is denoted by finding center distance between
# 			# two lines
# 			y = 360
# 			c1, d1, c2, d2 = r
# 			a1, b1, a2, b2 = l
# 			l_slope = (b2 - b1) / (a2 - a1)
# 			r_slope = (d2 - d1) / (c2 - c1)
# 			l_intercept = b1 - (l_slope * a1)
# 			r_intercept = d1 - (r_slope * c1)
# 			l_x = (y - l_intercept) / l_slope
# 			r_x = (y - r_intercept) / r_slope
# 			distance = math.sqrt((r_x - l_x) ** 2 + (y - y) ** 2)
#
# 			# line_center repressent the center point on the line
# 			line_center = distance / 2
# 			center_pt = [l_x + line_center]
#
# 			# f_l = [(l_x + (line_center * 2.02))]
# 			# f_r = [(l_x + (line_center * 0.08))]
#
# 			# create a center point which is fixed
# 			center_fixed = [664]
#
# 			x_1 = int(l_x)
# 			x_2 = int(r_x)
#
# 		# steer(center_pt, center_fixed, f_r, f_l)
#
#
# 		except:
# 			pass
# 		# straight()
# 		# print('forward')
#
# 	# line_image = display_line(screen)
# 	# combo_image = cv2.addWeighted(screen, 0.8, line_image, 1.2, 2)
# 	# cv2.imshow('Window', cv2.cvtColor(combo_image, cv2.COLOR_BGR2RGB))
# 	# cv2.imshow('Window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))


while (True):
	main()
	# main_old()

	if cv2.waitKey(25) & 0xff == ord('q'):
		cv2.destroyAllWindows()
		break



# while (True):
# 	screen = grab_screen(region=(7, 33, 1019, 792))
# 	new_image = proceesed_img(screen)
# 	lines = find_lines(new_image)
#
# 	left_lines_coords = []
# 	right_lines_coords = []
#
#
#
# 	image_ = Image(screen).process()
# 	lines_ = image_.find_lines()
#
# 	left_lines, right_lines = [], []
#
#
# 	if lines is not None:
# 		for line in lines:
# 			x1, y1, x2, y2 = line[0]
# 			m = (x2 - x1) / (y2 - y1)
#
# 			if m < 0:
# 				left_lines_coords.append([x1, y1, x2, y2])
# 			# and if n < m > p: pas interessant
# 			elif m > 0:
# 				# and if n < m > p: pas interessant
# 				right_lines_coords.append([x1, y1, x2, y2])
#
# 		l_avg = np.average(left_lines_coords, axis=0)
# 		r_avg = np.average(right_lines_coords, axis=0)
#
# 		l = l_avg.tolist()
# 		r = r_avg.tolist()
#
# 		# print("\noriginal")
# 		# print(l)
# 		# print(r)
#
#
# 		# main()
#
# 		# print(l)
# 		# print(r)
#
# 		try:
# 			# with the finded slope and intercept, this is used to find
# 			# the value of point x on both left and right line
# 			# the center point is denoted by finding center distance between
# 			# two lines
# 			y = 360
# 			c1, d1, c2, d2 = r
# 			a1, b1, a2, b2 = l
# 			l_slope = (b2 - b1) / (a2 - a1)
# 			r_slope = (d2 - d1) / (c2 - c1)
# 			l_intercept = b1 - (l_slope * a1)
# 			r_intercept = d1 - (r_slope * c1)
# 			l_x = (y - l_intercept) / l_slope
# 			r_x = (y - r_intercept) / r_slope
# 			distance = math.sqrt((r_x - l_x) ** 2 + (y - y) ** 2)
#
# 			# line_center repressent the center point on the line
# 			line_center = distance / 2
# 			center_pt = [l_x + line_center]
#
# 			# f_l = [(l_x + (line_center * 2.02))]
# 			# f_r = [(l_x + (line_center * 0.08))]
#
# 			# create a center point which is fixed
# 			center_fixed = [664]
#
# 			x_1 = int(l_x)
# 			x_2 = int(r_x)
#
# 		# steer(center_pt, center_fixed, f_r, f_l)
#
#
# 		except:
# 			pass
# 		# straight()
# 		# print('forward')
#
# 	# line_image = display_line(screen)
# 	# combo_image = cv2.addWeighted(screen, 0.8, line_image, 1.2, 2)
# 	# cv2.imshow('Window', cv2.cvtColor(combo_image, cv2.COLOR_BGR2RGB))
# 	# cv2.imshow('Window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
#
# 	if cv2.waitKey(25) & 0xff == ord('q'):
# 		cv2.destroyAllWindows()
# 		break
#
