from django.urls import path
from resources.views import *

urlpatterns = [
    path("share/", share),
    path("share/<int:post_id>/", share_detail),
]