from os import listdir, getcwd, rename, mkdir, path
from os.path import abspath, splitext, join
from time import sleep
import threading
# dependencies
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


currently_playing = False
MUSIC_PATH = abspath(getcwd()) + '\\MediaManager\\Music\\'
music_files = {}
album_title = None
TEXT_ENCODING = 'utf8'
current_state = None


# Removes all ID3 tags from mp3 files in Music dir
def remove_tags():
    for album in listdir(MUSIC_PATH):
        for song in listdir(MUSIC_PATH + album):
            file_name = join(MUSIC_PATH + album, song)
            if file_name.lower().endswith('.mp3'):
                mp3 = MP3(file_name)
                try:
                    mp3.delete()
                    mp3.save()
                except ValueError:
                    print(song + 'has no ID3 tag')


# Removes and spaces in album and songs
def convert_files():
    for album in listdir(MUSIC_PATH):
        rename(MUSIC_PATH+album, MUSIC_PATH + (album.replace(" ", "")))

    for album in listdir(MUSIC_PATH):
        for song in listdir(MUSIC_PATH + album):
            rename(MUSIC_PATH+album+'\\'+song, MUSIC_PATH + album + '\\' + (song.replace(" ", "")))


def get_music(music: dict):
    for album in listdir(MUSIC_PATH):
        songs = [[f for f in listdir(MUSIC_PATH + album)]]
        music[album] = songs
    return music


def get_input(music):
    return next((elem for elem in music if elem == input('Type album title: ')), None)


def play_music(song, time_left):
    global currently_playing
    global current_state
    currently_playing = True
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()
    while currently_playing:
        sleep(1)
        if current_state == 'play':
            mixer.music.unpause()
            current_state = None
        if current_state == 'pause':
            mixer.music.pause()
            current_state = None
        if current_state == 'skip':
            mixer.music.stop()
            time_left = 0
            current_state = None
        time_left -= 1
        if time_left < 1:
            currently_playing = False




def control_music():
    settings = ['play', 'pause', 'skip']
    print('controls:', settings)
    global current_state
    while True:
        user_input = str(input("> "))
        for option in settings:
            if user_input == option:
                current_state = option



def player(album, music):
    global currently_playing
    album_path = MUSIC_PATH + album
    lst = [i for i in range(5)]
    song_list = [song for song in listdir(album_path)]
    for song in song_list:
        while currently_playing:
            sleep(5)
        # create thread and play songs until complete add audio settings in main
        song_path = MUSIC_PATH + album + '\\' + song
        song_name, extension = splitext(song)
        if extension == '.mp3':
            song_type = MP3(song_path)
        elif extension == '.flac':
            song_type = FLAC(song_path)
        else:
            print("unsupported audio file type")
            exit()

        if not currently_playing:
            try:
                print("playing: " + song)
                time_left = song_type.info.length
                control_thread = threading.Thread(target=control_music)
                music_thread = threading.Thread(target=play_music, args=[song_path , time_left])
                control_thread.start()
                music_thread.start()
                while currently_playing:
                    sleep(1)
            except ValueError:
                print("Could not play: " + song)


if __name__ == '__main__':
    remove_tags()
    convert_files()
    music_files = get_music(music_files)
    print(music_files.keys())
    while album_title is None:
        album_title = get_input(music_files)
    player(album_title, music_files)

