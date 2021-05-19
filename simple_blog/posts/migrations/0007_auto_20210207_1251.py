# Generated by Django 3.1 on 2021-02-07 09:51

import ckeditor_uploader.fields
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20201207_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content_html',
        ),
        migrations.AlterField(
            model_name='comment',
            name='posted_date',
            field=models.DateTimeField(auto_now=True, verbose_name='posted date'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='text of the comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='main content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(auto_now=True, verbose_name='created date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, default=posts.models.get_default_header_image, null=True, upload_to='images/post_headers/', verbose_name='header image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='published date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
    ]