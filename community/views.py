from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from community.forms import PostForm
from django.utils.html import mark_safe
from django.http import JsonResponse
import markdown
import os

def indexBoard(request):
    return redirect(f"/community/notice/")

def board(request):
    receivePage = request.GET.get("page", "1")  # 페이지
    postListAllData = Post.objects.filter(notice_id__isnull=True).annotate(num_comments=Count("comment")).order_by(
        "-createdDate"
    )
    paginator = Paginator(postListAllData, 10)
    paginator_obj = paginator.get_page(receivePage)
    context = {"postList": paginator_obj,
                       "action": "view",}
    return render(request, "community/board.html", context)


def post_detail(request, post_id):
    idTargetPost = Post.objects.get(id=post_id)
    num_comments = idTargetPost.comment_set.count()
    idTargetPost.viewNum += 1
    idTargetPost.save()
    max_post_id = Post.objects.latest('id').id
    idTargetPost.content = mark_safe(markdown.markdown(idTargetPost.content))

    # 지운 게시글을 건너뛰고 이전 게시글 가져오기
    try: # id__lt = post_id 보다 작은 게시물들을 필터링 한다.
        # - 는 내림차순 정렬
        # [0] 은 정렬된 게시물 리스트 중, 가장 첫번째 게시물 선택
        prev_post = Post.objects.filter(id__lt=post_id).order_by('-id')[0]
    except IndexError:
        prev_post = None

    # 지운 게시글을 건너뛰고 다음 게시글 가져오기
    try:
        next_post = Post.objects.filter(id__gt=post_id).order_by('id')[0]
    except IndexError:
        next_post = None

    if request.method == "POST": # 상세보기 속에서 댓글작성 POST 요청 받을시
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            Comment.objects.create(
                content=comment_content,
                targetPost=idTargetPost,
                writer=request.user,
            )
        else:
            return redirect(f"/users/login/")

    context = {
        "post": idTargetPost,
        'max_post_id': max_post_id,
        "num_comments" : num_comments,
        'prev_post': prev_post,  # 이전 게시물 정보 추가
        'next_post': next_post   # 다음 게시물 정보 추가
    }
    return render(request, "community/post_detail.html", context)

def upload_image(request):
    if request.method == 'POST' and request.FILES["image"]:
        upload_image = request.FILES["image"]
        upload_image_name = upload_image.name
        upload_image_path = f"media/community/{{ request.username }}/" + upload_image_name
        print(upload_image_path)
        with open(upload_image_path, 'wb+') as destination: # 저장된 경로를 wb+ 쓰기와 바이너리 모드로 열고,
            # 연 파일 객체를 destination 변수에 할당
            for chunk in upload_image.chunks():
                destination.write(chunk)
        return JsonResponse({'상태': 'success', 'url': upload_image_path})
    return JsonResponse({'상태': 'error'})

def post_add(request):
    if request.user.is_authenticated: # 인증된 유저인 경우

        if request.method == "POST": # POST 글 작성을 완료할 경우
            addPostTitle = request.POST["title"]
            addPostContent = request.POST["content"]

            addPost = Post.objects.create(
                title=addPostTitle, content=addPostContent, writer=request.user
            )
            return redirect(f"/community/board/{addPost.id}")
        
        else: # 인증된 유저이지만 글 작성인경우
            context = {"action": "add",
                       "writer": request.user }
            return render(request, "community/post_add.html", context)

    else: # 게시물 목록에서 글 작성하기 버튼을 눌렀는데 로그인한 사용자가 아닌 경우
        return redirect(f"/users/login/")


@login_required(login_url="/users/login/")
def post_modify(request, post_id):
    targetPost = get_object_or_404(Post, pk=post_id)

    if request.user != targetPost.writer:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect(f"/community/board/{targetPost.id}")

    if request.method == "POST": # POST 요청인경우, 즉 수정을 완료했을경우
        modifyForm = PostForm(request.POST, instance=targetPost)

        targetPost = modifyForm.save(commit=False) # commit=False는 DB에 저장하지 않고 객체만 반환, But 밑코드 save()함수가 저장해줌 
        targetPost.modify_date = timezone.now()
        targetPost.save()
        return redirect(f"/community/board/{targetPost.id}")

    else:  # GET 요청인경우, 즉 수정하기 버튼을 눌렀을 경우
        modifyForm = PostForm(instance=targetPost)  # instance 속성으로 수정 누를시 글 내용과 동일하게 채워놔야함. 수정할수 있게
        context = {"form": modifyForm, "action": "modify", "post": targetPost, "writer": request.user }
        print(targetPost.title)
        return render(request, "community/post_add.html", context)
    

def board_search(request):
    search_kw = request.GET.get('search_kw', '')
    search_type = request.GET.get('search_type', 'title')
    receivePage= request.GET.get('page', "1")

    # 게시물 목록 기본 쿼리셋
    allPostList = Post.objects.annotate(num_comments=Count("comment")).order_by(
        "-createdDate")

    # 검색어가 있다면 필터 적용
    if search_kw:
        if search_type == 'title':
            searchPostList = allPostList.filter(title__icontains = search_kw)
        elif search_type == 'nickname':
            searchPostList = allPostList.filter(writer__nickname__icontains = search_kw)
        elif search_type == 'username':
            searchPostList = allPostList.filter(writer__username__icontains = search_kw)
        elif search_type == 'content':
            searchPostList = allPostList.filter(content__icontains=search_kw)

    paginator = Paginator(searchPostList, 10)
    paginator_obj = paginator.get_page(receivePage)

    context = {
        'postList': paginator_obj,
        'search_kw': search_kw,
        'search_type': search_type,
        "action": "search",
    }

    return render(request, 'community/board.html', context)

@login_required(login_url="/users/login/")
def board_delete(request, post_id):
    targetPost = get_object_or_404(Post, pk=post_id)

    if request.user != targetPost.writer:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect(f"/community/board/{targetPost.id}")

    if request.user == targetPost.writer:
        targetPost.delete()
        return redirect('/community/board/')
    else:
        return redirect(f"/community/board/{targetPost.id}")
    
@login_required(login_url="/users/login/")
def comment_delete(request, post_id, comment_id):
    targetComment = get_object_or_404(Comment, pk=comment_id)
    #post_id = comment_id

    if request.user != targetComment.writer:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect(f"/community/board/{post_id}")
    
    if request.user == targetComment.writer:
        targetComment.delete()
        return redirect(f'/community/board/{post_id}')
    else:
        return redirect(f"/community/board/{post_id}")


def notice(request):
    receivePage = request.GET.get("page", "1")  # 페이지
    postListAllData = Post.objects.filter(notice_id__isnull=False).annotate(num_comments=Count("comment")).order_by("-createdDate")
    paginator = Paginator(postListAllData, 10)
    paginator_obj = paginator.get_page(receivePage)
    context = {"postList": paginator_obj,
                       "action": "view",}
    return render(request, "community/notice.html", context)


def notice_detail(request, notice_id):
    idTargetPost = Post.objects.get(notice_id=notice_id)
    idTargetPost.viewNum += 1
    idTargetPost.save()

    max_post_id = Post.objects.latest('notice_id').notice_id

    context = {
        "post": idTargetPost,
        'max_post_id': max_post_id
    }
    return render(request, "community/notice_detail.html", context)