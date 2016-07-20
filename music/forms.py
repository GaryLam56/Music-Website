from django import forms
from django.contrib.auth.models import User
from .models import Album, Song, Folder


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #Turns the password into **** when typing

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class FolderForm(forms.ModelForm):
    
    class Meta:
        model = Folder
        fields = ['name']

class UploadSong(forms.Form):
    audio_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

