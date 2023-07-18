from authors.models import Author
from django.contrib import admin


class AuthorAdmin(admin.ModelAdmin):
    fields = ('__all__', )
    list_display = ("username", "password")


admin.site.register(Author, AuthorAdmin)
