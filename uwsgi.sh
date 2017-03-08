#!/bin/sh
NAME="salt_runler"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

echo $NAME
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
echo $ID
echo "################################################"
for id in $ID
do
    kill -9 $id
    echo "kill $id"
done
echo  "################################################"
echo >/data/PRG/salt_runler/uwsgi.log
#/usr/local/python27/bin/uwsgi --ini /data/PRG/salt_runler/uwsgi.ini

su - mysql -c "/usr/local/python27/bin/uwsgi --ini /data/PRG/salt_runler/uwsgi.ini"