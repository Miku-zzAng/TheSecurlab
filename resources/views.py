from django.shortcuts import render
from resources.models import SharePost
from django.core.paginator import Paginator

def share(request):
    # page 파라미터로 현재 페이지 번호를 가져옴. 기본값은 1
    current_page = request.GET.get("page", 1)  
    # 모든 게시물을 생성 날짜의 내림차순으로 가져옴
    all_posts = SharePost.objects.all().order_by('-createdDate')
    # 페이지당 9개의 게시물로 Paginator 객체 생성
    paginator = Paginator(all_posts, 9)
    # 현재 페이지에 해당하는 게시물들만 가져옴
    page_posts = paginator.get_page(current_page)

    context = {
        "postList": page_posts,  # 현재 페이지의 게시물들
        "action": "view",  # 보기 액션
    }

    return render(request, "resources/share.html", context)

def share_detail(request,post_id):
    idTargetPost = SharePost.objects.get(id=post_id)
    context = {
        "post": idTargetPost,
    }
    return render(request, "resources/share_detail.html", context)