# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import login_view, register_user, CustomLogoutView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('home/', login_view, name="home"),
    path('register/', register_user, name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout")
]

"""if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
