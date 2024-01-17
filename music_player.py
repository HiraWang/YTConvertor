import os
from pygame import *
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment


class MusicPlayer:
    def __init__(self, file_root):
        # creating the root window
        root = Tk()
        root.title('DataFlair Music player App ')
        # initialize mixer
        mixer.init()
        mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        init()  # turn all of pygame on.

        self.file_root = file_root
        self.root_path = os.getcwd() + self.file_root

        # create the listbox to contain songs
        self.songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
                                  selectbackground="gray", selectforeground="black")
        self.songs_list.grid(columnspan=9)
        self.addsongs()

    # add many songs to the playlist
    def addsongs(self):
        # a list of songs is returned
        temp_song = filedialog.askopenfilenames(initialdir='/Music', title="Choose a song",
                                                filetypes=(("mp3 Files", "*.mp3"),))
        # loop through everyitem in the list
        for s in temp_song:
            s = s.replace(self.root_path, "")
            self.songs_list.insert(END, s)


    def deletesong(self):
        curr_song = self.songs_list.curselection()
        self.songs_list.delete(curr_song[0])


    def Play(self):
        song = self.songs_list.get(ACTIVE)
        song = f'{song}'.replace('/', '\\')
        print(song)
        sound = AudioSegment.from_file("C:\\Users\\cy.wang\\MET\\Alan\\YTConverter\\Music\\MP4\\3 tuki. 一輪花.mp4", "mp4")
        sound.export("C:\\Users\\cy.wang\\MET\\Alan\\YTConverter\\Music\\MP3\\3 tuki. 一輪花.mp3", format="mp3")
        mixer.music.load("C:\\Users\\cy.wang\\MET\\Alan\\YTConverter\\Music\\MP3\\3 tuki. 一輪花.mp3")
        mixer.music.play()

    # to pause the song
    def Pause(self):
        mixer.music.pause()

    # to stop the  song
    def Stop(self):
        mixer.music.stop()
        self.songs_list.selection_clear(ACTIVE)

    # to resume the song
    def Resume(self):
        mixer.music.unpause()

    # Function to navigate from the current song
    def Previous(self):
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

    def Next(self):
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