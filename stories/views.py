from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from gtts import gTTS

from .models import Story





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from gtts import gTTS
import cloudinary
import cloudinary.uploader

import os
import tempfile

from .models import Story


def home_view(request):
    stories = Story.objects.all().order_by("-created_at")

    return render(
        request,
        "home.html",
        {"stories": stories}
    )


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

            # Generate audio using gTTS
            tts = gTTS(
                text=content,
                lang=language
            )

            tts.save(temp_path)

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