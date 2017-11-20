from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration', views.register),
    url(r'^login', views.login),
    url(r'^books$', views.success),
    url(r'^books/(?P<bookid>\d+)$', views.book),
    url(r'^books/new',views.newbook),
    url(r'review/new/(?P<bookid>\d+)$', views.addreview),
    url(r'reviews/(?P<bookid>\d+)/destroy/(?P<reviewid>\d+)$', views.deletereview),
    url(r'^books/add',views.add),
    url(r'^users/(?P<userid>\d+)$', views.user),
    url(r'^logout',views.logout)
]