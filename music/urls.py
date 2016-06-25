from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_folder/$', views.create_folder, name='create_folder'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
        url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^album/(?P<album_id>[0-9]+)/$', views.album, name='album'),
    url(r'^folder/(?P<folder_id>[0-9]+)/$', views.folder, name='folder'),
    url(r'^folder/(?P<int_id>[0-9]+)/upload_song/$', views.upload_song, name='upload_song_folder'),
    url(r'^album/(?P<int_id>[0-9]+)/upload_song/$', views.upload_song, name='upload_song_album'),
    url(r'^folders/$', views.folders, name='folders'),
    url(r'^albums/$', views.albums, name='albums'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^delete_song/(?P<song_id>[0-9]+)/from_all/$', views.delete_song, name='delete_song_from_all'),
    url(r'^folder/(?P<folder_id>[0-9]+)/delete_folder', views.delete_folder, name='delete_folder')
]
