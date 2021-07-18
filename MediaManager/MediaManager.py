from os import listdir, getcwd, rename, mkdir, path
from os.path import abspath, splitext, join
from time import sleep
import threading
# dependencies
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


currently_playing = False
music_path = abspath(getcwd()) + '\\MediaManager\\Music\\'
music_files = {}
album_title = None
TEXT_ENCODING = 'utf8'


# Removes all ID3 tags from mp3 files in Music dir
def remove_tags():
    for album in listdir(music_path):
        for song in listdir(music_path + album):
            file_name = join(music_path + album, song)
            if file_name.lower().endswith('.mp3'):
                mp3 = MP3(file_name)
                try:
                    mp3.delete()
                    mp3.save()
                except ValueError:
                    print(song + 'has no ID3 tag')


# Removes and spaces in album and songs
def convert_files():
    for album in listdir(music_path):
        rename(music_path+album, music_path + (album.replace(" ", "")))

    for album in listdir(music_path):
        for song in listdir(music_path + album):
            rename(music_path+album+'\\'+song, music_path + album + '\\' + (song.replace(" ", "")))


def get_music(music: dict):
    for album in listdir(music_path):
        songs = [[f for f in listdir(music_path + album)]]
        music[album] = songs
    return music


def get_input(music):
    return next((elem for elem in music if elem == input('Type album title: ')), None)


def play_music(song):
    global currently_playing
    currently_playing = True
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(5)
    currently_playing = False



def player(album, music):
    global currently_playing
    album_path = music_path + album
    lst = [i for i in range(5)]
    song_list = [song for song in listdir(album_path)]
    for song in song_list:
        while currently_playing:
            sleep(5)
        # create thread and play songs until complete add audio settings in main
        song_path = music_path + album + '\\' + song
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
                # t1 = threading.Thread(target=main)
                t2 = threading.Thread(target=play_music, args=[song_path])
                # t1.start()
                t2.start()
                sleep(song_type.info.length)
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
