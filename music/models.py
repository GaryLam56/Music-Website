from django.contrib.auth.models import User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist

class Folder(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True)
    artist = models.CharField(max_length=250, default='')
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
