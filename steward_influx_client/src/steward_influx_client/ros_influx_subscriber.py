#! /usr/bin/env python

import rospy
from ros_influx_endpoint import ROSInfluxEndpoint
from rospy.exceptions import ROSException
from steward_handler.msg import RoverStats
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist


def main():
    rospy.init_node("ros_influx_subscriber")

    rover_stats_topic = "rover_stats"
    imu_topic = "imu/data"
    cmd_vel_topic = "cmd_vel"

    rover_stats_sub = ROSInfluxEndpoint(rover_stats_topic, RoverStats)
    #imu_sub = ROSInfluxEndpoint(imu_topic, Imu)
    #cmd_vel_sub = ROSInfluxEndpoint(cmd_vel_topic, Twist)


if __name__ == "__main__":
    try:
        main()
        rospy.spin()
    except ROSException:
        pass
