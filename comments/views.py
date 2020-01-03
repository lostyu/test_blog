from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment_form = form.save(commit=False)
        comment_form.post = post
        comment_form.save()
        messages.add_message(request, messages.SUCCESS, '评论发布成功!', extra_tags='success')
        return redirect(post)  # 调用get_absolute_url

    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发布失败！', extra_tags='danger')
    return render(request, 'comments/preview.html', context)
