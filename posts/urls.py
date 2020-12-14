
from django.urls import path, include

from . import views

#################################################################################################################


app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('drafts/', views.DraftListView.as_view(), name='drafts'),
    path('drafts/<slug>/', views.DraftDetail.as_view(), name='draft'),
    path('drafts/<slug>/publish/', views.PostPublish.as_view(), name='publish'),
    path('drafts/<slug>/edit/', views.UpdateDraft.as_view(), name='edit_draft'),

    path('search/', views.SearchPostView.as_view(), name='search_post'),

    path('new/', views.CreatePost.as_view(), name='create'),

    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='comment_remove'),

    path('delete/', views.DeletePostList.as_view(), name='delete_list'),

    path('<slug>/', views.PostDetail.as_view(), name='single'),
    path('<slug>/delete/', views.DeletePost.as_view(), name='delete'),
    path('<slug>/edit/', views.UpdatePost.as_view(), name='edit'),
]
















