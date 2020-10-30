#!/bin/sh

### BEGIN INIT INFO
# Provides:          myservice
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remoe_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
PYTHON_PATH=<Path to python executable>
DIR=<DIR Domoticz-Home-Connect-Plugin>
DAEMON=$DIR/homeconnectSSE.py
DEVICE_NAME=<Dishwasher, Washer or Oven>
DOMOTICZ_IP=<ip address of Domoticz>
DOMOTICZ_PORT=<port of hardware config in Domoticz>
DAEMON_NAME=homeconnectSSE_$DEVICE_NAME
DAEMON_LOG=<log location>$DAEMON_NAME.log
# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you ar using the Raspberry Pi GPIO from Python.
DAEMON_USER=<username>

# Add any command line options for your daemon here
DAEMON_OPTS="$DAEMON $DEVICE_NAME $DOMOTICZ_IP $DOMOTICZ_PORT $DAEMON_LOG"

#the process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec $PYTHON_PATH -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
