# Generated by Django 3.1 on 2020-12-04 16:11

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='images/post_headers/')),
                ('title', models.CharField(max_length=255)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content_html', models.TextField(editable=False)),
            ],
            options={
                'ordering': ['published_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
        ),
    ]
