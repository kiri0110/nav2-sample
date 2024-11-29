#!/bin/bash

# ディレクトリを取得
MY_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_PATH="`cd $MY_DIR && cd .. && pwd`"
cd ..

  # AMCL Map Server の起動
  gnome-terminal --tab -t "MAP_AMCL" -- bash -c "ros2 run nav2_map_server map_server --ros-args --remap __node:=map_server_amcl --params-file $WORKSPACE_PATH/src/navigation/config/map_amcl_params.yaml -p use_sim_time:=False; bash"

  sleep 1

  # Lifecycle Manager の起動
  gnome-terminal --tab -t "MAP_AMCL_LIFECYCLE" -- bash -c \
    "ros2 run nav2_lifecycle_manager lifecycle_manager --ros-args -p autostart:=True -p node_names:=['map_server_amcl'] -p use_sim_time:=False; bash"

  sleep 1

  # RViz2 の起動
  gnome-terminal --tab -t "RVIZ2" -- bash -c \
    "source install/local_setup.bash ; \
    cd $WORKSPACE_PATH/src/navigation/launch ; \
    ros2 launch simple.launch.py urdf:=$WORKSPACE_PATH/urdf/er.urdf.xacro map:=$WORKSPACE_PATH/src/navigation/map/field.yaml rviz_config_file:=$WORKSPACE_PATH/src/navigation/rviz/nav2_default_view.rviz params_file:=$WORKSPACE_PATH/src/navigation/config/nav2_params_critics.yaml use_sim_time:=False  ; bash"


