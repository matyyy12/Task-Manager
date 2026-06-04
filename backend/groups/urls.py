from django.urls import path
from groups import views

urlpatterns = [
    path('', views.GroupListView.as_view(), name='group-list'),
    path('<int:pk>', views.GroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/invitation', views.InvitationView.as_view(), name='invitation-create'),
    path('invitation/<str:token>', views.InvitationView.as_view(), name='invitation-accept'),
]