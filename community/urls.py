from django.urls import path
from community.views import board, post_detail, post_add, post_modify

urlpatterns = [
    path("board/", board),
    path("board/<int:post_id>/", post_detail),
    path("board/add/", post_add),
    path("board/<int:post_id>/modify/", post_modify),
]