from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'worker.views.demo', name='home'),
    url(r'^judge', 'worker.views.judge', name='judge'),
    url(r'^demo', 'worker.views.demo', name='demo'),
]

