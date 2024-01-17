import os
import sys
from os import listdir
from os.path import isfile, join
import threading
import multiprocessing
from pygame import *
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment
from audio_analyzer import *
from audio_visualizer import *
import pygetwindow


class MusicPlayer:
    def __init__(self, list, file_root):
        # creating the root window
        self.root = Tk()
        self.root.title('DataFlair Music player App ')
        self.root.withdraw()

        # init mixer para
        mixer.init()

        self.list = list
        self.list_cnt = 0
        self.file_root = file_root
        self.root_path = os.getcwd() + self.file_root
        self.visualizer = None
        self.song_list = []
        self.add_songs()

    # add many songs to the playlist
    def add_songs(self):
        temp_song = ()
        files = [f for f in listdir(self.root_path) if isfile(join(self.root_path, f))]
        for file in files:
            file = self.root_path.replace('/', '\\') + '\\' + file
            temp_song = temp_song + (file,)
            self.song_list.append(temp_song)
        # print("songs added")

    def delete_song(self):
        curr_song = self.songs_list.curselection()
        self.songs_list.delete(curr_song[0])

    def play(self):
        song = os.getcwd() + self.file_root + '/' + self.list.currentItem().text()
        mixer.music.load(song)
        mixer.music.play()
        self.visualizer = AudioVisualizer(song)
        # p = multiprocessing.Process(target=AudioVisualizer, args=(song,))
        # p.start()

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
