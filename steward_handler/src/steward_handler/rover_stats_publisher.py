#! /usr/bin/env python

import rospy
import time
from rospy.exceptions import ROSException
from steward_handler.msg import RoverStats, PowerStats
from random import randint


class RoverStatsPublisher:
    def __init__(self) -> None:
        rospy.init_node("rover_stats_publisher")

        self.rover_stats_pub = rospy.Publisher("rover_stats", RoverStats, queue_size=10)

        self.battery_stats_sub = rospy.Subscriber("/mobile_base/power_stats", PowerStats, self.power_stats_cb)

        self.start_time_ms = time.time() * 1000

        rospy.wait_for_message("/mobile_base/power_stats", PowerStats)

        rospy.loginfo("rover_stats_publisher: Rover Stats Publisher initialized!")

    def power_stats_cb(self, msg):
        self.publish_rover_stats(msg)

    def publish_rover_stats(self, power_stats):
        battery_total_capacity = 5.2009

        rover_stats_msg = RoverStats()

        rover_stats_msg.battery_voltage = power_stats.battery_voltage
        rover_stats_msg.charge_estimate = power_stats.charge
        rover_stats_msg.capacity_estimate = int(power_stats.charge/battery_total_capacity * 100)
        rover_stats_msg.current_draw = power_stats.current_draw
        rover_stats_msg.uptime =  int(time.time() * 1000 - self.start_time_ms)
        rover_stats_msg.ros_control_loop_freq = 0.0
        rover_stats_msg.left_driver_temp = float(randint(30, 40))
        rover_stats_msg.right_driver_temp = float(randint(30, 40))
        rover_stats_msg.left_motor_temp = float(randint(30, 40))
        rover_stats_msg.right_motor_temp = float(randint(30, 40))

        self.rover_stats_pub.publish(rover_stats_msg)


if __name__ == "__main__":
    try:
        rover_stats_publisher = RoverStatsPublisher()
        
        rospy.spin()
    except ROSException:
        pass