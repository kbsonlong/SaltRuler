#Cobbler安装

## 1、Cobbler一键安装脚本

    #!/bin/sh
    #coding=utf8
    ##################################################################
    #将如下IP修改成你cobbler服务器的IP地址
    ip=192.168.62.110
    #将如下net修改成你Cobbler所在网段的NET  
    net=192.168.62.0  
    #修改成dhcp计划分配的IP段
    begin=192.168.62.250
    end=192.168.62.253
    echo "$ip    www.along.party" >> /etc/hosts
    yum install cobbler cobbler-web pykickstart dhcp debmirror syslinux cman fence-agents  vim -y
    /etc/init.d/iptables stop
    /etc/init.d/httpd start
    /etc/init.d/cobblerd start
    service cobblerd restart
    sed -i -e 's/= yes/= no/g' /etc/xinetd.d/rsync
    sed -i -e 's/= yes/= no/g' /etc/xinetd.d/tftp
    sed -i 's@next_server: 127.0.0.1@next_server: '$ip'@g' /etc/cobbler/settings
    sed -i 's@server: 127.0.0.1@server: '$ip'@g' /etc/cobbler/settings
    cp /usr/share/syslinux/pxelinux.0 /var/lib/cobbler/loaders/
    cp  /usr/share/syslinux/meminfo.c32  /var/lib/cobbler/loaders/
    sed -i 's$@arches="i386"$#@arches="i386"$g' /etc/debmirror.conf
    sed  -i 's$@dists="sid"$#@dists="sid"$g' /etc/debmirror.conf
    sed -i 's@default_password_crypted@#default_password_crypted@g' /etc/cobbler/settings
    echo "default_password_crypted:  "$1$ac756ac7$erF27Ljjp3rDItLVqHLOg/"" >> /etc/cobbler/settings
    cobbler get-loaders
    service cobblerd restart
    cobbler sync
    ####用cobbler check 查看到底有哪些步骤没有操作完成。
    cobbler check
    #dhcp 
    cat > /etc/dhcp/dhcpd.conf <<EOF
    option domain-name "along.party";
    option domain-name-servers $ip;
    default-lease-time 43200;
    max-lease-time 86400;
    log-facility local7;
    subnet $net netmask 255.255.255.0 {
         range $begin $end;
         option routers $ip;
    }
    next-server $ip;
    filename="pxelinux.0";
    EOF
    /etc/init.d/dhcpd restart
    service xinetd  restart
    service cobblerd restart
    mkdir /opt/along
    mount /dev/cdrom /opt/along 
    cobbler import --name=centos-6.5-x86_64 --path=/opt/along

## 2、查看Cobbler

    [root@along install]# cobbler list
    distros:
       centos-6.5-x86_64
    
    profiles:
       centos-6.5-x86_64
    
    systems:
    
    repos:
    
    images:
    
    mgmtclasses:
    
    packages:
    
    files:

## 3、安装cobbler-web:

yum -y install cobbler-web


## 4、 设置用户名密码

为已存在的用户cobbler重置密码

htdigest /etc/cobbler/users.digest "Cobbler" cobbler  

添加新用户

htdigest /etc/cobbler/users.digest "Cobbler" along

## 5、配置cobbler web可以登录

sed -i 's/authn_denyall/authn_configfile/g' /etc/cobbler/modules.conf
## 6、 重启Cobbler与http

/etc/init.d/cobblerd restart 

/etc/init.d/httpd restart
## 7、 访问Cobbler Web页面,输入用户名密码能登录即可

浏览器访问登录页面https://192.168.62.110/cobbler_web

然后登录名就是：along  密码是输入密码

## 8、 把demo.cfg文件copy到目录：/var/lib/cobbler/kickstarts/ 目录下