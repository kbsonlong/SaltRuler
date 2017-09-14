# SaltRunler


## 1、说明
由于是练手项目，将用过的工具都想成到项目中，所以项目功能比较杂，有些功能并不完整...目前集成服务有如下：

    a、saltstack     ##配置管理
    
    b、zabbix         ##zabbix监控
    
    c、docker registry  ##docker私有仓库管理
    
    d、gateone       ##web ssh
    
    e、SVN           ##利用saltstack svn模块发布代码
    
    f、jenkins       ##可持续迭代工具


##  2、安装步骤
### 2.1、安装 依赖关系
 
     yum install -y gcc-c++ git wget mysql-devel python-devel salt-master salt-api salt-minion 
    
    mkdir /tmp/soft -p 
    
    cd /tmp/soft 
    
    wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-12.0.3.tar.gz#md5=f07e4b0f4c1c9368fcd980d888b29a65 
    
    tar zxvf setuptools-12.0.3.tar.gz 
    
    cd setuptools-12.0.3 
    
    python setup.py install 
    
    easy_install pip  

### 2.2、下载源码

    git clone https://github.com/kbsonlong/SaltRuler.git

### 2.3、安装依赖

    pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com


    CREATE DATABASE IF NOT EXISTS saltruler DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

    GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY 'kbsonlong';

### 2.4、修改配置文件 SaltRuler/config.ini


### 2.5、同步数据库

    python manage.py makemigrations
    
    python manage.py migrate

####Django后台管理账户密码
    INSERT INTO `saltruler`.`auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES ('2', 'sha1$hmpYlKW04EUB$32f33bdbea3e9c818e626636d11a3456c7aaea09', NULL, '1', 'saltruler', '', '', '', '1', '1', '2017-03-28 08:37:41');

####平台账户密码
    INSERT INTO `saltruler`.`empauth_users` (`id`, `username`, `password`) VALUES ('2', 'saltruler', '8bb2135393b54831dcce04abdeb70f3e2c9ca420');


### 2.6、配置uwsgi + nginx

[uwsgi配置参考](/uwsgi.ini)

[nginx配置参考](/uwsgi_nginx.conf)


### 2.7、修改启动脚本uwsgi.sh

BASE_DIR="/data/PRG"         ##项目所在上级目录

NAME="SaltRuler"             ##如果重命名项目名称，需要修改

登录http://{ip}:{port}/
账号密码：saltruler/saltruler

as

### 2.8、配置gateone
[配置gateone](/gateone)



#截图


login界面
![image](/screenshots/login.jpg)

首页
![image](/screenshots/home.png)

minion认证管理
![image](/screenshots/minion_auth_man.png)



执行远程SHELL
![image](/screenshots/command.png)
执行States 模块
![image](/screenshots/STATES_Modules.png)

用户管理
![image](/screenshots/userinfo.png)

添加用户
![image](/screenshots/useradd.png)

修改密码
![image](/screenshots/userchange.png)


代码发布
![image](/screenshots/svn.png)

文件上传
![image](/screenshots/uploadfile.png)

文件下载
![image](/screenshots/downloadfile.png)


Cobbler装机平台

装机列表
![image](/screenshots/装机列表.png)

添加主机
![image](/screenshots/添加主机.png)

装机系统列表
![image](/screenshots/cobbler_profile.png)

添加装机系统
![image](/screenshots/添加装机系统.png)

系统镜像列表
![image](/screenshots/系统镜像列表.png)

添加系统镜像
![image](/screenshots/添加系统镜像.png)


物理服务器信息
![image](/screenshots/physical_server_info.png)

物理服务器详细信息
![image](/screenshots/physical_server_details_info.png)

服务器信息新增
![image](/screenshots/server_info_add.png)


操作审计
![image](/screenshots/shenji.png)


