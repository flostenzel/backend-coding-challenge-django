from notes.models import Note, Tag
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("author",)


class TagSerializer(serializers.ModelSerializer):
    notes = NoteSerializer

    class Meta:
        model = Tag
        fields = "__all__"
