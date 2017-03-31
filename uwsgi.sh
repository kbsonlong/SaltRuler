#!/bin/sh
BASE_DIR="/data/PRG"
NAME="saltruler"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

stop(){
	echo "################################################"
	echo $NAME
	if [ -f $BASE_DIR/$NAME/$NAME.pid ];then
		cat $BASE_DIR/$NAME/$NAME.pid  | xargs kill -9
	else
		echo $NAME is stop
	fi
	ps -ef | grep ftp.py | grep -v grep | awk '{print $2}' | xargs kill -9
	echo  "################################################"
	echo >$BASE_DIR/$NAME/uwsgi.log
	rm -rf $BASE_DIR/$NAME/$NAME.pid
}

start(){
	su - mysql -c "/usr/local/python27/bin/uwsgi --ini $BASE_DIR/$NAME/uwsgi.ini" >/dev/null
	cd $BASE_DIR/$NAME/deploy/
	nohup /usr/local/python27/bin/python ftp.py  &
	cd $BASE_DIR/$NAME/
	nohup su - mysql -c "/usr/local/python27/bin/python  $BASE_DIR/$NAME/manage.py celery worker --loglevel=info  >>$BASE_DIR/$NAME/celery`date +%Y%m%d` " &
	ps -ef | grep ftp.py | grep -v grep >>$BASE_DIR/$NAME/uwsgi.log
	sleep 3
	ps -ef | grep "$NAME" | grep -v "grep" | awk '{print $2}' >$BASE_DIR/$NAME/$NAME.pid
}


status() {
	if [ -f $BASE_DIR/$NAME/$NAME.pid ];then
		echo $NAME is running....
	else
		echo $NAME is stop
	fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    *)
        echo $"Usage: $0 {start|stop|status}"
        exit 1
esac