gnome-terminal --tab -t "LIDAR SETUP" -- bash -c "cd .. ; source install/local_setup.bash ; echo 'ros2 launch urg_node2 urg_node2.launch.py' ; ros2 launch urg_node2 urg_node2.launch.py ; bash"
