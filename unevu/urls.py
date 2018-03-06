from django.conf.urls import url
from unevu import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about-us/$', views.about, name = 'about'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^choose-uni/$', views.choose_uni, name = 'choose_uni'),
    url(r'^home-details$',views.home_details,name='home-details'),
    url(r'^review-course/(?P<course_id>\d+)$',views.review_course,name='review-course'),
] 
