from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django import template

from ckeditor_uploader.fields import RichTextUploadingField

from accounts import models as account_models


register = template.Library()


def get_default_header_image():
    return 'images/post_headers/default_post_headers/default_post_header.jpg'


class Post(models.Model):
    """Single post on the website"""

    slug = models.SlugField(verbose_name="slug", allow_unicode=True, unique=True)
    created_date = models.DateTimeField(verbose_name="created date", auto_now=True)
    published_date = models.DateTimeField(verbose_name="published date", blank=True, null=True)
    header_image = models.ImageField(verbose_name="header image", null=True, blank=True,
                                     upload_to='images/post_headers/', default=get_default_header_image)
    title = models.CharField(verbose_name="title", max_length=255)
    content = RichTextUploadingField(verbose_name="main content", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:draft', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Title: {self.title}"

    class Meta:
        ordering = ['published_date']


class Comment(models.Model):
    """Comment related to a Post"""
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, )
    author = models.ForeignKey(account_models.CustomUser, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='text of the comment')
    posted_date = models.DateTimeField(verbose_name="posted date", auto_now=True)

    def __str__(self):
        return f"Author: {self.author}, Text: {self.text}"

    class Meta:
        ordering = ["-posted_date"]












