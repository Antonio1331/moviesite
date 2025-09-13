from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    type = models.CharField(verbose_name="Nomi", max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        db_table = 'genres'

class Movie(models.Model):
    title = models.CharField(verbose_name="Nomi", max_length=75, unique=True)
    director = models.CharField(verbose_name="Rejissori", max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name="Ma'lumoti", null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies', verbose_name="Janri")
    cover = models.ImageField(verbose_name="Posteri", upload_to='covers/', null=True, blank=True)
    video = models.FileField(verbose_name="Kinosi", upload_to='videos/', null=True, blank=True)
    release = models.DateField(verbose_name="Chiqgan sanasi")
    views = models.IntegerField(verbose_name="Ko'rishlar soni", default=0)
    published = models.BooleanField(verbose_name="Saytga chiqarish?", default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        db_table = 'movies'

class Comment(models.Model):
    text = models.CharField(verbose_name="Matni", max_length=500)
    movie  = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Kino")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'comments'
