from django.contrib import admin
from django.contrib.auth.models import User

from .models import Book, Author, Comment

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Comment)
