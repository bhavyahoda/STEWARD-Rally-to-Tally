#! /usr/bin/env python

import rospy
from ros_influx_endpoint import ROSInfluxEndpoint
from rospy.exceptions import ROSException
from steward_handler.msg import RoverStats
from steward_perception.msg import StackStats


def main():
    rospy.init_node("ros_influx_subscriber")

    rover_stats_topic = "rover_stats"
    stack_stats_topic = "stack_stats"

    rover_stats_sub = ROSInfluxEndpoint(rover_stats_topic, RoverStats)
    rover_stats_sub = ROSInfluxEndpoint(stack_stats_topic, StackStats)
    #imu_sub = ROSInfluxEndpoint(imu_topic, Imu)
    #cmd_vel_sub = ROSInfluxEndpoint(cmd_vel_topic, Twist)


if __name__ == "__main__":
    try:
        main()
        rospy.spin()
    except ROSException:
        pass
