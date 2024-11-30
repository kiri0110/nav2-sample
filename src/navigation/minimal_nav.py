import rclpy
import rclpy.logging
from rclpy.node import Node
import geometry_msgs.msg
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import math
import time
import quaternion

class Commander(Node):
    def __init__(self):
        super().__init__('commander')
        self.get_logger().info("Start!")

        self.nav = BasicNavigator()

        #TFの取得->初期位置の設定
        try:
            self.tfBuffer = Buffer()
            self.tfListener = TransformListener(self.tfBuffer, node=self)
            tf_baselink = self.tfBuffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().error(f"Failed to get transform: {ex}")
        else:
            x = tf_baselink.transform.translation.x
            y = tf_baselink.transform.translation.y
            z = tf_baselink.transform.rotation.z
            w = tf_baselink.transform.rotation.w
            initial_pose = geometry_msgs.msg.PoseStamped()
            initial_pose.header.frame_id = 'map'
            initial_pose.header.stamp = self.get_clock().now().to_msg()
            initial_pose.pose.position.x = x
            initial_pose.pose.position.y = y
            initial_pose.pose.orientation.z = z
            initial_pose.pose.orientation.w = w
            self.nav.setInitialPose(initial_pose)
        
        #GOALの設定
        self.goal0 = self.create_pose(x = 1.0, y = 1.0, yaw = 0.0)
        self.goal1 = self.create_pose(x = 1.5, y = 1.0, yaw = 0.0)
        self.goal2 = self.create_pose(x = 2.0, y = 1.0, yaw = 0.0)


    def create_pose(self, x, y, yaw):
        pose = geometry_msgs.msg.PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        q = quaternion.from_euler_angles(0,0,yaw)
        pose.pose.orientation.z = q.z
        pose.pose.orientation.w = q.w
        return pose

    def run(self):
        # self.nav.waitUntilNav2Active()
        self.nav.lifecycleStartup()

        #goal0に移動
        self.nav.goToPose(self.goal0)
        self.get_logger().info("moving to goal0")
        while not self.nav.isTaskComplete():
            time.sleep(0.05)
        result = self.nav.getResult()
        rclpy.logging.get_logger('minimal_nav').info(f"Result: {result}")
        time.sleep(1)

        for _ in range(3):  # 3回往復
            #goal1
            self.nav.goToPose(self.goal1)
            self.get_logger().info("moving to goal1")
            while not self.nav.isTaskComplete():
                time.sleep(0.05)
            result = self.nav.getResult()
            rclpy.logging.get_logger('minimal_nav').info(f"Result: {result}")

            time.sleep(3)

            #goal2
            self.nav.goToPose(self.goal2)
            self.get_logger().info("moving to goal2")
            while not self.nav.isTaskComplete():
                time.sleep(0.05)
            result = self.nav.getResult()
            rclpy.logging.get_logger('minimal_nav').info(f"Result: {result}")

            time.sleep(3)

def main(args=None):
    rclpy.init(args=args)
    node = Commander()
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("Interrupted by user, shutting down.")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
