import threading
from os import listdir
from os.path import isfile, join
from pygame import *
from tkinter import *
from audio_visualizer import *
from utility import *
import pygetwindow


class MusicPlayer:
    def __init__(self, list, file_root):
        # creating the root window
        # self.root = Tk()
        # self.root.title('DataFlair Music player App ')
        # self.root.withdraw()

        # init mixer para
        mixer.init()

        self.song = None
        self.list = list
        self.list_cnt = 0
        self.file_root = file_root
        self.root_path = os.getcwd() + self.file_root
        self.visualizer = None
        self.song_list = []
        self.add_songs()
        self.music_length = 0

    # add many songs to the playlist
    def add_songs(self):
        temp_song = ()
        if not os.path.isdir(self.root_path):
            return
        files = [f for f in sorted(listdir(self.root_path)) if isfile(join(self.root_path, f))]
        for file in files:
            file = self.root_path.replace('/', DIR_CHAR) + DIR_CHAR + file
            temp_song = temp_song + (file,)
            self.song_list.append(temp_song)
        # print("songs added")

    def delete_song(self):
        curr_song = self.songs_list.curselection()
        self.songs_list.delete(curr_song[0])

    def set(self):
        self.song = os.getcwd() + self.file_root + '/' + self.list.currentItem().text()
        self.music_length = self.get_music_length()
        mixer.music.load(self.song)

    def play(self, start=0):
        mixer.music.play(start=start)
        self.visualizer = AudioVisualizer(self.song)
        # t = threading.Thread(target=AudioVisualizer, args=(self.song,))
        # t.start()
        # p = multiprocessing.Process(target=AudioVisualizer, args=(self.song,))
        # p.start()
        self.music_length = self.get_music_length()

    def stop(self):
        mixer.music.stop()
        pygame.display.quit()

    def pause(self):
        mixer.music.pause()
        self.alwaysOnTop()

    def resume(self):
        mixer.music.unpause()
        self.alwaysOnTop()

    def alwaysOnTop(self):
        putty = pygetwindow.getWindowsWithTitle('pygame')[0]
        putty.activate()

    def get_current_time(self):
        return mixer.music.get_pos()

    def get_music_length(self):
        return pygame.mixer.Sound(self.song).get_length()
