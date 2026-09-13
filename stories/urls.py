from django.urls import path

from .views import home_view, create_story_view


urlpatterns = [
    path("", home_view, name="home"),

    path(
        "stories/create/",
        create_story_view,
        name="create_story"
    ),
]