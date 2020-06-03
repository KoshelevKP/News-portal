# Create your views here.

from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
from os.path import normpath
from random import randint
import json
import datetime


class WelcomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, normpath('news/WelcomePage.html'), {})


class News(View):

    def get(self, request, news_id, *args, **kwargs):

        with open(settings.NEWS_FILE, 'r') as news_file:
            news_json = json.load(news_file)

            news_context = None
            for news in news_json:
                if news['link'] == int(news_id):
                    news_context = news

        if news_context:
            return render(request, normpath('news/News.html'), {'news': news_context})
        else:
            raise Http404


class MainPage(View):

    def get(self, request, *args, **kwargs):

        with open(settings.NEWS_FILE, 'r') as news_file:
            news_json = json.load(news_file)

        if request.GET.get('news_tags') is not None:
            tags = request.GET.get('news_tags')
            news_json = [news for news in news_json if tags.lower() in news['title'].lower()]

        for news in news_json:
            news['created'] = news['created'][:10]

        return render(request, normpath('news/MainPage.html'), context={'news': news_json})


class CreateNews(View):

    def get(self, request, *args, **kwargs):
        return render(request, normpath('news/CreateNews.html'), {})

    def post(self, request, *args, **kwargs):

        with open(settings.NEWS_FILE, 'r') as news_file:
            news_json = json.load(news_file)

        news_text = request.POST.get('text')
        news_title = request.POST.get('title')
        news_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        news_link = randint(10, 10000000)

        link_list = [news['link'] for news in news_json]
        while news_link in link_list:
            news_link = randint(10, 10000000)

        news_json.append({
            "created": news_created,
            "text": news_text,
            "title": news_title,
            "link": news_link
        })

        with open(settings.NEWS_FILE, 'w') as news_file:
            json.dump(news_json, news_file)

        return redirect('/news/')
