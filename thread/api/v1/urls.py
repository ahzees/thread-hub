from django.urls import path

from thread.api.v1.views import ThreadApiView, ViewThreadApiView, AddMembersApiView, ViewMessagesThreadApiView, ViewAllThreadApiView, AddMessageThreadApiView, DeleteThreadApiView


urlpatterns = [
    path('create/', ThreadApiView.as_view()),
    path('all/', ViewAllThreadApiView.as_view()),
    path('<int:pk>/view/', ViewThreadApiView.as_view()),
    path('<int:pk>/delete/', DeleteThreadApiView.as_view()),
    path('<int:pk>/add_members/', AddMembersApiView.as_view()),
    path('<int:pk>/messages/', ViewMessagesThreadApiView.as_view()),
    path('<int:pk>/message/', AddMessageThreadApiView.as_view())
]