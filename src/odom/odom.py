import rclpy
from rclpy.node import Node
import can_msgs.msg
import sensor_msgs.msg
import nav_msgs.msg
import math
from tf2_ros import TransformBroadcaster, TransformStamped

class PyOdom(Node):
    def __init__(self):
        super().__init__('pyodom')

        self.pi = math.pi
        self.odom_broadcaster = TransformBroadcaster(self)

        self.can_receiver_subscriber = self.create_subscription(
                can_msgs.msg.Frame, 'from_can_bus', self.on_received_message, 10)

        self.imu_publisher = self.create_publisher(
                sensor_msgs.msg.Imu, 'imu', 10)
        
        self.odom_publisher = self.create_publisher(
                nav_msgs.msg.Odometry, 'odom', 1)
        
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def on_received_message(self, msg):
        if msg.id == 0x30:
            can_data = msg.data
            #self.yaw = int.from_bytes(can_data[0:2], 'little', signed=True) / 10.0 * self.pi / 180.0
            self.yaw = int.from_bytes(can_data[0:2], 'little', signed=True)  * self.pi / 180.0
            self.y = -1.0 * int.from_bytes(can_data[2:4], 'little', signed=True) / 1000.0
            self.x = 1.0 * int.from_bytes(can_data[4:6], 'little', signed=True) / 1000.0

    def timer_callback(self):
        print(self.x)
        print(self.y)
        print(self.yaw)
        print()

        cy = math.cos(self.yaw * 0.5)
        sy = math.sin(self.yaw * 0.5)

        stamp = self.get_clock().now().to_msg()

        odom_msg = nav_msgs.msg.Odometry()
        odom_msg.header.frame_id = "odom"
        odom_msg.header.stamp = stamp
        odom_msg.child_frame_id = "base_link"
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.orientation.w = cy
        odom_msg.pose.pose.orientation.z = sy

        imu_msg = sensor_msgs.msg.Imu()
        imu_msg.orientation.w = cy
        imu_msg.orientation.z = sy

        odom_trans = TransformStamped()
        odom_trans.header.frame_id = "odom"
        odom_trans.header.stamp = stamp
        odom_trans.child_frame_id = "base_link"
        odom_trans.transform.translation.x = odom_msg.pose.pose.position.x
        odom_trans.transform.translation.y = odom_msg.pose.pose.position.y
        odom_trans.transform.translation.z = 0.0
        odom_trans.transform.rotation = odom_msg.pose.pose.orientation

        self.odom_publisher.publish(odom_msg)
        # self.imu_publisher.publish(imu_msg)
        self.odom_broadcaster.sendTransform(odom_trans)

        # publish_odom(self.odom_publisher, self.imu_publisher, x, y, yaw)


def main(args=None):
    rclpy.init(args=args)

    pyodom = PyOdom()

    rclpy.spin(pyodom)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
