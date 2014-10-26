#! /bin/bash
# /etc/init.d/ledbot.sh

### BEGIN INIT INFO
# Provides:          LEDscape and LEDbot
# Required-Start:    
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Run the LEDscape firmware, LEDbot server
# Description:       loads the correct DTS file and then the LEDscape and then LEDbot 
### END INIT INFO

# If you want a command to always run, put it here

. /lib/init/vars.sh

do_start () {
	#
	if grep -q CAPE-BONE-OCTO /sys/devices/bone_capemgr.8/slots
	then
		echo "CAPE-BONE-OCTO already set"
  	else 
   		echo "setting CAPE-BONE-OCTO"
 		echo CAPE-BONE-OCTO > /sys/devices/bone_capemgr.8/slots
 	
	fi
	if pgrep opc-rx>/dev/null 2>&1
	then
		echo "already running"
		exit 1
 	else
		echo "Starting LEDscape"
        	echo "sleeping for 5"
 		sleep 5
		bash -c 'cd /home/debian/LEDscape/; ./bin/opc-rx > /dev/null 2>&1'
		pgrep opc-rx > /var/run/opc-rx.pid

	fi
	if pgrep bot_scheduler >/dev/null 2>&1
	then
		echo "already running botscheduler"
		exit 1
	else
		echo "Starting bot scheduler"
		exec su - debian -c 'python /home/debian/LED-bot/LEDBot/bot_scheduler.py > /dev/null 2>&1 &'
	fi
	
}

do_stop () {
    pkill opc-rx
    rm /var/run/opc-rx.pid
    pkill bot_scheduler
}
	
do_status () {
	if [ -f /var/run/motd.dynamic ] ; then
		return 0
	else
		return 4
	fi
}



# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting ledbot and ledscape"
    do_start
    ;;
  stop)
    echo "Stopping ledbot and ledscape"
    # kill application you want to stop
    do_stop
    ;;
  restart)
    do_stop
    do_start
    ;;
  *)
    echo "Usage: /etc/init.d/ledbot.sh {start|stop}"
    exit 1
    ;;
esac

exit 0

