from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.db.models import Q
from django.core.urlresolvers import reverse
from .forms import AlbumForm, UserForm, FolderForm, UploadSong, SongForm
from .models import Album, Song, Folder
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import resolve

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            #return render(request, 'music/album.html', {'album': album})
            return HttpResponseRedirect('/music/album/' + str(album.id))
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)
    
def create_folder(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = FolderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            newdoc = form.save(commit=False)
            newdoc.user = request.user
            newdoc.save()
            return HttpResponseRedirect('/music/folders')
        context = {
            'form': form,
        }
        return render(request, 'music/create_folder.html', context)

def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    #return render(request, 'music/index.html', {'albums': albums})
    return HttpResponseRedirect('/music/albums/')

def delete_song(request, song_id):
    current_url = resolve(request.path_info).url_name
    song = Song.objects.get(pk=song_id)
    if(song.folder):
        folder_id = song.folder.id
        song.delete()
        if(current_url == 'delete_song_from_all'): return HttpResponseRedirect('/music/songs/all/')
        return HttpResponseRedirect('/music/folder/' + str(folder_id)) #redirects them to the folder page
        #return render(request, 'music/folder.html', {'folder': Folder.objects.get(pk=folder_id)})
    else:
        album_id = song.album.id
        song.delete()
        if(current_url == 'delete_song_from_all'): return HttpResponseRedirect('/music/songs/all/')
        return HttpResponseRedirect('/music/album/' + str(album_id)) #redirects them to the album page
        #return render(request, 'music/album.html', {'album': album})


def album(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        #user = request.user
        #album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/album.html', {'album': get_object_or_404(Album, pk=album_id), 'user': request.user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        folders = Folder.objects.filter(user=request.user)
        query = request.GET.get("q")# get the query
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            folders = folders.filter(
                 Q(name__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
                'folders': folders
            })
        return render(request, 'music/index.html', {
                'albums': albums,
                'folders': folders
        })

def albums(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/albums.html', {'albums': albums})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None) #gets the user form
    if form.is_valid():
        user = form.save(commit=False) #Creates a user Object that is empty (commit=false makes the object empty)
        # cleaned (normalized) data 
        username = form.cleaned_data['username'] # sets clean username
        password = form.cleaned_data['password'] # sets clean password
        user.set_password(password) # updates password
        user.save() #saves the user
        user = authenticate(username=username, password=password) # returns User objects if credentials are correct
        if user is not None: # if it's a user that exist
            if user.is_active: # if user is active/not banned/exist/logged in
                login(request, user)#login the user
                #request.user.username prints out the username
                albums = Album.objects.filter(user=request.user) 
                return render(request, 'music/index.html', {'albums': albums}) #redirects the user to the main page of user
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context) # returns them to a blank form if they can't log in


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            for folder in Folder.objects.filter(user=request.user):
                for song in folder.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        except Folder.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
        

def folders(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        folders = Folder.objects.filter(user=request.user)
        return render(request, 'music/folders.html', {'folders': folders})
    
def folder(request, folder_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        folder = get_object_or_404(Folder, pk=folder_id)
        folder.user = request.user
        return render(request, 'music/folder.html', {'folder': folder, 'user': folder.user})
        #return reverse('folder')
    
def upload_song(request, int_id):
    current_url = resolve(request.path_info).url_name
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    elif(current_url == 'upload_song_folder'):
        folder_id = int_id
        form = UploadSong(request.POST or None, request.FILES or None)
        folder = get_object_or_404(Folder, pk=folder_id)
        if form.is_valid():
            files = request.FILES.getlist('audio_file')
            for f in files:
                song = SongForm(initial={'song_title':f.name}).save(commit=False)# Creates a form with an initial title song and creates and empty object Song
                song.song_title = f.name.replace(' ', '')[:-4] #sets the song to be only the
                song.folder = folder
                song.audio_file = f #sets the audio file
                file_type = song.audio_file.url.split('.')[-1] #gets the thing after the dot?
                file_type = file_type.lower()# makes it lowercase
                if check_file_type(file_type):
                    song.save()
                else:
                    return render(request, 'music/upload_song.html', context = {'form': form,'error_message': 'Audio file must be WAV, MP3, or OGG',}) #leaves them at the with an error message aka the context
            return HttpResponseRedirect('/music/folder/' + str(folder_id))
        context = {'form': form, 'folder':folder}
        return render(request, 'music/upload_song.html', context) # remember that music/upload_song.html is a file path
    else:
        album_id = int_id
        form = UploadSong(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            files = request.FILES.getlist('audio_file')
            for f in files:
                song = SongForm(initial={'song_title':f.name}).save(commit=False)# Creates a form with an initial title song and creates and empty object Song
                song.song_title = f.name.replace(' ', '')[:-4] #sets the song to be only the
                song.album = album
                song.audio_file = f #sets the audio file
                file_type = song.audio_file.url.split('.')[-1] #gets the thing after the dot?
                file_type = file_type.lower()# makes it lowercase
                if check_file_type(file_type):
                    song.save()
                else:
                    return render(request, 'music/upload_song.html', {'form': form,'error_message': 'Audio file must be WAV, MP3, or OGG',}) #leaves them at the with an error message aka the context
            return HttpResponseRedirect('/music/album/' + str(album_id))
        context = {'form': form, 'album':album}
        return render(request, 'music/upload_song.html', context) # remember that music/upload_song.html is a file path
    

def check_file_type(file_type): # this function checks the audio type, is a boolean
    if file_type not in AUDIO_FILE_TYPES:
        return False
    else: #is the file is an audio file
        return True
    
def delete_folder(request, folder_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        folder = Folder.objects.get(pk=folder_id)
        folder.delete()
        return HttpResponseRedirect('/music/folders/')