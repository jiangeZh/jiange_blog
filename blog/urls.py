from django.conf.urls import url
from blog.views import IndexView,ArticleView,AllView,SearchView,ColumnView,UserView,NewsView,NewsDetailView,TagView,CategoryView,MessageView,MessageControl,RSSFeed
from django.views.generic import TemplateView,DetailView
from blog.models import News

urlpatterns = [
        url(r'^$',IndexView.as_view()),
        url(r'^article/(?P<slug>\w+).html$',ArticleView.as_view()),
        url(r'^all/$',AllView.as_view()),
        url(r'^search/$',SearchView.as_view()),
        url(r'^login/$',TemplateView.as_view(template_name="login.html")),
        url(r'^register/$',TemplateView.as_view(template_name="register.html")),
        url(r'^forgetpassword/$',TemplateView.as_view(template_name="forgetpassword.html")),
        url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',TemplateView.as_view(template_name="resetpassword.html")),
        url(r'^column/(?P<column>\w+)$',ColumnView.as_view()),
        url(r'^user/(?P<slug>\w+)$',UserView.as_view()),
        url(r'^news/$',NewsView.as_view()),
		url(r'^message/$',MessageView.as_view()),
		url(r'^message/send$',MessageControl.as_view()),
        url(r'^news/(?P<pk>\w+)$',NewsDetailView.as_view()),
        url(r'^tag/(?P<tag>\w+)/$',TagView.as_view()),
        url(r'^category/(?P<category>\w+)/$',CategoryView.as_view()),
        url(r'^feed/$', RSSFeed(), name = "RSS"),
]
