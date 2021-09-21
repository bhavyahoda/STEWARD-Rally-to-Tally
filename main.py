import cv2
import glob
from circle_detection import get_centers

mp4_video = glob.glob(r"./*.mp4")[0]
local_video_capture = cv2.VideoCapture(mp4_video)

while True:
    ret, frame = local_video_capture.read()
    circles = get_centers(frame)
    for(x, y, r) in circles:
        cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
        print(x, y)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

local_video_capture.release()
cv2.destroyAllWindows()
