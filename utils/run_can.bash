gnome-terminal --tab -t "CAN SENDER" -- bash -c "ros2 launch ros2_socketcan socket_can_sender.launch.py interface:=can0 ; bash"

sleep 1

gnome-terminal --tab -t "CAN RECEIVER" -- bash -c "ros2 launch ros2_socketcan socket_can_receiver.launch.py interface:=can0 filters:=0X30:0X7f8 interval_sec:=1.0 ; bash"
