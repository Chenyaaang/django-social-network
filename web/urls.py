"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import glumblr.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', glumblr.views.index),
    path('', include('glumblr.urls')),
    # path('login/', glumblr.views.login, name='login'),
    # path('register/', glumblr.views.register, name='register'),
    # path('confirm/<str:username>/<str:token>', glumblr.views.confirm_registration, name='confirm'),
    # path('profile/<str:username>', glumblr.views.profile, name='profile'),
    # path('global_stream/', glumblr.views.global_stream, name='global_stream'),
    # path('logout/', glumblr.views.logout, name='logout'),
    # path('edit/', glumblr.views.edit, name='edit'),
    # path('delete/<int:id>', glumblr.views.delete, name='delete'),
    # path('follow/<str:username>', glumblr.views.follow, name='follow'),
    # path('unfollow/<str:username>', glumblr.views.unfollow, name='unfollow'),
    # path('follow_stream/<str:username>', glumblr.views.follow_stream, name='follow_stream'),
    # path('reset/', glumblr.views.reset, name='reset'),
    # path('reset/<str:username>/<str:token>', glumblr.views.reset_password_valid, name='reset_password_valid'),
    # path('change_password/', glumblr.views.change_password, name='change_password'),
]
