import re

from django.db.models import Q
from notes.models import Note, Tag
from notes.serializers import NoteSerializer, TagSerializer
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class NoteCreateView(CreateAPIView):
    """
    API view for creating a new note via POST.
    Required: title:str, body:str
    Optional: tags: list(Tag), is_public: Boolean
    """
    serializer_class = NoteSerializer


class NoteListView(ListAPIView):
    """
    API view for retrieving a list of notes.
    GET: Returns a filtered list of notes based on additional query parameters and the
        user's authentication status.
    Query Params:
        "search" for content in notes body
        "tags" for notes with tag_uuid
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["body"]
    queryset = Note.objects.all()

    def get_queryset(self):
        """
        Returns a filtered queryset of notes based on additional query parameters and the
            user's authentication status.
        - If "search" as query parameters search contents of notes with keywords
        - If "tags" as query parameters filter notes notes via tags
        - If the user is anonymous (=unauthenticated), only public notes are returned.
        - If the user is authenticated, their notes and public notes are returned.
        """
        queryset = super().get_queryset()

        # Look for tag as query param
        tag_query = self.request.query_params.get('tag', None)

        if tag_query:
            # Find all uuids in query param via regrex
            uuid_regrex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
            for tag_uuid in re.findall(uuid_regrex, tag_query, re.DOTALL):
                # Filter in loop to only keep notes which have all the tags found in query params
                queryset = queryset.filter(tags__pk=tag_uuid, author=self.request.user)

        if self.request.user.is_anonymous:
            return queryset.filter(is_public=True)
        return queryset.filter(Q(author=self.request.user) | Q(is_public=True))


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving (GET), updating (UPDATE), and deleting (DELETE) a note.
    """
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        """
        Returns a filtered queryset of notes belonging to the authenticated user.
        """
        return Note.objects.filter(author=self.request.user)


class TagCreateView(CreateAPIView):
    """
    API view for creating a new tag with POST.
    Required: title: str
    """
    serializer_class = TagSerializer


class TagDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving (GET), updating (UPDATE), and deleting (DELETE) a tag.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """
        Returns a filtered queryset of tags associated with the authenticated user's notes.
        """
        queryset = super().get_queryset()
        return queryset.filter(notes__author=self.request.user)


class TagListView(ListAPIView):
    """
    API view for retrieving a list of all tags.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    # TODO: Find out if this is necessary
    # def get_queryset(self):
    #     # Returns only the tags associated with authors notes
    #     queryset = super().get_queryset()
    #     return queryset.filter(notes__author=self.request.user)
