from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect

#           Extra Imports for the Login and Logout Capabilities
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from django.db.models import Q

from braces.views import SelectRelatedMixin

from . import forms
from . import models

##################################################################################################################


class PostList(generic.ListView):
    model = models.Post
    paginate_by = 6

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['active_blog_page'] = 'active'
        return context


class PostDetail(generic.DetailView):
    model = models.Post
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = get_object_or_404(models.Post, slug=self.kwargs.get('slug'))

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
    permission_required = 'posts.add_post'

    redirect_field_name = 'posts:draft'

    form_class = forms.PostForm

    model = models.Post

    # def get(self, request, *args, **kwargs):
    #     print("Permissions: ")
    #     for perm in list(Permission.objects.filter(group__user=self.request.user)):
    #         print(perm)
    #     print("Has perm: ", self.request.user.has_perm('posts.add_post'))
    
    def form_valid(self, form):
        self.object = form.save()
        return super(CreatePost, self).form_valid(form)


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'posts.change_post'

    redirect_field_name = 'posts:single'

    form_class = forms.PostForm

    model = models.Post

    def get_success_url(self):
        return reverse('posts:single', kwargs={'slug': self.kwargs.get('slug')})


class SearchPostView(generic.ListView):
    model = models.Post
    template_name = 'posts/post_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = models.Post.objects.filter(
            Q(title__icontains=query),
            published_date__isnull=False
        )
        return object_list


class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'posts.delete_post'

    redirect_field_name = 'posts:single'

    form_class = forms.PostForm

    model = models.Post

    success_url = reverse_lazy('posts:all')


class DraftListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'posts.add_post'

    redirect_field_name = 'posts:single'

    model = models.Post

    context_object_name = 'draft_list'

    template_name = 'posts/draft_list.html'

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('-created_date')


class DeletePostList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'posts.delete_post'

    model = models.Post
    template_name = 'posts/post_delete_list.html'

    def get_queryset(self):
        return models.Post.objects.order_by('-published_date')


class DraftDetail(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = 'posts.add_post'

    model = models.Post
    template_name = 'posts/draft_detail.html'
    context_object_name = 'draft'

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True)


class UpdateDraft(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'posts.change_post'
    model = models.Post
    template_name = 'posts/post_form.html'
    redirect_field_name = 'posts:single'
    form_class = forms.PostForm

    def get_success_url(self):
        return reverse('posts:draft', kwargs={'slug': self.kwargs.get('slug')})


class PostPublish(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
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
            post.publish()
            messages.success(self.request,
                             "You have successfully published this post!")
            return redirect('/posts/')
        # return super(PostPublish, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True)


class DeleteComment(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):

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



















