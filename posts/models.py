from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

import misaka
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth import get_user_model

from accounts import models as account_models

from django import template
register = template.Library()

##################################################################################################################


def get_default_header_image():
    return '/images/post_headers/default_post_headers/default_post_header.jpg'


class Post(models.Model):
    slug = models.SlugField(allow_unicode=True, unique=True)

    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    header_image = models.ImageField(null=True, blank=True, upload_to='images/post_headers/',
                                     default=get_default_header_image)
    title = models.CharField(max_length=255)
    # content = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    content_html = models.TextField(editable=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.content_html = misaka.html(self.content_html)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:draft', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Title: {self.title}"

    class Meta:
        ordering = ['published_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, )
    author = models.ForeignKey(account_models.CustomUser, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField()
    posted_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Author: {self.author}, Text: {self.text}"

    class Meta:
        ordering = ["-posted_date"]












