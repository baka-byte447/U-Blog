from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # inbuilt django login method
from .models import Post
from .forms import PostFrom, UserRegistrationForm, CommentForm
from django.contrib import messages

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            posts = Post.objects.all().order_by('-created_at')
        else : # Normal user
            posts = Post.objects.filter(author = request.user).order_by('-created_at')

    else :
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'blogapp/home.html', {'posts':posts})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blogapp/signup.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostFrom(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostFrom()
    return render(request, 'blogapp/create_post.html', {'form': form})

def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_details', id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blogapp/post_details.html', {
        'post': post, 
        'comments': comments,
        'form': form
    })