#実機
alias CAN='sudo ip link set can0 type can bitrate 500000 ; sudo ip link set can0 up ; ip link show & gnome-terminal --window --geometry=80x24   -- bash run_can.bash'
alias LIDAR='gnome-terminal --window  --geometry=80x24   -- bash run_lidar.bash'
alias MCU='gnome-terminal --window  --geometry=80x24   -- bash run_mcu.bash'
alias MAP='gnome-terminal --window  --geometry=80x24   -- bash run_map.bash'
alias CONT='gnome-terminal --window  --geometry=80x24   -- bash run_controller.bash'
alias NAV='gnome-terminal --window  --geometry=80x24   -- bash run_nav.bash'
alias ALL='CAN ; LIDAR ; MCU ; MAP'

#シミュレーション
alias SIM='gnome-terminal --window  --geometry=80x24   -- bash run_sim.bash'
alias SIM_MAP='gnome-terminal --window  --geometry=80x24   -- bash run_map_sim.bash'


