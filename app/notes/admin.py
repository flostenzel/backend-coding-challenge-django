from django.contrib import admin
from notes.models import Note, Tag


class NoteAdmin(admin.ModelAdmin):
    fields = ['__all__', ]


admin.site.register(Note, NoteAdmin)


class TagAdmin(admin.ModelAdmin):
    fields = ['__all__', ]


admin.site.register(Tag, TagAdmin)
