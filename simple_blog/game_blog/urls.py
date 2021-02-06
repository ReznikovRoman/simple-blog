from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500

from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static

from . import views as project_views


urlpatterns = [
    path('', project_views.HomePage.as_view(), name='homepage'),
    path('about/', project_views.AboutPage.as_view(), name='about'),

    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('posts/', include('posts.urls', namespace='posts')),

    path('ckeditor', include('ckeditor_uploader.urls'))

]

if settings.USE_S3:
    pass
else:
    urlpatterns += (
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

handler404 = 'game_blog.views.error_404_view'
handler500 = 'game_blog.views.error_500_view'
handler403 = 'game_blog.views.error_403_view'
handler400 = 'game_blog.views.error_400_view'


