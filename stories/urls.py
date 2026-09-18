from django.urls import path

from .views import home_view, create_story_view,toggle_bookmark_view,toggle_like_view


urlpatterns = [
    path("", home_view, name="home"),

    path(
        "stories/create/",
        create_story_view,
        name="create_story"
    ),
    path("stories/<int:story_id>/like/", toggle_like_view, name="toggle_like"),
path("stories/<int:story_id>/bookmark/", toggle_bookmark_view, name="toggle_bookmark"),
]