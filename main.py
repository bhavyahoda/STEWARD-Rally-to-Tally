import cv2

system_video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = system_video_capture.read()
	cv2.imshow("Frame", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

system_video_capture.release()
cv2.destroyAllWindows()
