
import sys
import json
import struct

import rclpy
from rclpy.node import Node

import geometry_msgs.msg
import can_msgs.msg

def serialize_float(f):
    return bytearray(struct.pack('<f', f))

def serialize_int(h):
    return bytearray(struct.pack('<h', h))


class WheelsSerializer:
    CAN_MSG_ID_WHEEL=0x101

    def construct_can_frame(self, vx, vy, omega):
    
        fv_frame = can_msgs.msg.Frame(id=self.CAN_MSG_ID_WHEEL, dlc=6, data=
                serialize_int(
                    int(vx)
                )
                + serialize_int(
                    int(vy)
                )
                + serialize_int(
                    int(omega * 100) 
                )
                + serialize_int(
                    0
                )
            )
    
        return fv_frame


class PyAshi(Node):
    def __init__(self, wser):
        super().__init__('pyashi')

        self.wser = wser

        self.ashi_subscriber = self.create_subscription(
                geometry_msgs.msg.Twist, 'cmd_vel', self.on_received_message, 10)

        self.can_sender_publisher = self.create_publisher(
                can_msgs.msg.Frame, 'to_can_bus', 10)

    def on_received_message(self, msg):
        # vx[mm/s] vy[mm/s] omega[rad/s]
        vy = msg.linear.x * 1000.0
        vx = msg.linear.y * 1000.0 * -1.0
        omega = msg.angular.z

        frame = self.wser.construct_can_frame(vx, vy, omega)

        self.can_sender_publisher.publish(frame)

def main(args=None):
    rclpy.init(args=args)

    pyashi = PyAshi(WheelsSerializer())

    rclpy.spin(pyashi)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

