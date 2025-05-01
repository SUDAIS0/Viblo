from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Video, Comment, Like
from .form import VideoUploadForm, UserRegisterForm, CommentForm
from fuzzywuzzy import fuzz 

# Home page - List of all videos
def home(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'core/home.html', {'videos': videos})

# Upload Video - For logged-in users
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoUploadForm()
    return render(request, 'core/upload_video.html', {'form': form})

# View single video with comments & like functionality
def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    all_videos = Video.objects.exclude(id=video.id)
    comments = video.comments.all().order_by('timestamp')
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(video=video, user=request.user).exists()

    # Handle comment form
    if request.method == 'POST' and 'comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return redirect('video_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'core/video_details.html', {
        'video': video,
        'all_videos': all_videos,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'total_likes': video.total_likes()
    })

# Toggle Like/Unlike
@login_required
def toggle_like(request, slug):
    video = get_object_or_404(Video, slug=slug)
    like, created = Like.objects.get_or_create(video=video, user=request.user)
    if not created:
        like.delete()
    return redirect('video_detail', slug=slug)

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('home')

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def search_videos(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        videos = Video.objects.all()
        for video in videos:
            title_score = fuzz.partial_ratio(query.lower(), video.title.lower())
            desc_score = fuzz.partial_ratio(query.lower(), video.description.lower())
            avg_score = max(title_score, desc_score)

            if avg_score > 60:  # You can tweak this threshold
                results.append((avg_score, video))

        # Sort by best match
        results = sorted(results, key=lambda x: x[0], reverse=True)
        results = [video for score, video in results]

    return render(request, 'core/search_results.html', {
        'query': query,
        'results': results,
    })



