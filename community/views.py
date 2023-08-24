from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from community.forms import PostForm

def board(request):
    receivePage = request.GET.get("page", "1")  # 페이지
    postListAllData = Post.objects.annotate(num_comments=Count("comment")).order_by(
        "-createdDate"
    )
    paginator = Paginator(postListAllData, 5)
    paginator_obj = paginator.get_page(receivePage)
    context = {"postList": paginator_obj,
                       "action": "view",}
    return render(request, "community/board.html", context)


def post_detail(request, post_id):
    idTargetPost = Post.objects.get(id=post_id)
    print(idTargetPost)
    idTargetPost.viewNum += 1
    idTargetPost.save()
    max_post_id = Post.objects.latest('id').id

    if request.method == "POST": # 상세보기 속에서 댓글작성 POST 요청 받을시
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            addComment = Comment.objects.create(
                content=comment_content,
                targetPost=idTargetPost,
                writer=request.user,
            )
        else:
            return redirect(f"/users/login/")

    context = {
        "post": idTargetPost,
        'max_post_id': max_post_id
    }
    return render(request, "community/post_detail.html", context)


def post_add(request):
    if request.user.is_authenticated:

        if request.method == "POST": # POST 글 작성을 완료할 경우
            addPostTitle = request.POST["title"]
            addPostContent = request.POST["content"]

            addPost = Post.objects.create(
                title=addPostTitle, content=addPostContent, writer=request.user
            )
            return redirect(f"/community/board/{addPost.id}")
    else: # 상세보기에서 글 작성하기 버튼을 누를 경우
        return redirect(f"/users/login/")
    context = {"action": "add"}
    return render(request, "community/post_add.html", context)


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
        context = {"form": modifyForm, "action": "modify", "post": targetPost}
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

    paginator = Paginator(searchPostList, 5)
    paginator_obj = paginator.get_page(receivePage)

    context = {
        'postList': paginator_obj,
        'search_kw': search_kw,
        'search_type': search_type,
        "action": "search",
    }

    return render(request, 'community/board.html', context)

