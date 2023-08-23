from django.shortcuts import render, redirect
from community.models import Post, Comment
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages


def board(request):
    receivePage = request.GET.get('page', '1')  # 페이지
    postListAllData = Post.objects.annotate(num_comments=Count('comment')).order_by('-createdDate')
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


#@login_required(login_url='common:login')
#def post_modify(request, post_id):