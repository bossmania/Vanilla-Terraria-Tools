#!/usr/bin/env bash

# make it fail on error
set -eu

RUN_PYTHON=false

#check if using python or the binary
while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--python)
      RUN_PYTHON=true
      shift
      ;;
    *)
      SERVER_VERSION="$1"
      shift
      ;;
  esac
done

# invalid commands error
if [[ -z "${SERVER_VERSION:-}" ]]; then
  echo "Usage: $0 [-p|--python] <server_version>"
  exit 1
fi


# Only run python if -p or --python was provided
if [[ "$RUN_PYTHON" == true ]]; then
  # put the user in the venv if they're not already
  source venv/bin/activate

  #run the server
  python3 server_logic/server_controller.py \
    "$HOME/server_versions/$SERVER_VERSION/TerrariaServer.bin.x86_64" \
    -disableannouncementbox \
    -banlist "$HOME/admin/banlist.txt" \
    -config "$HOME/admin/config.txt"
else
  #set the binary to be executable
  chmod +x server_controller

  #run the binary
  ./server_controller \
    "$HOME/server_versions/$SERVER_VERSION/TerrariaServer.bin.x86_64" \
    -disableannouncementbox \
    -banlist "$HOME/admin/banlist.txt" \
    -config "$HOME/admin/config.txt"
fi
