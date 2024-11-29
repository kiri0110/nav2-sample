cd ..

gnome-terminal --tab -t "ODOM" -- bash -c "cd src/odom ; python3 odom.py ; bash"

sleep 1

gnome-terminal --tab -t "ASHI" -- bash -c "cd src/mobile_base ; python3 mobile_base.py ; bash"
