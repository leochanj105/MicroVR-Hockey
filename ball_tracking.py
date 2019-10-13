# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import multiprocessing

def main_a(pipe):
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help="path to the (optional) video file")
	ap.add_argument("-b", "--buffer", type=int, default=64,
		help="max buffer size")
	args = vars(ap.parse_args())

	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space, then initialize the
	# list of tracked points
	greenLower = (29, 86, 6)
	greenUpper = (64, 255, 255)

	redLower = (169, 100, 100)
	redUpper = (189, 255, 255)

	pts_green = deque(maxlen=args["buffer"])
	pts_red = deque(maxlen=args["buffer"])

	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		vs = VideoStream(src=0).start()

	# otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])
		

	# allow the camera or video file to warm up
	time.sleep(2.0)

	# keep looping
	while True:
		time.sleep(0.001)

		# grab the current frame
		# print("width = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)") 
		# print("height = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT")
		
		frame = vs.read()

		# handle the frame from VideoCapture or VideoStream
		frame = frame[1] if args.get("video", False) else frame

		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		if frame is None:
			break

		# resize the frame, blur it, and convert it to the HSV
		# color space
		#600x340
		frame = imutils.resize(frame, width=600)

		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		# construct a mask_green for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask_green
		mask_green = cv2.inRange(hsv, greenLower, greenUpper)
		mask_green = cv2.erode(mask_green, None, iterations=2)
		mask_green = cv2.dilate(mask_green, None, iterations=2)

		mask_red = cv2.inRange(hsv, redLower, redUpper)
		mask_red = cv2.erode(mask_red, None, iterations=2)
		mask_red = cv2.dilate(mask_red, None, iterations=2)


		# find contours in the mask_green and initialize the current
		# (x, y) center_green of the ball
		cnts_green = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts_green = imutils.grab_contours(cnts_green)
		center_green = None

		cnts_red = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts_red = imutils.grab_contours(cnts_red)
		center_red = None


		# only proceed if at least one contour was found
		if (len(cnts_green) > 0 and len(cnts_red) > 0):
			# find the largest contour in the mask_green, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts_green, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center_green = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			center_green_x_pos = 1.0 - center_green[0] / 600
			center_green_y_pos = center_green[1] / 340
			center_green_x_pos = min(max(0.0, center_green_x_pos), 1.0)
			center_green_y_pos = min(max(0.0, center_green_y_pos), 1.0)

			d = max(cnts_red, key=cv2.contourArea)
			((x1, y1), radius1) = cv2.minEnclosingCircle(d)
			N = cv2.moments(d)
			center_red = (int(N["m10"] / N["m00"]), int(N["m01"] / N["m00"]))
			
			center_red_x_pos = 1.0 - center_red[0] / 600
			center_red_y_pos = center_red[1] / 340
			center_red_x_pos = min(max(0.0, center_red_x_pos), 1.0)
			center_red_y_pos = min(max(0.0, center_red_y_pos), 1.0)

			pipe.send((center_green_x_pos, center_green_y_pos, center_red_x_pos, center_red_y_pos))

			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center_green, 5, (0, 0, 255), -1)

			if radius1 > 10:
				cv2.circle(frame, (int(x1), int(y1)), int(radius1),
					(0, 255, 255), 2)
				cv2.circle(frame, center_red, 5, (0, 0, 255), -1)

		# update the points queue
		pts_green.appendleft(center_green)

		pts_red.appendleft(center_red)

		# loop over the set of tracked points
		for i in range(1, len(pts_green)):
			# if either of the tracked points are None, ignore
			# them
			if pts_green[i - 1] is None or pts_green[i] is None:
				continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts_green[i - 1], pts_green[i], (0, 0, 255), thickness)
				
		# # show the frame to our screen
		# cv2.imshow("Frame", frame)
		# key = cv2.waitKey(1) & 0xFF

		# # if the 'q' key is pressed, stop the loop
		# if key == ord("q"):
		# 	break

		for j in range(1, len(pts_red)):
			# if either of the tracked points are None, ignore
			# them
			if pts_red[j - 1] is None or pts_red[j] is None:
				continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness1 = int(np.sqrt(args["buffer"] / float(j + 1)) * 2.5)
			cv2.line(frame, pts_red[j - 1], pts_red[j], (0, 0, 255), thickness1)

		# show the frame to our screen
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	# if we are not using a video file, stop the camera video stream
	if not args.get("video", False):
		vs.stop()

	# otherwise, release the camera
	else:
		vs.release()

	# close all windows
	cv2.destroyAllWindows()
	pipe.send("OVER")