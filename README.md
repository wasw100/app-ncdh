#脑残对话#
 

使用tornado, sqlalchemy 开发的一个QQ空间应用, 应用地址: <http://my.qzone.qq.com/app/1101240590.html>

使用的数据库是MySQL

内容来源: [百度图片的脑残对话](http://image.baidu.com/channel/funny?fm=index#%E6%90%9E%E7%AC%91&%E8%84%91%E6%AE%8B%E5%AF%B9%E8%AF%9D&0&0)

* 初始化数据

在MySQL中建立数据库, 并在[database.py](https://github.com/wasw100/app-ncdh/blob/master/database.py)下将db_path设为自己MySQL对应的地址

执行init_data

    > python init_data.py

* 配置nginx

百度下的图片是限制外链的, 我们用nginx做一层反向代理, 为简单起见, web server和图片反向代理使用同一个域名, nginx配置如下:


    server {
        listen       80;
        server_name  ncdh.iqq7.com;

        location ^~ /image/ {
            resolver    114.114.114.114;
            proxy_pass  http://d.hiphotos.baidu.com;
            proxy_set_header Host d.hiphotos.baidu.com;
            proxy_set_header Referer http://image.baidu.com;
        }

        location ~ /static/ {
            root /data/web/app-ncdh/;
        }

        location /favicon.ico {
            root /data/web/app-ncdh/static/;
        }

        location /robots.txt {
            root /data/web/app-ncdh/static/;
        }

        location / {
             proxy_pass         http://127.0.0.1:9028;
             proxy_redirect     off;
             proxy_set_header   Host             $host;
             proxy_set_header   X-Real-IP        $remote_addr;
             proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }

    }



