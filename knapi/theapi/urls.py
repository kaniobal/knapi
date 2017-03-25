from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^$', views.KnapsackProblemRequestList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.KnapsackProblemRequestDetail.as_view(), name='knapsackproblemrequest-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
