#coding:utf-8
from django import template
from django import forms
from django.http import HttpResponse,Http404
from django.shortcuts import render,render_to_response
from django.template import Context,loader
from django.views.generic import View,TemplateView,ListView,DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.syndication.views import Feed
from blog.models import Article,Category,Carousel,Column,Nav,News,Message,Link
from jiange_comments.models import Comment
from jiange_auth.models import jiangeUser
from jiange_auth.forms import jiangeUserCreationForm,jiangePasswordRestForm
from jiange_blog.settings import PAGE_NUM
import datetime,time
import json
import logging


#缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

#logger
logger = logging.getLogger(__name__)


class BaseMixin(object):
    
    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)
        try:
            #热门文章
            context['hot_article_list'] = Article.objects.order_by("-view_times")[0:10]
            #导航条
            context['nav_list'] =  Nav.objects.filter(status=0)
            #最新评论
            context['latest_comment_list'] = Comment.objects.order_by("-create_time")[0:10]
			#友情链接
            context['link_list'] = Link.objects.all()

        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context


class IndexView(BaseMixin,ListView):
    template_name = 'index.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM #分页--每页的数目
    
    def get_context_data(self,**kwargs):
        #轮播
        kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView,self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0).exclude(en_title = 'aboutme')
        return article_list
    

class ArticleView(BaseMixin,DetailView):
    queryset = Article.objects.filter(status=0)
    template_name = 'article.html'
    context_object_name = 'article'
    slug_field = 'en_title'

    def get(self,request,*args,**kwargs):
        #统计文章的访问访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip

        en_title = self.kwargs.get('slug')
        #获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get(en_title,[])
        
        #如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article = self.queryset.get(en_title=en_title)
            except Article.DoesNotExist:
                logger.error(u'[ArticleView]访问不存在的文章:[%s]' % en_title)
                raise Http404
            else:
                article.view_times += 1
                article.save()
                visited_ips.append(ip)

            #更新缓存
            cache.set(en_title,visited_ips,15*60)

        return super(ArticleView,self).get(request,*args,**kwargs)


    def get_context_data(self,**kwargs):
        #评论
        en_title = self.kwargs.get('slug','')
        kwargs['comment_list'] = self.queryset.get(en_title=en_title).comment_set.all()
        return super(ArticleView,self).get_context_data(**kwargs)


class AllView(BaseMixin,ListView):
    template_name = 'all.html'
    context_object_name = 'article_list'

    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all()
        kwargs['PAGE_NUM'] = PAGE_NUM
        return super(AllView,self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0).exclude(en_title = 'aboutme')[0:PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        val = self.request.POST.get("val","")
        sort = self.request.POST.get("sort","time")
        start = self.request.POST.get("start",0)
        end = self.request.POST.get("end",PAGE_NUM)

        start = int(start)
        end = int(end)

        if sort == "time":
            sort = "-pub_time"
        elif sort == "recommend":
            sort = "-view_times"
        else:
            sort = "-pub_time"

        if val == "all":
            article_list = Article.objects.filter(status=0).exclude(en_title = 'aboutme').order_by(sort)[start:end+1]
        else:
            try:
                article_list = Category.objects.get(name=val).article_set.filter(status=0).exclude(en_title = 'aboutme').order_by(sort)[start:end+1]
            except Category.DoesNotExist:
                logger.error(u'[AllView]此分类不存在:[%s]' % val)
                raise PermissionDenied

        isend = len(article_list) != (end-start+1)

        article_list = article_list[0:end-start]

        html = ""
        for article in article_list:
            html +=  template.loader.get_template('include/all_post.html').render(template.Context({'post':article}))

        mydict = {"html":html,"isend":isend}
        return HttpResponse(json.dumps(mydict),content_type="application/json")


class SearchView(BaseMixin,ListView):
    template_name = 'search.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_context_data(self,**kwargs):
        kwargs['s'] = self.request.GET.get('s','')
        return super(SearchView,self).get_context_data(**kwargs)

    def get_queryset(self):
        #获取搜索的关键字
        s = self.request.GET.get('s','')
        #在文章的标题,summary和tags中搜索关键字
        article_list = Article.objects.only('title','summary','tags')\
                .filter(Q(title__icontains=s)|Q(summary__icontains=s)|Q(tags__icontains=s)\
                ,status=0);
        return article_list


class TagView(BaseMixin,ListView):
    template_name = 'tag.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag','')
        article_list = Article.objects.only('tags').filter(tags__icontains=tag,status=0);

        return article_list


class CategoryView(BaseMixin,ListView):
    template_name = 'category.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        category = self.kwargs.get('category','')
        try:
            article_list = Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            logger.error(u'[CategoryView]此分类不存在:[%s]' % category)
            raise Http404

        return article_list


class UserView(BaseMixin,TemplateView):
    template_name = 'user.html'

    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated():
            logger.error(u'[UserView]用户未登陆')
            return render(request, 'login.html')

        slug = self.kwargs.get('slug')

        if slug == 'changetx':
            self.template_name = 'user_changetx.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'changepassword':
            self.template_name = 'user_changepassword.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'changeinfo':
            self.template_name = 'user_changeinfo.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'message':
            self.template_name = 'user_message.html'
            return super(UserView,self).get(request,*args,**kwargs)

        logger.error(u'[UserView]不存在此接口')
        raise Http404



class ColumnView(BaseMixin,ListView):
    queryset = Column.objects.all()
    template_name = 'column.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM

    def get_context_data(self,**kwargs):
        column = self.kwargs.get('column','')
        try:
            kwargs['column'] = Column.objects.get(name=column)
        except Column.DoesNotExist:
            logger.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return super(ColumnView,self).get_context_data(**kwargs)

    def get_queryset(self):
        column = self.kwargs.get('column','')
        try:
            article_list = Column.objects.get(name=column).article.all()
        except Column.DoesNotExist:
            logger.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return article_list


class NewsView(BaseMixin,TemplateView):
    template_name = 'news.html'
    
    def get_context_data(self, **kwargs):
        timeblocks = []

        #获取开始和终止的日期
        start_day = self.request.GET.get("start","0")
        end_day =  self.request.GET.get("end","6")
        start_day = int(start_day)
        end_day = int(end_day)

        start_date = datetime.datetime.now();

        #获取url中时间断的资讯
        for x in range(start_day,end_day+1):
            date = start_date - datetime.timedelta(x)
            news_list = News.objects.filter(pub_time__year=date.year,
                                        pub_time__month=date.month,
                                        pub_time__day = date.day)
                   
            if news_list:
                timeblocks.append(news_list)
        
        kwargs['timeblocks'] = timeblocks
        kwargs['active'] = start_day/7  #li中那个显示active

        return super(NewsView,self).get_context_data(**kwargs)

class NewsDetailView(DetailView):

    template_name = 'news_detail.html'
    model = News
    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        return context

class MessageView(BaseMixin,TemplateView):
    template_name = 'message.html'

    def get_context_data(self,**kwargs):
        kwargs['message_list'] = Message.objects.filter(status=0)
        return super(MessageView,self).get_context_data(**kwargs)


class MessageControl(View):
    def post(self, request, *args, **kwargs):
        #获取当前用户
        user = self.request.user
        #获取留言
        message = self.request.POST.get("message","")
        #获取类型
        status = self.request.POST.get("status","")
        #判断当前用户是否是活动的用户
        if not user.is_authenticated():
            logger.error(u'[CommentControl]当前用户非活动用户:[%s]' % user.username)
            return HttpResponse(u"请登陆！",status=403)
        if not message:
            logger.error(u'[CommentControl]当前用户输入空留言:[%s]' % user.username)
            return HttpResponse(u"请输入留言内容！",status=403)

        #保存评论
        message = Message.objects.create(
                user=user,
                message = message,
				status = status,
                )

        try:
            img = message.user.img
        except Exception as e:
            img = "http://jiange.qiniudn.com/image/tx/tx-default.jpg"

        #返回当前评论
        html = "<li>\
                    <div class=\"jiange-comment-tx\">\
                        <img src="+img+" width=\"40\"></img>\
                    </div>\
                    <div class=\"jiange-comment-content\">\
                        <a><h1>"+message.user.username+"</h1></a>"\
                        +u"<p>"+message.message+"</p>"+\
                        "<p>"+message.create_time.strftime("%Y-%m-%d %H:%I:%S")+"</p>\
                    </div>\
                </li>"
        if status=='0':
            return HttpResponse(html)
        else:
            return HttpResponse("")

class RSSFeed(Feed) :
    title = "Jiange Blog"
    link = "feeds/"
    description = "MY LIFE'S GETTING BETTER!"
    def items(self):
        return Article.objects.order_by('-create_time')
    def item_title(self, item):
        return item.title
    def item_pubdate(self, item):
        return item.create_time
    def item_description(self, item):
        return item.summary
    def item_link(self, item):
        return ""
