from django.db import models

# Create your models here.


class Book(models.Model):
    isbn = models.CharField(max_length=17, unique=True)
    title = models.CharField(max_length=400)
    authors = models.CharField(max_length=400)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    cover = models.URLField(blank=True, null=True, max_length=400)
    year = models.CharField(max_length=4, blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.title
