from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.conf import settings

import os
import random
import boto3

from posts import models as post_models


############################################################################################################


class TestPage(generic.TemplateView):
    template_name = 'test.html'


class AboutPage(generic.TemplateView):
    template_name = 'about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context['active_about_page'] = 'active'
        return context


class HomePage(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['active_homepage'] = 'active'
        context['latest_posts'] = self.get_latest_posts()
        context['background_images'] = self.get_random_background_images()
        return context

    def get_latest_posts(self):
        query = post_models.Post.objects.order_by('-published_date')[:3]
        return query

    def get_random_background_images(self):
        prefix = "static/game_blog/images/background_images/"
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        bucket = s3.Bucket(name=settings.AWS_STORAGE_BUCKET_NAME)
        all_images = bucket.objects.filter(Prefix=prefix)
        images_urls = [img.key.split('static/')[1] for img in all_images]

        # all_images = os.listdir(os.path.join(settings.STATIC_URL, "game_blog/images/background_images/"))

        images_count = 3
        random_images = random.sample(images_urls, images_count)
        return random_images

############################################################################################################


def error_404_view(request, *args, **kwargs):
    response = render(request, '404_page.html')
    response.status_code = 404
    return response


def error_500_view(request, *args, **kwargs):
    response = render(request, '500_page.html')
    response.status_code = 500
    return response


def error_403_view(request, *args, **kwargs):
    response = render(request, '403_page.html')
    response.status_code = 403
    return response


def error_400_view(request, *args, **kwargs):
    response = render(request, '400_page.html')
    response.status_code = 400
    return response






