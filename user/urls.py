from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world, name='hello'),
    path('get_all', views.get_users, name='get_users'),
    path('get/<int:pk>', views.get_user, name='get_user'),
    path('create', views.create_user, name='create_user'),
    path('update/<int:pk>', views.update_user, name='update_user'),
    path('delete/<int:pk>', views.delete_user, name='delete_user'),
]