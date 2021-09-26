#! /home/singh/.virtualenvs/cv/bin/python

import rospy
import pytz
import json
from steward_handler.msg import RoverStats
from rospy_message_converter import json_message_converter
from influxdb import InfluxDBClient
from datetime import datetime


class ROSInfluxEndpoint:
    def __init__(self, topic, msg_type) -> None:
        self.topic = topic
        self.msg_type = msg_type

        self.timezone = pytz.timezone("Asia/Kolkata")

        self.influx_client = InfluxDBClient('192.168.1.17', 8086, 'admin', 'Password1', 'mydb')
        self.influx_client.switch_database('mydb')

        self.msg_sub = rospy.Subscriber(self.topic, self.msg_type, self.msg_cb)

        print("Initializing subscriber for {}".format(self.topic))
        #rospy.wait_for_message(self.topic, self.msg_type, timeout=rospy.Duration(3))
        print("Initialized subscriber for {}".format(self.topic))

    def msg_cb(self, msg):
        msg_json = json_message_converter.convert_ros_message_to_json(msg)
        msg_json = json.loads(msg_json)

        if 'header' in msg_json:
            del msg_json['header']
   
        self.push_to_influx(msg_json)

    def push_to_influx(self, msg_json):
        json_payload = []
        data = {
            "measurement": self.topic,
            "tags": {
                "ticker": "TSLA" 
                },
            "time": datetime.now(self.timezone),
            "fields": msg_json
        }

        #print(data)

        json_payload.append(data)
        
        self.influx_client.write_points(json_payload)

        #print("Sent message of type {} to Influx mydb".format(self.msg_type))