from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Q

from .forms import CommentForm
from .models import Post, Comment
from accounts.models import CustomUser


def get_post_by_slug(post_slug: str) -> Post:
    """
    Returns a Post by a given slug.

    Args:
        post_slug (str): post's slug

    Returns:
        Post: post with a given slug
    """
    return get_object_or_404(Post, slug=post_slug)


def get_comment_by_pk(comment_pk: int) -> Comment:
    """
    Returns a Comment by a given pk.

    Args:
        comment_pk (int): comment's pk

    Returns:
        Comment: comment with a given pk
    """
    return get_object_or_404(Comment, pk=comment_pk)


def publish_post(post: Post) -> None:
    """
    "Publishes" a post - fills in the 'published_date' field.

    Args:
        post (Post): post that should be published

    Returns:
        None
    """
    post.published_date = timezone.now()
    post.save()


def save_comment_from_form(form: CommentForm, post_slug: str, comment_author: CustomUser) -> None:
    """
    Saves a Comment.

    Args:
        form (CommentForm): Comment creation form
        post_slug (str): slug of the post where comment is written
        comment_author (CustomUser): comment's author

    Returns:
        None
    """
    comment = form.save(commit=False)
    comment.post = get_post_by_slug(post_slug)
    comment.author = comment_author
    comment.save()


def get_all_posts() -> QuerySet[Post]:
    """
    Returns a QuerySet of all posts (ordered by a published date - from published posts to drafts).

    Returns:
        QuerySet[Post]: all posts
    """
    return Post.objects.order_by('-published_date')


def get_published_posts() -> QuerySet[Post]:
    """
    Returns a QuerySet of published posts (ordered by a published date - from newest to oldest).

    Returns:
        QuerySet[Post]: published posts
    """
    return Post.objects.filter(published_date__isnull=False).order_by('-published_date')


def get_search_results(title_query: str) -> QuerySet[Post]:
    """
    Returns search results - a QuerySet of posts.

    Args:
        title_query (str): query

    Returns:
        QuerySet[Post]: search results
    """
    return Post.objects.filter(
        Q(title__icontains=title_query),
        published_date__isnull=False
    )


def get_drafts() -> QuerySet[Post]:
    """
    Returns a QuerySet of drafts (ordered by a created date - from newest to oldest).

    Returns:
        QuerySet[Post]: drafts
    """
    return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
