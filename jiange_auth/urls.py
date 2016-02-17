from django.conf.urls import url
from jiange_auth.views import UserControl


urlpatterns = [
        url(r'^usercontrol/(?P<slug>\w+)$',UserControl.as_view()),
]
