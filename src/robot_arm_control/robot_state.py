#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotStateNode(Node):
    def __init__(self):
        super().__init__("robot_state")
        self.pub = self.create_publisher(String, "/robot/state", 10)
        self.timer = self.create_timer(1.0, self.publish_state)

    def publish_state(self):
        msg = String()
        msg.data = "running"
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotStateNode()
    rclpy.spin(node)
