from django.contrib import admin

from .models import Book, Author, Comment

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Comment)
