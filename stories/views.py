from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
import requests
import cloudinary
import cloudinary.uploader

import os
import tempfile

from .models import Story,Bookmark,Like


from django.db.models import Count

def home_view(request):
    stories = Story.objects.all().order_by("-created_at")

    recommended = None

    if request.user.is_authenticated:
        for story in stories:
            story.is_liked = Like.objects.filter(user=request.user, story=story).exists()
            story.is_book = Bookmark.objects.filter(user=request.user, story=story).exists()

        # user ne jo genres like kiye hain unki list
        liked_genres = Like.objects.filter(user=request.user).values_list('story__genre', flat=True).distinct()

        if liked_genres:
            recommended = Story.objects.filter(genre__in=liked_genres).exclude(likes__user=request.user).order_by('-created_at')[:3]
        else:
            # naya user - trending dikhao
            recommended = Story.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    else:
        for story in stories:
            story.is_liked = False
            story.is_book = False

    paginator=Paginator(stories,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj, "recommended": recommended})

# Real voice IDs confirmed available on your ElevenLabs account.
GENRE_VOICE_MAP = {
    "horror": "N2lVS1w4EtoT3dr4eOWO",     # Callum - gravelly, unsettling
    "romance": "EXAVITQu4vr4xnSDxMaL",    # Sarah - warm, reassuring
    "comedy": "cgSgspJ2msm6clMCkdW9",     # Jessica - playful, bright
    "adventure": "SOYHLrjzK2X1ezoPC6cr",  # Harry - fierce warrior energy
    "default": "JBFqnCBsd6RMkjVDRZzb",    # George - warm storyteller
}


def pick_voice_id_for_genre(genre):
    """Pick a voice_id for the given genre, falling back to the default narrator voice."""
    return GENRE_VOICE_MAP.get(genre.lower(), GENRE_VOICE_MAP["default"])


def generate_elevenlabs_audio(text, genre, output_path):
    """Generate narration audio using ElevenLabs TTS and save it to output_path."""

    voice_id = pick_voice_id_for_genre(genre)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        # eleven_multilingual_v2 is best for longer-form narration quality.
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)


@login_required
def create_story_view(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        language = request.POST.get("language")
        genre = request.POST.get("genre")

        # Create story first
        story = Story.objects.create(
            author=request.user,
            title=title,
            content=content,
            language=language,
            genre=genre
        )

        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
            api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
            api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
        )

        # Create temporary MP3 file
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        )

        temp_path = temp_file.name
        temp_file.close()

        try:

            # Generate audio using ElevenLabs (much more natural narration than gTTS)
            generate_elevenlabs_audio(
                text=content,
                genre=genre,
                output_path=temp_path
            )

            # Upload MP3 to Cloudinary
            result = cloudinary.uploader.upload(
                temp_path,
                resource_type="video",
                folder="storyverse/audio"
            )

            # Save Cloudinary URL in Story
            story.audio = result["secure_url"]
            story.save()

        finally:

            # Delete temporary local file
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return redirect("home")

    return render(
        request,
        "create_story.html"
    )

@login_required
def toggle_like_view(request, story_id):
    story = Story.objects.get(id=story_id)
    # like, created = Like.objects.get_or_create(user=request.user, story=story)
    user=request.user

    l=Like.objects.filter(user=user,story=story)
    if l.exists():
        l.delete()
        print("like deletd ")

    else:
        like=Like.objects.create(
                user=user,
                story=story
            )
        print(like)
        like.save()

        redirect('home')


    

    return redirect("home")


@login_required
def toggle_bookmark_view(request, story_id):
    story = Story.objects.get(id=story_id)
    if request.user:
        bookmark=Bookmark.objects.filter(story=story,user=request.user)
        if bookmark:
            bookmark.delete()
            print("bookmark dleted successfully ")
        else:
            book=Bookmark.objects.create(
                user=request.user,
                story=story
            )
            print(f"book marked suuccefully{book}")    
            book.save()


    return redirect("home")


