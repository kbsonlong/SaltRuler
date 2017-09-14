#集成gateone配置

1、配置gateone认证方式，

    cd gateone
    python run_gateone.py --new_api_key
    # 生成一个api的key
    cd conf.d
    vim 10server.conf
    # 配置要调用gateone的web应用地址及端口
    "origins": ["localhost:10443", "127.0.0.1:10443","127.0.0.1:8088","172.16.13.80:8088"],
    # 修改origins这一行，添加应用地址及端口
    
    
    vim  20authentication.conf 
    配置认证方式
    "auth":"api",
    
    cat  30api_keys.conf
    // This file contains the key and secret pairs used by Gate One's API authentication method.
    {
        "*": {
            "gateone": {
                "api_keys": {
                    "ODdiN2QwZjI3OGUwNGQ4Njg2M2I5MTY3NTM1NTVjMWQyZ": "MTY5ZWVjYmU0YmFiNGYzNDliYjQxYWY2YTg2MjllNDc0N"
                }
            }
        }
    }
    
    # key1:secret1,key2:secret2,
    # 左边的是key，右边的是secret 后面调用的时候要用到
    
#2、将生成的新的配置文件复制到/etc/gateone/conf.d/目录替换原来

    cp 10server.conf /etc/gateone/conf.d/
    cp 20authentication.conf /etc/gateone/conf.d/
    cp 30api_keys.conf /etc/gateone/conf.d/