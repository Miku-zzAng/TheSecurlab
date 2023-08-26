from django.urls import path
from community.views import *

urlpatterns = [
    path("", indexBoard),
    path("board/", board),
    path("board/<int:post_id>/", post_detail),
    path("board/add/", post_add),
    path("board/<int:post_id>/modify/", post_modify),
    path("board/<int:post_id>/delete/", board_delete),
    path("board/search/", board_search, name='board_search'),
    path("board/<int:post_id>/delete/<int:comment_id>", comment_delete),
    path("notice/", notice,),
    path("notice/<int:notice_id>/", notice_detail),
]