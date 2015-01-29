from django.conf.urls  import *
from AdminHome import *

admin_urls = patterns('Admin.views',
    url(r'^$', HomePage.as_view()),
)
