from django.contrib import admin
from django.urls import path, re_path
from .views import WelcomePage, News, MainPage, CreateNews

urlpatterns = [
    path('', WelcomePage.as_view()),
    re_path('news/(?P<news_id>\d+)', News.as_view()),
    path('news/', MainPage.as_view()),
    path('news/create/', CreateNews.as_view()),
]
