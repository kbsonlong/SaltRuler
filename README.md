# SaltRunler

1、下载源码

git clone https://github.com/kbsonlong/SaltRuler.git

2、安装依赖

pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com


3、修改配置文件 SaltRuler/config.ini


4、同步数据库

python manage.py makemigrations

python manage.py migrate

INSERT INTO `saltruler`.`auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES ('2', 'sha1$hmpYlKW04EUB$32f33bdbea3e9c818e626636d11a3456c7aaea09', NULL, '1', 'saltruler', '', '', '', '1', '1', '2017-03-28 08:37:41');
INSERT INTO `saltruler`.`empauth_users` (`id`, `username`, `password`) VALUES ('2', 'saltruler', '8bb2135393b54831dcce04abdeb70f3e2c9ca420');


5、配置uwsgi + nginx

uwsgi配置参考（https://github.com/kbsonlong/SaltRuler/blob/master/uwsgi.ini）

nginx配置参考（https://github.com/kbsonlong/SaltRuler/blob/master/uwsgi_nginx.conf）


6、修改启动脚本uwsgi.sh

BASE_DIR="/data/PRG"         ##项目所在上级目录

NAME="SaltRuler"             ##如果重命名项目名称，需要修改

登录http://{ip}:{port}/


#截图


login界面
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/login.jpg)

首页
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/home.png)

minion认证管理
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/minion_auth_man.png)



执行远程SHELL
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/command.png)
执行States 模块
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/STATES_Modules.png)

用户管理
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/userinfo.png)

添加用户
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/useradd.png)

修改密码
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/userchange.png)


代码发布
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/svn.png)

文件上传
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/uploadfile.png)

文件下载
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/downloadfile.png)



物理服务器信息
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/physical_server_info.png)

物理服务器详细信息
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/physical_server_details_info.png)

服务器信息新增
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/server_info_add.png)


操作审计
![image](https://github.com/kbsonlong/SaltRuler/blob/master/screenshots/shenji.png)


