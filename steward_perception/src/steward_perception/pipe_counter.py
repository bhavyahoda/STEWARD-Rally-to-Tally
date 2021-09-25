#! /home/singh/.virtualenvs/cv/bin/python

from inspect import stack
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from rospy.exceptions import ROSException
from rospy.timer import sleep
from sensor_msgs.msg import Image
from std_msgs.msg import Empty, Int32
from Utils.circle_detection import get_centers
from Utils.centroid_tracker import CentroidTracker
from Utils.trackable_object import TrackableObject
from steward_perception.msg import StackStats


class PipeCounter:
    def __init__(self) -> None:
        rospy.init_node("pipe_counter")

        # maybe wont need this if we use contour detection directly to detect stack
        # else this used to start counting by ar_tag/qr_code detection script 
        self.start_counting_sub = rospy.Subscriber("/pipe_counter/start", Empty, self.start_counting_cb)
        self.stop_counting_pub = rospy.Subscriber("/pipe_counter/stop", Empty, self.stop_counting_cb)
        rospy.loginfo("pipe_counter: subscriber created") 
        
        self.img_bridge = CvBridge()
        self.centroid_tracker = CentroidTracker()
        self.count = 0
        self.total_frames = 0
        self.skip_frames = 1
        self.trackers = []
        self.tracked_objects = {}

        self.stacks = {
            'A': {
                'pipe_od': '48inch',
                'pipe_manu_type': 'seamless',
                'pipe_material': 'steel'
            },
            'B': {
                'pipe_od': '24inch',
                'pipe_manu_type': 'seamed',
                'pipe_material': 'steel'
            },
            'C': {
                'pipe_od': '36inch',
                'pipe_manu_type': 'seamed',
                'pipe_material': 'steel'
            }
        }

        self.stack_counted = 0
        self.mission = '26 September 2021'

        self.image_pub = rospy.Publisher("/pipe_counter/processed_image", Image, queue_size=10)
        self.stack_stats_pub = rospy.Publisher("/pipe_counter/stack_stats", StackStats, queue_size=10)

    def image_cb(self, image):
        try:
            cv_image = self.img_bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
        except CvBridgeError:
            rospy.logerr("pipe_counter: ERROR IN RECEIVING IMAGE")

        frame_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        rects = []
        
        if self.total_frames % self.skip_frames == 0:
            self.trackers = []
            circles = get_centers(cv_image)
    
            if circles is not None:
                for(x, y, r) in circles:
                    cv2.circle(cv_image, (x, y), r, (0, 255, 0), 2)
                    startX = x - r
                    startY = y - r
                    endX = x + r
                    endY = y + r
                    rects.append((startX, startY, endX, endY))

        cv2.line(cv_image, 
                (cv_image.shape[1]//2, 0), 
                (cv_image.shape[1]//2, cv_image.shape[0]),
                (0, 255, 0), 2)

        tracked_circles = self.centroid_tracker.update(rects, self.tracked_objects)
    
        if tracked_circles is not None:
            for (objectID, centroid) in tracked_circles.items():
                tracked_object = self.tracked_objects.get(objectID, None)
                
                if tracked_object is None:
                    tracked_object = TrackableObject(objectID, centroid)
                
                else:
                        if not tracked_object.isCounted:
                            if centroid[0] == cv_image.shape[1]//2:
                                print("Counted ID: {}".format(objectID))
                                self.count += 1
                                tracked_object.isCounted = True
                                cv2.circle(cv_image, (centroid[0], centroid[1]), 35, (0, 0, 255), 2)
                
                self.tracked_objects[objectID] = tracked_object

                cv2.putText(cv_image, "ID: {}".format(objectID), 
                            (centroid[0] - 10, centroid[1] - 10), 
                            cv2.FONT_HERSHEY_COMPLEX, 
                            0.5, (0, 255, 0), 2)
                cv2.circle(cv_image, (centroid[0], centroid[1]),
                            4, (0, 255, 0), -1)

        cv2.putText(cv_image, str(self.count), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        img_with_circles = self.img_bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.total_frames += 1

        self.image_pub.publish(img_with_circles)
    
    def start_counting_cb(self, msg):
        rospy.loginfo("pipe_counter: STARTING COUNTING PIPES!")

        self.count = 0

        self.image_sub = rospy.Subscriber("/image", Image, self.image_cb)

    def stop_counting_cb(self, msg):
        rospy.loginfo("pipe_counter: STOPPED COUNTING STACK")

        stack_stats_msg = StackStats()
        stack_stats_msg.id = self.stacks[self.stack_counted]['id']
        stack_stats_msg.count = self.count
        stack_stats_msg.mission = self.mission
        stack_stats_msg.pipe_manu_type = self.stacks[self.stack_counted]['pipe_manu_type']
        stack_stats_msg.pipe_material = self.stacks[self.stack_counted]['pipe_material']
        stack_stats_msg.pipe_od = self.stacks[self.stack_counted]['pipe_od']

        self.stack_stats_pub.publish(stack_stats_msg)

        rospy.loginfo("pipe_counter: Counted Stack id: {}".format(self.stacks[self.stack_counted]['id']))

        self.stack_counted += 1


if __name__ == "__main__":
    try:
        pipe_counter = PipeCounter()
        rospy.spin()
    except ROSException:
        pass