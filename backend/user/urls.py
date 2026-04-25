from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserListView.as_view(), name='user-list'),
    path('', views.UserDetailView.as_view(), name='user-detail'),
    path('tasks', views.UserTaskView.as_view(), name='user-task'),

]