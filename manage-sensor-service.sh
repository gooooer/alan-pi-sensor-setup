#!/usr/bin/env bash
set -euo pipefail

# Simple manager for the systemd unit that runs the sensor script.
# Usage:
#   ./manage-sensor-service.sh init         # install/enable/start service
#   ./manage-sensor-service.sh reinstall    # copy unit, reload, restart
#   ./manage-sensor-service.sh start|stop|restart|status
#   ./manage-sensor-service.sh logs         # follow logs
#   ./manage-sensor-service.sh logs-since "1 hour ago"
#   ./manage-sensor-service.sh enable|disable
#   ./manage-sensor-service.sh reload       # systemd daemon-reload only
#
# Options (env or flags):
#   SERVICE_NAME=sensor.service
#   SERVICE_FILE=./etc/systemd/system/sensor.service
#
# Flags:
#   --service-name <name>
#   --service-file <path>

SERVICE_NAME="${SERVICE_NAME:-sensor.service}"
SERVICE_FILE="${SERVICE_FILE:-./etc/systemd/system/sensor.service}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --service-name) SERVICE_NAME="$2"; shift 2 ;;
    --service-file) SERVICE_FILE="$2"; shift 2 ;;
    *) CMD="${1:-}"; shift; ARGS=("$@"); break ;;
  esac
done

CMD="${CMD:-help}"

require_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "This action requires root. Re-run with: sudo $0 $CMD"
    exit 1
  fi
}

copy_unit() {
  if [[ ! -f "$SERVICE_FILE" ]]; then
    echo "Unit file not found: $SERVICE_FILE"
    exit 1
  fi
  echo "Installing unit to /etc/systemd/system/${SERVICE_NAME}"
  install -m 0644 "$SERVICE_FILE" "/etc/systemd/system/${SERVICE_NAME}"
}

daemon_reload() {
  systemctl daemon-reload
}

do_init() {
  require_root
  copy_unit
  daemon_reload
  systemctl enable "$SERVICE_NAME"
  systemctl start "$SERVICE_NAME"
  systemctl status "$SERVICE_NAME" --no-pager || true
}

do_reinstall() {
  require_root
  copy_unit
  daemon_reload
  systemctl restart "$SERVICE_NAME"
  systemctl status "$SERVICE_NAME" --no-pager || true
}

case "$CMD" in
  init)
    do_init
    ;;
  reinstall)
    do_reinstall
    ;;
  reload)
    require_root
    daemon_reload
    ;;
  start|stop|restart|enable|disable|status)
    require_root
    systemctl "$CMD" "$SERVICE_NAME"
    [[ "$CMD" == "status" ]] && exit 0
    systemctl status "$SERVICE_NAME" --no-pager || true
    ;;
  logs)
    # follow logs
    exec journalctl -u "$SERVICE_NAME" -f
    ;;
  logs-since)
    SINCE="${ARGS[0]:-1 hour ago}"
    exec journalctl -u "$SERVICE_NAME" --since "$SINCE" -f
    ;;
  help|*)
    cat <<EOF
Usage: $0 [--service-name NAME] [--service-file PATH] <command>

Commands:
  init            Copy unit, daemon-reload, enable, start, show status
  reinstall       Copy unit, daemon-reload, restart, show status
  reload          systemctl daemon-reload only
  start|stop|restart|enable|disable|status
  logs            Follow service logs (journalctl -f)
  logs-since T    Follow logs since time T (e.g., "30 min ago", "today")

Defaults:
  SERVICE_NAME=$SERVICE_NAME
  SERVICE_FILE=$SERVICE_FILE

Examples:
  sudo $0 init
  sudo $0 --service-file ./sensor.service reinstall
  $0 logs
  $0 logs-since "today"
EOF
    ;;
esac