# test_blog
blog_system create by django2

<strong>使用django搭建的个人博客系统</strong>

# 主要功能有：
     提供了多用户注册和登陆博客
	 用户可以注册一个专属的博客站点，并配置个人详情比如头像、个人信息等。
	 用户可以在后台进行博客管理和发布博客
	 用户可以浏览其他用户的博客站点，进行点赞和评论
可以查看笔者发布到网站上的站点：http://106.12.61.7/

# 数据库配置：
本博客采用的数据库是sqllite3 并且提供了一份db.sqlite3数据库数据
本博客还采用了redis数据库进行用户浏览次数的记录 请先进行redis的安装

# 项目配置：
安装requirments.txt中的依赖包
在跟目录执行数据迁移：
python manage.py makemigrations
python manage.py migrate

然后执行：python manage.py runserver 127.0.0.1:8080
访问网站
在浏览器地址栏中访问http://127.0.0.1:8080

部分依赖包中可能需要去修改包中的配置（如passwordreset需要修改rervse的url redis_uploder需要修改上传图片时的权限）

#项目发布：
将本地项目部署在自己的云服务器上：（可以分别用Xshell和Xftp来连接服务器和传输文件）
    先分别安装 nginx和uwsgi
	输入 nginx -t 查看nginx.conf文件所在位置 修该其中server的配置,拉起静态文件和媒体文件
	
	server {
        listen       80;
        server_name  localhost;
        charset utf-8;
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:9010;
        }
        location /static/ {
            alias /root/test1/new_static/;
        }
        location /media/ {
            alias /root/test1/media/;
        }
		
		注意该配置文件中的第一行 用户 要有访问上述文件的权限 
		
安装uwsgi 项目的配置文件为根目录下的 uwsgi.ini 
输入下列命令 分别先关闭uwsgi和nginx防止端口占用 然后再启动
	输入命令
	   
	   pkill -9 uwsgi
	   uwsgi --ini uwsgi.ini
	   pkill -9 nginx
	   nginx

就可以远程访问自己服务器的IP 查看自己的项目

