from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^problem/(?P<problemid>\d+)/$', 'code_challenge.views.problem', name='problem'),
    url(r'^discussion/(?P<problemid>\d+)/$', 'code_challenge.views.discussion', name='discussion'),
    url(r'^add-discussion/(?P<problemid>\d+)/$', 'code_challenge.views.add_discussion', name='add-discussion'),
    url(r'^add-comment/(?P<discussionid>\d+)/$', 'code_challenge.views.add_comment', name='add_comment'),    
    url(r'^each_discussion/(?P<discussionid>\d+)/$', 'code_challenge.views.each_discussion', name='each_discussion'),
    
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'code_challenge/password_reset_form.html'}, name='reset_password_reset1'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'code_challenge/password_reset_done.html'}, name='password_reset_done'),
    url(r'^(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'code_challenge/password_reset_confirm.html'} , name='password_reset_confirm'),
    url(r'^done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'code_challenge/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^$', 'code_challenge.views.home', name='home'),
    url(r'^code_challenge$', 'code_challenge.views.home', name='home'),
    url(r'^add-post', 'code_challenge.views.add_post', name='add'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'code_challenge/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'code_challenge.views.register', name='regitser'),
    url(r'^add_problem$', 'code_challenge.views.add_problem', name='addproblem'),
    url(r'^trysubmit$', 'code_challenge.views.try_submit', name='trysubmit'),

    url(r'^profile/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', 'code_challenge.views.profile', name='profile'),
    url(r'^edit_profile$', 'code_challenge.views.edit_profile', name='edit'),
    url(r'^change_password$', 'django.contrib.auth.views.password_change', {'template_name': 'code_challenge/password_change_form.html'}, name='password_change'),
    url(r'^change_password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'code_challenge/password_change_done.html'}, name='password_change_done'),

    url(r'^follow/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', 'code_challenge.views.follow', name='follow'),
    url(r'^unfollow/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', 'code_challenge.views.unfollow', name='unfollow'),
    url(r'^follower_stream$', 'code_challenge.views.follower_stream', name='follower_stream'),
    url(r'^get_comments/$', 'code_challenge.views.get_comments', name='get-comments'),
    url(r'^foo/$', 'code_challenge.views.foo', name='foo'),

]
