"""
Traitement d'image: Projet final
Linor Project

INF3b
Latino Nathan
Rosca Sol
"""

from src.steering.directkeys import PressKey, ReleaseKey, W, A, D, LEFT, RIGHT


def straight():
	ReleaseKey(A)
	ReleaseKey(D)


def little_left():
	PressKey(A)
	PressKey(LEFT)
	ReleaseKey(LEFT)
	ReleaseKey(W)
	ReleaseKey(D)


def little_right():
	PressKey(D)
	PressKey(RIGHT)
	ReleaseKey(RIGHT)
	ReleaseKey(W)
	ReleaseKey(A)


def steer(center_pt, center_fixed, f_r, f_l):
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
