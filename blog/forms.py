#coding:utf-8
from django import forms
from pagedown.widgets import AdminPagedownWidget
from blog.models import Article

class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget=AdminPagedownWidget())

	class meta:
		model = Article

