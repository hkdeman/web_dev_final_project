from django.conf.urls import url
from unevu import views

#Links urls to views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about-us/$', views.about, name = 'about'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^choose-uni/$', views.choose_uni, name = 'choose_uni'),
    url(r'^uni-details$',views.uni_details,name='uni-details'),
    url(r'^school-details$',views.school_details,name='school-details'),    
    url(r'^review-course/(?P<course_id>\d+)$',views.review_course,name='review-course'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^university/(?P<uni_id>\d+)$',views.university,name='university-page'),
    url(r'^add-review',views.add_review,name='add-review'),
    url(r'^review-uni/(?P<uni_id>\d+)$',views.review_uni,name='review-uni'),
    url(r'^review-teacher/(?P<teacher_id>\d+)$',views.review_teacher,name='review-teacher'),   
    url(r'^like',views.like,name='like'),    
    url(r'^preferences',views.preferences,name='preferences'),    
    url(r'^update-review',views.update_review,name='update-review'),    
] 
