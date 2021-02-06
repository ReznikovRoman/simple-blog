from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

from . import forms
from . import models


class PostList(generic.ListView):
    """List posts (paginate by 6)"""

    model = models.Post
    paginate_by = 6

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['active_blog_page'] = 'active'
        return context


class PostDetail(generic.DetailView):
    """Single post's details"""

    model = models.Post
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = get_object_or_404(models.Post, slug=self.kwargs.get('slug'))

        # TODO: move business logic
        if self.request.method == 'POST':
            form = forms.CommentForm(data=self.request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = self.request.user
                comment.save()
        else:
            form = forms.CommentForm()

        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs.get('slug'))

        # TODO: move business logic
        if self.request.method == 'POST':
            if self.request.user.is_authenticated:
                form = forms.CommentForm(data=self.request.POST)

                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.author = self.request.user
                    comment.save()
            else:
                return redirect('accounts:login')
        else:
            form = forms.CommentForm()
        return redirect('posts:single', slug=self.kwargs.get('slug'))

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=False)


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """Post's creation"""

    permission_required = 'posts.add_post'
    redirect_field_name = 'posts:draft'
    form_class = forms.PostForm
    model = models.Post
    
    def form_valid(self, form):
        self.object = form.save()
        return super(CreatePost, self).form_valid(form)


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """Edit post"""

    permission_required = 'posts.change_post'
    redirect_field_name = 'posts:single'
    form_class = forms.PostForm
    model = models.Post

    def get_success_url(self):
        return reverse('posts:single', kwargs={'slug': self.kwargs.get('slug')})


class SearchPostView(generic.ListView):
    """Search results (list of posts)"""

    model = models.Post
    template_name = 'posts/post_search_results.html'

    def get_queryset(self):
        query_title = self.request.GET.get('q')
        object_list = models.Post.objects.filter(
            Q(title__icontains=query_title),
            published_date__isnull=False
        )
        return object_list


class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    """Delete Post"""

    permission_required = 'posts.delete_post'
    redirect_field_name = 'posts:single'
    form_class = forms.PostForm
    model = models.Post
    success_url = reverse_lazy('posts:all')


class DraftListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """List drafts"""

    permission_required = 'posts.add_post'
    redirect_field_name = 'posts:single'
    model = models.Post
    context_object_name = 'draft_list'
    template_name = 'posts/draft_list.html'

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('-created_date')


class DeletePostList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """List posts that can be deleted"""

    permission_required = 'posts.delete_post'
    model = models.Post
    template_name = 'posts/post_delete_list.html'

    def get_queryset(self):
        return models.Post.objects.order_by('-published_date')


class DraftDetail(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """Single draft detail"""

    permission_required = 'posts.add_post'
    model = models.Post
    template_name = 'posts/draft_detail.html'
    context_object_name = 'draft'

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True)


class UpdateDraft(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """Edit draft"""

    permission_required = 'posts.change_post'
    model = models.Post
    template_name = 'posts/post_form.html'
    redirect_field_name = 'posts:single'
    form_class = forms.PostForm

    def get_success_url(self):
        return reverse('posts:draft', kwargs={'slug': self.kwargs.get('slug')})


class PostPublish(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """Publish post"""

    permission_required = 'posts.add_post'
    model = models.Post
    template_name = 'posts/draft_publish.html'
    context_object_name = 'draft'

    def post(self, request, *args, **kwargs):
        try:
            post = get_object_or_404(models.Post, slug=self.kwargs.get('slug'))
        except models.Post.DoesNotExist:
            messages.warning(self.request,
                             "You cannot publish this post, because it does not exist")
        else:
            post.publish()  # TODO: Move method from model to a separate file
            messages.success(self.request,
                             "You have successfully published this post!")
            return redirect('/posts/')
        # return super(PostPublish, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True)


class DeleteComment(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    """Delete comment"""

    permission_required = 'posts.delete_comment'
    model = models.Comment
    template_name = 'posts/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        post_slug = comment.post.slug
        success_url = reverse_lazy('posts:single', kwargs={'slug': post_slug})
        return success_url

    def get_queryset(self):
        return models.Comment.objects.filter(pk=self.kwargs.get('pk'))



















