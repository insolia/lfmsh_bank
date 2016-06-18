from django.conf.urls import patterns, url

from bank import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),

                       #url(r'^all_acc$', views.show_accounts, name='all_acc'),
                       url(r'^all_acc$', views.AccsView.as_view(), name='all_acc'),
                       url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'bank/login.html'}, name='login'),
                       url(r'^my_acc/$', views.show_my_account, name='my_acc'),
                       url(r'^payment/$', views.pay, name='pay'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

                       )

