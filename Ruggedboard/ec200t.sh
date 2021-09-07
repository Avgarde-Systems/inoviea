GPRS_DEV=ppp0
GPRS_MDM=/dev/ppp
CHECK_INTERVAL=1
DEBUG_FLAG=0
APP_FLAG=1

gprs_start () {
		echo "start"    
		pppd call quectel-ppp&
		sleep 5

}

gprs_stop (){
		echo "stop"
		rm -rf /var/lock/
		mkdir  /var/lock/
		killall pppd
		killall chat
}

app_start () {

if [ $APP_FLAG -ne 0 ];then
	    /usr/sbin/ntpd -u ntp:ntp -p /run/ntpd.pid -g
	    sleep 20
	 #   /home/root/Soil &
	    APP_FLAG=0
        fi
}
echo "test redial"
TEST_URL="www.google.com"
RETRY_NUM=1
FAIL_TIME=1
rm /var/lock/LCK..ttyS3
sleep 1
while true; do
    if [ -e ${GPRS_MDM} ];then
        parameter="-I ${GPRS_DEV} ${TEST_URL} -c 1"

        ping ${parameter} > /dev/null 2>&1
        result=$?

        if [ $DEBUG_FLAG -lt 0 ];then
            echo "result :: ${result}"
            echo "run cmd :: ping " ${parameter}
        fi

        if [ ${result} == 0 ];then
            echo "--------connected-------"
	    exit 1

        elif [ ${result} != 0 ];then
            echo "--------discconnected-------"
            if [ $FAIL_TIME -lt $RETRY_NUM ];then
                FAIL_TIME=$((FAIL_TIME + 1))
                echo "fail count : " $FAIL_TIME 
            else
                FAIL_TIME=1
                echo "redial at once"
                gprs_stop
                gprs_start
            fi
        fi
    else
        echo "Not exist"
    fi
    sleep  ${CHECK_INTERVAL}
done

