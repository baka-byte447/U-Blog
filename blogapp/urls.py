from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:id>/', views.post_details, name='post_details'),
]