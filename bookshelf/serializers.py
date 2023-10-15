from bookshelf.models import Book, Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_day', 'biography']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['url', 'title', 'description', 'author', 'published_date', 'cover']
