from django.contrib import admin
from .models import Album, Song, Folder

admin.site.register(Album)# adds Albums to the admin page
admin.site.register(Song)# adds Songs to the admin page
admin.site.register(Folder)# adds Folder to the admin page