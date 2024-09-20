from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        messages.error(request, 'You are cannot edit this post.')
        return redirect('post_detail', id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        messages.error(request, 'You are cannot delete this post.')
        return redirect('post_detail', id=post.id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('post_list')

# User Authentication and Authorization
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list')