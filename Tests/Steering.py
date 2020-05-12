from Tests.directkeys import PressKey, ReleaseKey, W, A, S, D, LEFT, RIGHT


# this funtions sends the input to the game which is running on left side of
# screen
def straight():
	ReleaseKey(A)
	ReleaseKey(D)


def little_left():
	PressKey(A)
	# indicate when turning so traffic in next lane stops
	PressKey(LEFT)
	ReleaseKey(LEFT)
	ReleaseKey(W)
	ReleaseKey(D)


def little_right():
	PressKey(D)
	# indicate when turning so traffic in next lane stops
	PressKey(RIGHT)
	ReleaseKey(RIGHT)
	ReleaseKey(W)
	ReleaseKey(A)


def steer(center_pt, center_fixed, f_r, f_l):
	'''The logic behind this code is simple,
  	the center_fixed should be in the center_line.
  	means the cars is in center of the lane, if its get away from
  	center,
  	then the left and right functions are used accordingly,then if
  	the center fixed is too far from the center_pt the car takes
  	complete left or right accordingly!'''
	if center_pt == center_fixed:
		straight()
		print('forward')
	elif center_pt > center_fixed and center_fixed > f_r:
		# for cockpit view
		# little_right()
		# print('right')
		# for bumper view
		straight()
		print('forward')
	elif center_pt < center_fixed and center_fixed < f_l:
		# for cockpit view
		# little_left()
		# print('left')

		# for bumper view
		straight()
		print('forward')
	elif center_fixed < f_r:
		little_right()
		print('right')
	elif center_fixed > f_l:
		little_left()
		print('left')
	else:
		straight()
		print('forward')
