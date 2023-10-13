from django.db import models


class Author(models.Model):
    name = models.TextField()
    birth_day = models.DateTimeField()
    biography = models.TextField()


class Book(models.Model):
    title = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date  = models.DateTimeField(null=True)
    description = models.TextField()
    cover = models.ImageField(upload_to='cover/')
