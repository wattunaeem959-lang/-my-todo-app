from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('toggle/<int:id>/', views.toggle_task, name='toggle'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]