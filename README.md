Ubskin API & Admin Site
==================
Configuration notes
------------
推荐使用 Nginx 作为本地 Web 服务器。  
复制 conf/vhost_dev.conf 为 conf/vhost_dev_xxx.conf，xxx 建议为用户名。
修改
```
root /Users/matt/Projects/ubskin_web/assets;
```
和
```
root /Users/matt/Projects/backup/ubskin/static;
```
为本地路径。  

然后在 Nginx 配置文件中添加该文件即可：  
```
include /Users/matt/Projects/ubskin_web/conf/vhost_dev.conf;
```

Development notes
------------
配置文件（涉及到路径、本机配置相关，都在这里设置，不要直接修改 config_web.py）：  
请在根目录创建 config_local.py，内容如下：
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ["STATIC_PATH"] = "/path/to/ubskin/static/"
```


HOST:
```
127.0.0.1       ubs_db
127.0.0.1       www-local.ubskin.net
127.0.0.1       s-local.ubskin.net
127.0.0.1       api-local.ubskin.net
127.0.0.1       admin-local.ubskin.net
127.0.0.1       m-local.ubskin.net
```
