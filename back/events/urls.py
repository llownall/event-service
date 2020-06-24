from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('api/events/', views.EventList.as_view()),
    path('api/events/<int:pk>/', views.EventInfo.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('', views.index),
]
