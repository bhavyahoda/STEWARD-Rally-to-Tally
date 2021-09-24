# https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/

# USAGE
# python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
from Utils.centroid_tracker import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
# 	help="minimum probability to filter weak detections")
# args = vars(ap.parse_args())

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)

# load our serialized model from disk
# print("[INFO] loading model...")
# net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
# 
# # initialize the video stream and allow the camera sensor to warmup
# print("[INFO] starting video stream...")
vs = cv2.VideoCapture("camera_video.avi")
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# read the next frame from the video stream and resize it
	_, frame = vs.read()
	# frame = imutils.resize(frame, width=400)

	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame_gray = cv2.medianBlur(frame_gray, 5)

	# if the frame dimensions are None, grab them
	# if W is None or H is None:
	# 	(H, W) = frame.shape[:2]

	# construct a blob from the frame, pass it through the network,
	# obtain our output predictions, and initialize the list of
	# bounding box rectangles
	# blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
	# 	(104.0, 177.0, 123.0))
	# net.setInput(blob)
	# detections = net.forward()
	rects = []
	circles = cv2.HoughCircles(frame_gray, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=35, minRadius=0, maxRadius=40)
	print(circles)

	if circles is not None:
		circles = np.round(circles[0, :]).astype('int')

		# loop over the detections
		for (x, y, r) in circles:
			# filter out weak detections by ensuring the predicted
			# probability is greater than a minimum threshold
				# compute the (x, y)-coordinates of the bounding box for
				# the object, then update the bounding box rectangles list
			startX = x - r
			startY = y - r
			endX = x + r
			endY = y + r
			rects.append((startX, startY, endX, endY))
			# draw a bounding box surrounding the object so we can
			# visualize it
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)

	# update our centroid tracker using the computed set of bounding
	# box rectangles
	print(len(rects))
	objects = ct.update(rects)

	if objects is not None:
	# loop over the tracked objects
		for (objectID, centroid) in objects.items():
			# draw both the ID of the object and the centroid of the
			# object on the output frame
			text = "ID {}".format(objectID)
			cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.release()