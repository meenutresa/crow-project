from django.conf.urls import patterns, include, url
from pro.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pro.views.home', name='home'),
    # url(r'^pro/', include('pro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tags/(?P<theTag>[a-zA-Z0-9]+)$','crow.views.viewTag'),
    url(r'^shouts/(?P<reqId>\w+)$','crow.views.viewSingleItem'),
    url(r'^users/(?P<userId>[a-zA-Z0-9@/./+/-/_ ]+)/$','crow.views.viewProfile'),
    url(r'^myfeed/','crow.views.viewMyFeed'),
    url(r'^follow/','crow.views.viewFollowBtn'),                                       
    url(r'^app-login2/','crow.views.viewLoginAddonVideo'),                                          
 #   url(r'^app-login/',auth_views.login,{'template_name':'site/login.html'},name='auth_login'),
    url(r'^app-logout/','crow.views.viewLogoutAddon'),
    url(r'^login-error/','crow.views.viewLoginError'),
    url(r'^imagesubmit/','crow.views.viewSubmitImage'),
    url(r'^videosubmit/','crow.views.viewSubmitVideo'),
    #url(r'^profileedit/(?P<userId>[a-zA-Z0-9@/./+/-/_ ]+)','crow.views.viewEdit'),  
    url(r'^edit/(?P<username>[a-zA-Z0-9@/./+/-/_ ]+)','crow.views.edit_profile'),                     
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),                       
url(r'^$', 'crow.views.viewTrending'),
    url(r'^accounts/', include('registration.urls')),

    url(r'^$', 'pro.views.home'),

    url(r'^facebook/login$', 'facebook.views.login'),
    url(r'^facebook/authentication_callback$', 'facebook.views.authentication_callback'),
    url(r'^logout$', 'django.contrib.auth.views.logout'),


)
