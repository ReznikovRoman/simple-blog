from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CommentForm, PostForm
from .models import Post, Comment
from .services import (publish_post, save_comment_from_form, get_published_posts, get_search_results,
                       get_drafts, get_all_posts, get_comment_by_pk, get_post_by_slug)


class PostList(generic.ListView):
    """List posts (paginate by 6)."""
    model = Post
    paginate_by = 6

    def get_queryset(self):
        return get_published_posts()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['active_blog_page'] = 'active'
        return context


class PostDetail(generic.DetailView):
    """Single post's details."""
    model = Post
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_queryset(self):
        return get_published_posts()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        form = CommentForm()
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = CommentForm(data=self.request.POST)
            if form.is_valid():
                save_comment_from_form(form, self.kwargs.get('slug'), self.request.user)
        else:
            return redirect('accounts:login')
        return redirect('posts:single', slug=self.kwargs.get('slug'))


class CreatePost(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 generic.CreateView):
    """Post's creation."""
    model = Post
    permission_required = 'posts.add_post'
    redirect_field_name = 'posts:draft'
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save()
        return super(CreatePost, self).form_valid(form)


class UpdatePost(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 generic.UpdateView):
    """Edit post."""
    model = Post
    permission_required = 'posts.change_post'
    redirect_field_name = 'posts:single'
    form_class = PostForm

    def get_success_url(self):
        return reverse('posts:single', kwargs={'slug': self.kwargs.get('slug')})


class SearchPostView(generic.ListView):
    """Search results (list of posts)."""
    model = Post
    template_name = 'posts/post_search_results.html'

    def get_queryset(self):
        return get_search_results(self.request.GET.get('q'))


class DeletePost(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 generic.DeleteView):
    """Delete Post."""
    model = Post
    permission_required = 'posts.delete_post'
    redirect_field_name = 'posts:single'
    form_class = PostForm
    success_url = reverse_lazy('posts:all')


class DraftListView(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    generic.ListView):
    """List drafts."""
    model = Post
    permission_required = 'posts.add_post'
    redirect_field_name = 'posts:single'
    context_object_name = 'draft_list'
    template_name = 'posts/draft_list.html'

    def get_queryset(self):
        return get_drafts()


class DeletePostList(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     generic.ListView):
    """List posts that can be deleted."""
    model = Post
    paginate_by = 6
    permission_required = 'posts.delete_post'
    template_name = 'posts/post_delete_list.html'

    def get_queryset(self):
        return get_all_posts()


class DraftDetail(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  generic.DetailView):
    """Single draft detail."""
    model = Post
    permission_required = 'posts.add_post'
    template_name = 'posts/draft_detail.html'
    context_object_name = 'draft'

    def get_queryset(self):
        return get_drafts()


class UpdateDraft(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  generic.UpdateView):
    """Edit draft."""
    model = Post
    permission_required = 'posts.change_post'
    template_name = 'posts/post_form.html'
    redirect_field_name = 'posts:single'
    form_class = PostForm

    def get_success_url(self):
        return reverse('posts:draft', kwargs={'slug': self.kwargs.get('slug')})


class PostPublish(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  generic.DetailView):
    """Publish post."""
    permission_required = 'posts.add_post'
    model = Post
    template_name = 'posts/draft_publish.html'
    context_object_name = 'draft'

    def get_queryset(self):
        return get_drafts()

    def post(self, request, *args, **kwargs):
        try:
            post = get_post_by_slug(self.kwargs.get('slug'))
        except Post.DoesNotExist:
            messages.warning(self.request,
                             "You cannot publish this post, because it does not exist")
        else:
            publish_post(post)
            messages.success(self.request,
                             "You have successfully published this post!")
            return redirect('/posts/')


class DeleteComment(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    generic.DeleteView):
    """Delete comment."""
    model = Comment
    permission_required = 'posts.delete_comment'
    template_name = 'posts/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_object(self, queryset=None):
        return get_comment_by_pk(self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('posts:single',
                            kwargs={'slug': get_comment_by_pk(self.kwargs.get('pk')).post.slug})
