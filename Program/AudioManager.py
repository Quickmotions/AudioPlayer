import time
from os import listdir, getcwd, name, system
from os.path import abspath, splitext
from time import sleep, time
from math import ceil
from select import select
import threading
# dependencies
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from pydub import AudioSegment

MUSIC_PATH = abspath(getcwd()) + '\\Music\\'


class MusicManager:
    def __init__(self, song, album, song_path):
        self.currently_playing = False
        self.song = song
        self.album = album
        self.song_path = song_path
        self.song_name, self.extension = splitext(self.song)
        self.paused = False

        if self.extension == '.mp3':
            song_type = MP3(self.song_path)
        elif self.extension == '.flac':
            song_type = FLAC(self.song_path)
        else:
            print("unsupported audio file type")
        try:
            self.duration = song_type.info.length
        except ValueError:
            self.duration = 0
        self.time_left = self.duration

    def audio_menu(self, time_left, time_total, currently_playing, song_name, album):
        clear_term()
        clock = f'{round(time_total - time_left)} / {round(time_total)}'
        percent_done = round((100 / time_total) * (time_total - time_left))
        bar = '─' * round(percent_done/2) + '⚪' + '─' * round(50 - percent_done/2)
        if currently_playing:
            play_button = '▐▐'
        else:
            play_button = '▶▶'
        print('───────────────────|FUNGUS AMP|────────────────────')
        print(f"now playing:  {song_name} \nfrom:  {album}")
        print(f'{bar}')
        print(f'     ──⠀{play_button} ──⠀⠀   ⠀{clock}                   ⠀───○ ⠀')
        print(f'\n1: resume      2: pause      3: skip      4: rewind')
        print('───────────────────|FUNGUS AMP|────────────────────')

    def play_song(self, playlist):
        self.time_left = self.duration
        self.currently_playing = True
        if self.extension == '.flac':
            flac_tmp_audio_data = AudioSegment.from_file(self.song_path, self.song_path.suffix[1:])
            flac_tmp_audio_data.export(self.song_path.name.replace(self.song_path.suffix, "") + ".wav", format="wav")
            temp_wav = f'{MUSIC_PATH}{self.album}\\{self.song_name}.wav'
        mixer.init()
        mixer.music.load(temp_wav)
        mixer.music.play()
        while True:
            music.audio_menu(self.time_left, self.duration, self.currently_playing, self.song_name, self.album)
            sleep(1)
            if self.currently_playing:
                self.time_left -= 1
                if self.time_left < 1:
                    self.currently_playing = False
                    playlist_edit(None, 'remove', playlist)
                    break

    def pause(self):
        mixer.music.pause()
        self.currently_playing = False

    def resume(self):
        mixer.music.unpause()
        self.currently_playing = True

    def skip(self):
        self.time_left = 0
        self.currently_playing = True

    def rewind(self):
        self.time_left = self.duration
        self.currently_playing = True
        mixer.music.rewind()

    def music_controller(self):
        settings = {'1': self.resume, '2': self.pause, '3': self.skip, '4': self.rewind}
        while self.time_left > 0:
            user_input = input()
            if self.time_left < 1:
                break
            for option in settings:
                if user_input.lower() == str(option):
                    settings[option]()


def clear_term():
    system('cls' if name == 'nt' else 'clear')


def playlist_edit(music: list(), option: str(), playlist: list()):
    if option == 'remove':
        del playlist[0]
        play_playlist(playlist, music_list)
    elif option == 'add':
        playlist.append(music.song)
    else:
        print("missing option (line 44)")
    return playlist


def setup_music():
    music = list()
    for album in listdir(MUSIC_PATH):
        songs = [f for f in listdir(MUSIC_PATH + album)]
        for song in songs:
            song_path = f'{MUSIC_PATH}{album}\\{song}'
            music.append(MusicManager(song, album, song_path))
    return music


def play_playlist(playlist, music_list):
    for music in music_list:
        if music.song == playlist[0]:
            print(f"now playing: {music.song_name} from {music.album}")
            print(f"next up:     {playlist[1]} from {music.album}")
            print('--------------------------------------')
            control_thread = threading.Thread(target=music.music_controller, args=[])
            music_thread = threading.Thread(target=music.play_song, args=[playlist])
            music_thread.start()
            control_thread.start()


if __name__ == '__main__':
    clear_term()
    # setup music
    playlist = list()
    music_list = setup_music()
    for music in music_list:
        playlist = playlist_edit(music, 'add', playlist)
    play_playlist(playlist, music_list)
