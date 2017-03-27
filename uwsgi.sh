#!/bin/sh
NAME="SaltRuler"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

basedir=`pwd`

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
echo >/data/PRG/SaltRuler/uwsgi.log
#/usr/local/python27/bin/uwsgi --ini /data/PRG/SaltRuler/uwsgi.ini

su - mysql -c "/usr/local/python27/bin/uwsgi --ini /data/PRG/SaltRuler/uwsgi.ini"
su - mysql -c "nohup python $basedir/deploy/ftp.py >>$basedir/uwsgi.log &"