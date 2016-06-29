from django.conf.urls import patterns, url

from bank import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),

                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'bank/login.html'},
                           name='login'),


                       url(r'^my_trans/$', views.show_my_trans, name='my_trans'),
                       url(r'^all_acc$', views.AccsView.as_view(), name='all_acc'),

                       url(r'^add_trans/single/$', views.single_trans, name='add_single'),
                       url(r'^add_trans/multi/', views.multi_trans, name='multi_trans'),
                       url(r'^add_trans/sem/', views.multi_trans, name='add_sem'),

                       )

