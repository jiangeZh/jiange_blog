#概述
这是一个基于  **Django1.8**  跟  **Bootstrap3**  开发的 **博客系统** ，实现了一个博客完整的功能。

#开发平台以及主要工具

- 操作系统：Ubuntu 14.04 LTS

- 主要开发工具：Python2.7 + Django1.8 + Bootstrap3

- 数据库： SQLite 3（一款轻型的、遵守ACID的关系型数据库管理系统）

其他辅助工具：

- 头像库以及存储：Pillow & 七牛云

- 文本编辑：markdown2

- 代码高亮：highlight

- 图片展示：highslide

- 后台文章预览：django-pagedown

- 后台美化：bootstrap-admin

#功能
- 文章,分类,专栏的添加，删除，修改。支持**markdown**,支持文章中代码**高亮**。
- 实现**用户注册,登陆,修改密码,忘记重置密码**。通过**邮箱**通知注册用户, 用户忘记密码（基于邮件，需要在setting.py设置好邮箱)。
- 实现**用户头像**，用户可以上传头像，然后编辑头像大小，然后保存，头像可以存在本地，也可自动保存在**七牛**云中（需要在setting.py 中设置好七牛的相关配置）。
- **支持评论**，实现了一个独立的评论系统。
- 首页支持显示**轮播**，显示最新评论，显示人气最高的文章。
- 首页支持显示**标签云**，拥有一个非常酷炫的便签云。
- 拥有一个**动态加载**的“全部文章”板块 可以显示所有文章分类，可以按照浏览数或者时间排序显示文章。
- 支持**手机浏览**，对手机浏览进行了调整。
- 支持**RSS订阅**（注：chrome浏览器需要安装对应插件才能使用）

#演示地址
> www.jiangezh.com

#安装运行
安装virtualenv :

    sudo pip install virtualenv

创建并激活虚拟环境 :

    virtualenv www
    cd www
    source bin/acitve

安装Django1.8 :

    pip install Django==1.8

安装Pillow的依赖库：zlib，jpegsrc（下载源码自己编译），pip install python-dev

安装Pillow （因为处理头像要用到PIL库）:

    pip install Pillow


如果想使用七牛云替代本地存储头像，安装qiniu :

    pip install qiniu

如果使用sqlite，安装pytz :
    
    pip install pytz

使用bootstrap来美化后台：

pip install bootstrap-admin

安装markdown2：

pip install markdown2

安装pagedown

pip install django-pagedown 

下载代码,切换目录：
    
    git clone https://github.com/jiangeZh/jiange_blog
    cd jiange_blog

配置setting.py :

    vim jiange_blog/setting.py
设置其中的  PAGE\_NUM 每页显示文章数，EMAIL\_HOST(你用的邮箱的smtp)，EMAIL\_PORT(smtp端口)，EMAIL\_HOST\_USER(你的邮箱的用户名)，如果要使用七牛设置好七牛的相关配置。
EMAIL\_HOST\_PASSWORD(你的邮箱密码)，
```
    #分页配置#######################################
    PAGE_NUM = 3

    #email配置#########################################
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = ''                        #SMTP地址 例如: smtp.163.com
    EMAIL_PORT = 25                        #SMTP端口 例如: 25
    EMAIL_HOST_USER = ''                   #我自己的邮箱 例如: xxxxxx@163.com
    EMAIL_HOST_PASSWORD = ''               #我的邮箱密码 例如  xxxxxxxxx
    EMAIL_SUBJECT_PREFIX = u'jiange'        #为邮件Subject-line前缀,默认是'[django]'
    EMAIL_USE_TLS = True                   #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    #七牛配置#######################################
    qiniu_access_key = ''
    qiniu_secret_key = ''
    qiniu_bucket_name = ''
```

初始化数据库 :

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    
运行 :
    
    python manage.py runserver
    
#后台管理
访问http://127.0.0.1:8000/admin  
输入前面初始化数据库时的用户名密码。  

**特别注意**
首页的便签云中的内容，在后台不能修改。
请修改  blog/templates/blog/widgets/tags_cloud.html 中的 tags数组的内容。
