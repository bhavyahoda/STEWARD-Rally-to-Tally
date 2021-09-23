#! /bin/bash

source /usr/share/gazebo/setup.bash
export GAZEBO_MODEL_PATH="${CATKIN_ENV_HOOK_WORKSPACE}/../src/steward/steward_gazebo/models/:${GAZEBO_MODEL_PATH}"
export GAZEBO_PLUGIN_PATH="${CATKIN_ENV_HOOK_WORKSPACE}/../src/brass_gazebo_battery/build/devel/lib/:${GAZEBO_MODEL_PATH}"
