from bookshelf.models import Book, Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор автора
    """
    class Meta:
        model = Author
        fields = ['name', 'birth_day', 'biography']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор книг
    Имеет вложенный сериализатор автора
    """
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['url', 'title', 'description', 'author', 'published_date', 'cover']
