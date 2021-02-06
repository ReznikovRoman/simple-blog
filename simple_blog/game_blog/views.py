from django.views import generic
from django.shortcuts import render
from django.conf import settings

import os
import random
import boto3

from posts import models as post_models


class AboutPage(generic.TemplateView):
    """About this project - view"""

    template_name = 'about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context['active_about_page'] = 'active'
        return context


class HomePage(generic.TemplateView):
    """Homepage - view"""

    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['active_homepage'] = 'active'
        context['latest_posts'] = self.get_latest_posts()
        context['background_images'] = self.get_random_background_images()
        return context

    def get_latest_posts(self):
        # TODO: reformat, move to separate file
        query = post_models.Post.objects.order_by('-published_date')[:3]
        return query

    def get_random_background_images(self):
        # TODO: reformat, move to separate file
        if settings.USE_S3:
            prefix = "static/game_blog/images/background_images/"
            s3 = boto3.resource('s3',
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            bucket = s3.Bucket(name=settings.AWS_STORAGE_BUCKET_NAME)
            all_images = bucket.objects.filter(Prefix=prefix)
            images_urls = [img.key.split('static/')[1] for img in all_images]
        else:
            prefix = 'game_blog/images/background_images/'
            all_images = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], prefix))
            images_urls = [prefix + img for img in all_images]

        images_count = 3
        random_images = random.sample(images_urls, images_count)
        return random_images

############################################################################################################


def error_404_view(request, *args, **kwargs):
    """Handle 404 error - view"""
    response = render(request, '404_page.html')
    response.status_code = 404
    return response


def error_500_view(request, *args, **kwargs):
    """Handle 500 error - view"""
    response = render(request, '500_page.html')
    response.status_code = 500
    return response


def error_403_view(request, *args, **kwargs):
    """Handle 403 error - view"""
    response = render(request, '403_page.html')
    response.status_code = 403
    return response


def error_400_view(request, *args, **kwargs):
    """Handle 400 error - view"""
    response = render(request, '400_page.html')
    response.status_code = 400
    return response






