#! /home/singh/.virtualenvs/cv/bin/python

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from rospy.exceptions import ROSException
from sensor_msgs.msg import Image
from std_msgs.msg import Empty
from circle_detection import get_centers


class PipeCounter:
    def __init__(self) -> None:
        rospy.init_node("pipe_counter")

        # maybe wont need this if we use contour detection directly to detect stack
        # else this used to start counting by ar_tag/qr_code detection script 
        self.start_counting_sub = rospy.Subscriber("/pipe_counter/start", Empty, self.start_counting_cb)
        rospy.loginfo("pipe_counter: subscriber created") 
        
        self.img_bridge = CvBridge()

        self.image_pub = rospy.Publisher("/pipe_counter/processed_image", Image, queue_size=10)

    def image_cb(self, image):
        try:
            cv_image = self.img_bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
        except CvBridgeError:
            rospy.logerr("pipe_counter: ERROR IN RECEIVING IMAGE")
        
        circles = get_centers(cv_image)

        if circles is not None:
            for(x, y, r) in circles:
                cv2.circle(cv_image, (x, y), r, (0, 255, 0), 4)
                print(x, y, r)
            
        img_with_circles = self.img_bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")

        self.image_pub.publish(img_with_circles)
    
    def start_counting_cb(self, msg):
        rospy.loginfo("pipe_counter: STARTING COUNTING PIPES!")

        self.image_sub = rospy.Subscriber("/image", Image, self.image_cb)


if __name__ == "__main__":
    try:
        pipe_counter = PipeCounter()
        rospy.spin()
    except ROSException:
        pass