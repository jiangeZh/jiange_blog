#coding:utf-8
from django.contrib import admin
from blog.models import Article,Category,Carousel,Nav,Column,News,Link,Message
from forms import ArticleForm

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('status','create_time')
    list_display = ('name','parent','rank','status')
    fields = ('name','parent','rank','status')


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	search_fields = ('title','summary')
	list_filter = ('status','category','is_top','create_time','update_time','is_top')
	list_display = ('title','category','author','status','is_top','update_time')
	fieldsets = (
        (u'基本信息', {
            'fields': ('title','en_title','img','category','tags','author','is_top','rank','status')
            }),
        (u'内容', {
            'fields': ('content',) 
            }),
        (u'摘要', {
            'fields': ('summary',) 
            }),
        (u'时间', {
            'fields': ('pub_time',) 
            }),
    )


class NewsAdmin(admin.ModelAdmin):
    search_fields = ('title','summary')
    list_filter = ('news_from','create_time')
    list_display = ('title','news_from','url','create_time')
    fields = ('title','news_from','url','summary','pub_time')


class NavAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','url','status','create_time')
    list_filter = ('status','create_time')
    fields = ('name','url','status')


class ColumnAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','status','create_time')
    list_filter = ('status','create_time')
    fields = ('name','status','article','summary')
    filter_horizontal = ('article',)


class CarouselAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title','article','img','create_time')
    list_filter = ('create_time',)
    fields = ('title','article','img','summary')

class MessageAdmin(admin.ModelAdmin):
    search_fields = ('user__username','message')
    list_filter = ('create_time',)
    list_display = ('user','message','create_time','status')
    fields = ('user','message')

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','url')
    list_filter = ('name',)
    fields = ('name','url')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Nav,NavAdmin)
admin.site.register(Column,ColumnAdmin)
admin.site.register(Carousel,CarouselAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Link,LinkAdmin)
