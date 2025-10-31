#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 {yaw|pitch|roll}"
  exit 1
fi

TEST_NAME=$1
CONFIG_FILE="tests/phaseA_pose_only/configs/phaseA.config.yaml"
OVERRIDE_FILE="tests/phaseA_pose_only/configs/${TEST_NAME}.override.yaml"
M0_RUNNER="m0_runner.py"

if [ ! -f "$OVERRIDE_FILE" ]; then
  echo "Error: Override file not found for test: ${TEST_NAME}"
  exit 1
fi

python $M0_RUNNER --config $CONFIG_FILE --override $OVERRIDE_FILE
