import os
import random
from typing import List

import boto3

from django.conf import settings
from django.db.models import QuerySet

from posts.models import Post


def get_latest_posts() -> QuerySet[Post]:
    """
    Returns 3 latest published posts (sorted by a published date).

    Returns:
        QuerySet[Post]: QuerySet of 3 latest posts
    """
    return Post.objects.order_by('-published_date')[:3]


def get_random_background_images() -> List[str]:
    """
    Returns a list of images (urls) depending on a storage backend.

    Returns:
        List[str]: list of images' urls
    """
    if settings.USE_S3:
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.Bucket(name=settings.AWS_STORAGE_BUCKET_NAME)

        prefix = "static/game_blog/images/background_images/"
        all_images = bucket.objects.filter(Prefix=prefix)
        images_urls = [img.key.split('static/')[1] for img in all_images]
    else:
        prefix = 'game_blog/images/background_images/'
        all_images = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], prefix))
        images_urls = [prefix + img for img in all_images]

    images_count = 3
    random_images = random.sample(images_urls, images_count)

    return random_images















