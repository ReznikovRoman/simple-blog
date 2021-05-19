from django.views import generic
from django.shortcuts import render

from .services import get_latest_posts, get_random_background_images


class AboutPage(generic.TemplateView):
    """About this project - view."""
    template_name = 'about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context['active_about_page'] = 'active'
        return context


class HomePage(generic.TemplateView):
    """Homepage - view."""
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        context['active_homepage'] = 'active'
        context['latest_posts'] = get_latest_posts()
        context['background_images'] = get_random_background_images()

        return context


def error_404_view(request, *args, **kwargs):
    """Handle 404 error - view."""
    response = render(request, '404_page.html')
    response.status_code = 404
    return response


def error_500_view(request, *args, **kwargs):
    """Handle 500 error - view."""
    response = render(request, '500_page.html')
    response.status_code = 500
    return response


def error_403_view(request, *args, **kwargs):
    """Handle 403 error - view."""
    response = render(request, '403_page.html')
    response.status_code = 403
    return response


def error_400_view(request, *args, **kwargs):
    """Handle 400 error - view."""
    response = render(request, '400_page.html')
    response.status_code = 400
    return response
