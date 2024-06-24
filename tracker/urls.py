from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('add/', views.add_entry, name='add_entry'),
    path('summary/', views.summary, name='summary'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
