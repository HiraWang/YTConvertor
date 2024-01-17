import os
from os import listdir
from os.path import isfile, join
from pygame import *
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment


class MusicPlayer:
    def __init__(self, file_root):
        # creating the root window
        root = Tk()
        root.title('DataFlair Music player App ')
        root.withdraw()

        # init mixer para
        mixer.init()

        self.file_root = file_root
        self.root_path = os.getcwd() + self.file_root

        # create the listbox to contain songs
        self.songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
                                  selectbackground="gray", selectforeground="black")
        self.songs_list.grid(columnspan=9)
        self.add_songs()

    # add many songs to the playlist
    def add_songs(self):
        temp_song = ()
        files = [f for f in listdir(self.root_path) if isfile(join(self.root_path, f))]
        for file in files:
            file = self.root_path.replace('/', '\\') + '\\' + file
            temp_song = temp_song + (file,)

        # loop through everyitem in the list
        for s in temp_song:
            s = s.replace(self.root_path, "")
            self.songs_list.insert(END, s)
        print("songs added")

    def delete_song(self):
        curr_song = self.songs_list.curselection()
        self.songs_list.delete(curr_song[0])

    def play(self):
        song = self.songs_list.get(ACTIVE)
        song = f'{song}'.replace('/', '\\')
        mixer.music.load(song)
        mixer.music.play()

    # to pause the song
    def pause(self):
        mixer.music.pause()

    # to stop the  song
    def stop(self):
        mixer.music.stop()
        self.songs_list.selection_clear(ACTIVE)

    # to resume the song
    def resume(self):
        mixer.music.unpause()

    # Function to navigate from the current song
    def previous(self):
        # to get the selected song index
        previous_one = self.songs_list.curselection()
        # to get the previous song index
        previous_one = previous_one[0] - 1
        # to get the previous song
        temp2 = self.songs_list.get(previous_one)
        temp2 = self.root_path + f'/{temp2}'
        mixer.music.load(temp2)
        mixer.music.play()
        self.songs_list.selection_clear(0, END)
        # activate new song
        self.songs_list.activate(previous_one)
        # set the next song
        self.songs_list.selection_set(previous_one)

    def next(self):
        print(self.songs_list)
        # to get the selected song index
        next_one = self.songs_list.curselection()
        # to get the next song index
        next_one = next_one[0] + 1
        # to get the next song
        temp = self.songs_list.get(next_one)
        temp = self.root_path + f'/{temp}'
        mixer.music.load(temp)
        mixer.music.play()
        self.songs_list.selection_clear(0, END)
        # activate newsong
        self.songs_list.activate(next_one)
        # set the next song
        self.songs_list.selection_set(next_one)