from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views
from Finpy import views

# All these URLs patterns have 'finpy/' prefix
urlpatterns = patterns('',

                        # Home page
                        # Pattern: /finpy
                        url(r'^$', views.index, name='index'),

                        # About page
                        # Pattern: finpy/about.html
                        url(r'^about.html', views.about_page),

                        # Services resume page
                        # Pattern: finpy/service.html
                        url(r'^service.html', views.service_page),

                        # Register page
                        # Pattern: finpy/signup
                        url(r'^signup/$', views.signup, {'template_name': 'accounts/signup.html'}, name='signup'),

                        # New entry page
                        # Pattern: finpy/entry/create
                        url(r'^entry/create/$', views.create_entry, name='create_entry'),

                        # List of entries
                        # Pattern: finpy/entry/list
                        url(r'^entry/list/$', views.list_entry, name='list_entry'),


                        # Delete an entry
                        # Pattern: finpy/entry/delete/id , where id is the number of entry id
                        url(r'^entry/delete/(?P<entry_id>\d+)$', views.delete_entry, name='delete_entry'),

                        # Update an entry
                        # Pattern: finpy/entry/update/id , where id is the number of entry id
                        url(r'^entry/update/(?P<entry_id>\d+)$', views.update_entry, name='update_entry'),
                        
                        # Investment simulation
                        # Pattern: finpy/investment/simulate
                        url(r'^investment/simulate/$', views.simulate_investment, name='simulate_investment'),

                        # Investment simulations list
                        # Pattern: finpy/investment/list
                        url(r'^investment/list/$', views.list_simulations, name='list_simulations'),

                        # User personal data update
                        # Pattern: finpy/profile/update/id , where id is the number of user id
                        url(r'^profile/update/(?P<profile_id>\d+)$', views.update_profile, name='update_profile'),

                        # Login page
                        # Pattern: finpy/login
                        url(r'^login/$', auth_views.login, {'template_name': 'Finpy/pageLogin.html'}, name='login'),

                        # URL to logout the current user 
                        # Pattern: finpy/logout
                        url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

                        # Password change page
                        # Pattern: finpy/password_change
                        url(r'^password_change/$', auth_views.password_change, {'template_name': 'accounts/password_change_form.html'}, name='password_chage'),

                        # Confirmation of password changed page
                        # Pattern: finpy/password_change/done
                        url(r'^password_change/done/$', auth_views.password_change_done, {'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),

                        # Change password by sending an email
                        # Pattern: finpy/password_reset
                        url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'accounts/password_reset_form.html'}, name='password_reset'),
                        
                        # Confirmation of changing password by sending an email
                        # Pattern: finpy/password_reset/done
                        url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'accounts/password_reset_done.html'},name='password_reset_done'),

                        # Reset using CSFR token
                        # Pattern: finpy/reset/id/token
                        url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                            auth_views.password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
                        url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
                       )
