from django.urls import path
from community.views import board, post_detail, post_add

urlpatterns = [
    path("board/", board),
    path("board/<int:post_id>/", post_detail),
    path("board/add/", post_add),
]