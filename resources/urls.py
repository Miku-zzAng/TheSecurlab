from django.urls import path
from resources.views import *

urlpatterns = [
    path("share/", share),
]