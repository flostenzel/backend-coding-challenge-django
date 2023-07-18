from django.urls import re_path
from notes.views import (NoteCreateView, NoteDetailView, NoteListView,
                         TagCreateView, TagDetailView, TagListView)

urlpatterns = [
    # Notes view
    re_path(r"^notes/note/create/$",
            NoteCreateView.as_view(), name="note-create"),
    re_path(r"^notes/note/list/$",
            NoteListView.as_view(), name="note-list"),
    re_path(r"^notes/note/(?P<pk>[0-9]+)/$",
            NoteDetailView.as_view(), name="note-detail"),
    # Tag views
    re_path(r"^notes/tag/create/$",
            TagCreateView.as_view(), name="tag-create"),
    re_path(r"^notes/tag/list/$",
            TagListView.as_view(), name="tag-list"),
    re_path(r"^notes/tag/(?P<pk>[0-9A-Fa-f\-]+)/$",
            TagDetailView.as_view(), name="tag-detail"),
]
