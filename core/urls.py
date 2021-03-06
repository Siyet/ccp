from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from checkout import views as checkout_views

urlpatterns = i18n_patterns(
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^backend/', include('backend.urls')),
    url(r'^kassa/order-check/?$', checkout_views.CheckOrderView.as_view(), name='kassa_check_order'),
    url(r'^kassa/', include('yandex_kassa.urls')),
    url(r'^(?P<pk>[0-9]+)/$', 'processing.views.shirt')
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
