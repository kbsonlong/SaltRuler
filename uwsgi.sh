#!/bin/sh
BASE_DIR="/data/PRG"
NAME="SaltRuler"
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
ps -ef | grep ftp.py | grep -v grep | awk '{print $2}' | xargs kill -9
echo  "################################################"
echo >$BASE_DIR/$NAME/uwsgi.log
#/usr/local/python27/bin/uwsgi --ini /data/PRG/SaltRuler/uwsgi.ini

su - mysql -c "/usr/local/python27/bin/uwsgi --ini $BASE_DIR/$NAME/uwsgi.ini"
cd $BASE_DIR/$NAME/deploy/
nohup /usr/local/python27/bin/python ftp.py  &
ps -ef | grep ftp.py | grep -v grep >>$BASE_DIR/$NAME/uwsgi.log