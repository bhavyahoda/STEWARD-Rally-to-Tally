#! /home/singh/.virtualenvs/cv/bin/python

import rospy
import os
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Empty


class VideoSaver:
    def __init__(self) -> None:
        rospy.init_node("video_saver")

        self.img_bridge = CvBridge()

        self.start_recording_sub = rospy.Subscriber("/video_saver/start", Empty, self.start_recording_cb)
        self.start_recording_sub = rospy.Subscriber("/video_saver/stop", Empty, self.stop_recording_cb)

        self.recording_started = False

        self.image_sub = rospy.Subscriber("/image", Image, self.image_cb)

        rospy.wait_for_message("/image", Image)

        rospy.loginfo("video_saver: Image received! Setting frame height and width")
        
        self.image_sub.unregister()

    def image_cb(self, img):
        self.frame_width = img.width
        self.frame_height = img.height

        if(self.recording_started):
            try:
                cv_image = self.img_bridge.imgmsg_to_cv2(img, "bgr8")
            except CvBridgeError as e:
                print(e)
            self.video_writer.write(cv_image)

    def start_recording_cb(self, msg):
        self.image_sub = rospy.Subscriber("/image", Image, self.image_cb)
        curr_path = os.path.dirname(__file__)
        self.video_writer = cv2.VideoWriter(curr_path + "/camera_video.avi", 
                                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                        30, (self.frame_width, self.frame_height))
        self.recording_started = True
        rospy.loginfo("video_saver: STARTED RECORDING!")
    
    def stop_recording_cb(self, msg):
        self.image_sub.unregister()
        self.video_writer.release()
        self.recording_started = False
        rospy.loginfo("video_saver: STOPPED RECORDING!")


if __name__ == "__main__":
    try:
        video_saver = VideoSaver()

        rospy.spin()
    except rospy.ROSException:
        pass