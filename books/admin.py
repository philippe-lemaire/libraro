from django.contrib import admin
from .models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["isbn", "title", "authors", "publisher"]
    list_filter = [
        "authors",
        "publisher",
    ]


admin.site.register(Book, BookAdmin)
