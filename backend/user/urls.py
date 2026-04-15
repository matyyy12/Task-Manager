from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('tasks/<int:pk>', views.UserTaskView.as_view(), name='user-task'),

]