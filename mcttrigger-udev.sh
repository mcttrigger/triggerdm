#!/bin/sh
# Copyright (c) 2016 -2024 Magic Control Technology Corp.

# Start the mcttrigger service.
start_mcttrigger() {
	start_service
}

# Stop the mcttrigger service.
stop_mcttrigger() {
	stop_service
}

# Evdi can be a built-in or not.
build_in_EVDI() {
  local EVDI_ADD="/sys/devices/evdi/add"

  modprobe evdi || true
  # Allow smdisplay (in video group) write to evdi/add.
  chgrp video "${EVDI_ADD}"
  chmod g+w "${EVDI_ADD}"
}

main() {
  local action="$ACTION"

  if [ "${action}" = "add" ]; then
    build_in_EVDI
    start_mcttrigger
  elif [ "${action}" = "remove" ]; then
    stop_mcttrigger
  elif [ "${action}" = "START" ]; then
    build_in_EVDI
    start_mcttrigger
  else
    echo "Invalid action."
    return
  fi
}

# Start the service.
start_service() {
  start mcttrigger
}

# Stop the service.
stop_service() {
  stop mcttrigger
}

action="$1"

main "${action}"
