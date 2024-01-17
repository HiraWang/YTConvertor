import os
from os import listdir
from os.path import isfile, join
from pygame import *
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment


class MusicPlayer:
    def __init__(self, list, file_root):
        # creating the root window
        root = Tk()
        root.title('DataFlair Music player App ')
        root.withdraw()

        # init mixer para
        mixer.init()

        self.list = list
        self.list_cnt = 0
        self.file_root = file_root
        self.root_path = os.getcwd() + self.file_root

        # create the listbox to contain songs
        self.song_list = []
        # self.songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
        #                           selectbackground="gray", selectforeground="black")
        # self.songs_list.grid(columnspan=9)
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

    def stop(self):
        mixer.music.stop()

    def pause(self):
        mixer.music.pause()

    def stop(self):
        mixer.music.stop()

    def resume(self):
        mixer.music.unpause()