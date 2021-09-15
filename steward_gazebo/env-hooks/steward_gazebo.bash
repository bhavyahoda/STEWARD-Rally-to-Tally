#! /bin/bash

source /usr/share/gazebo/setup.bash
export GAZEBO_MODEL_PATH="${CATKIN_ENV_HOOK_WORKSPACE}/../src/steward/steward_gazebo/models/:${GAZEBO_MODEL_PATH}"
