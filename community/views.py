from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def board(request):
    receivePage = request.GET.get("page", "1")  # 페이지
    postListAllData = Post.objects.annotate(num_comments=Count("comment")).order_by(
        "-createdDate"
    )
    paginator = Paginator(postListAllData, 5)
    paginator_obj = paginator.get_page(receivePage)
    context = {"postList": paginator_obj}
    return render(request, "community/board.html", context)


def post_detail(request, post_id):
    idTargetPost = Post.objects.get(id=post_id)
    print(idTargetPost)

    if request.method == "POST":
        if request.user.is_authenticated:
            addPostUserId = request.user.id
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
    }
    return render(request, "community/post_detail.html", context)


def post_add(request):
    if request.user.is_authenticated:
        addPostUserId = request.user.id

        if request.method == "POST":
            addPostTitle = request.POST["title"]
            addPostContent = request.POST["content"]

            addPost = Post.objects.create(
                title=addPostTitle, content=addPostContent, writer=request.user
            )
            return redirect(f"/community/board/{addPost.id}")
    else:
        return redirect(f"/users/login/")
    return render(request, "community/post_add.html")


@login_required(login_url="/users/login/")
def post_modify(request, post_id):
    targetPost = get_object_or_404(Post, pk=post_id)

    if request.user != targetPost.writer:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect(f"board/{targetPost.post_id}")

    if request.method == "POST":
        modifyForm = PostForm(request.POST, instance=targetPost)

        if targetPost.is_valid():
            targetPost = modifyForm.save(commit=False)
            targetPost.modify_date = timezone.now()
            targetPost.save()
        return redirect(f"/community/board/{targetPost.id}")

    else:  # GET 요청인경우, 즉 수정하기 버튼을 눌렀을 경우
        modifyForm = Post(
            instance=targetPost
        )  # instance 속성으로 수정 누를시 글 내용과 동일하게 채워놔야함. 수정할수 있게

    context = {"form": modifyForm}

    return render(request, "community/post_add.html", context)
