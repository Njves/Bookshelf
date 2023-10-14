from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.TextField()
    birth_day = models.DateField()
    biography = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(null=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='cover/')

    class Meta:
        verbose_name_plural = 'Книги'
        verbose_name = 'Книга'
        ordering = ['-published_date']

    def __str__(self):
        return f'{self.title}, {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
