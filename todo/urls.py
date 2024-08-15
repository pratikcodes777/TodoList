from django.urls import path, include
from . import views


urlpatterns = [
    path('' , views.home , name='home'),
    path('register/' , views.register , name='register'),
    path('login/' , views.login , name='login'),
    path('delete/<str:name>' , views.delete , name='delete'),
    path('update/<str:name>' , views.update , name='update'),
    path('unupdate/<str:name>' , views.unupdate , name='unupdate'),
    path('toggle_status/<str:name>' , views.toggle_status , name='toggle'),
    path('update_todo/<str:name>' , views.update_todo , name='update-todo'),
    path('logout/' , views.logout , name='logout'),
]