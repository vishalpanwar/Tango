"""tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tango import settings
from django.conf.urls.static import static
from rango import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/rango/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rango/$',views.rango_index,name = "rango_index"),
    url(r'^rango/about/$',views.rango_about,name = "rango_about"),
    url(r'^rango/add_category/$',views.add_category,name = "rango_add_category"),
    url(r'^rango/category/add_page/(?P<slug>[\w\-]+)/$',views.add_page,name = "rango_add_page"),
    url(r'^rango/category/(?P<slug>[\w\-]+)/$',views.rango_categories,name = "rango_category"),
    url(r'^rango/register/$', views.register,name = 'rango_register'),
    url(r'^rango/login/$',views.user_login,name = 'rango_user_login'),
    url(r'^rango/logout/$',views.user_logout,name = 'rango_user_logout'),
    url(r'^rango/restricted/$',views.restricted,name = 'rango_restricted'),
    url(r'^rango/profile/$',views.build_profile,name = 'rango_userprofile'),
    url(r'^rango/view_profile/$',views.view_profile,name = 'rango_view_userprofile'),
    url(r'^rango/goto/$',views.track_url,name = 'rango_goto'),
    url(r'^rango/like_category/$', views.like_category,name = 'rango_like_category'),
    url(r'^rango/suggest_category/$',views.suggest_category,name = 'rango_suggest'),

    url(r'^accounts/', include('registration.backends.default.urls')),


]

if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)