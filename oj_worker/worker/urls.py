from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'worker.views.judge', name='home'),
    url(r'^judge', 'worker.views.judge', name='judge'),
]

