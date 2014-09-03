from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^shops/', include('shops.urls', namespace = "shops")),
    # url(r'^products/', include('products.urls', namespace = "products")),
    url(r'^users/', include('users.urls', namespace = "users")),
    url(r'^core/', include('core.urls', namespace = "core")),
    url(r'^facebook/', include('django_facebook.urls')),
    # url(r'^home/notifications/', include(notifications.urls)),
)