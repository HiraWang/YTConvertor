import functools
import os
from os import listdir
from os.path import isfile, join
import sys
import shutil
import requests
import threading
import subprocess
from pytube import Playlist
from pytube import YouTube
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from music_player import *
from utility import *
from ui_unit import *

g_pytube_trigger = True
g_pydub_trigger = True


def exit_exe(self):
    sys.exit(0)


def on_progress(stream, chunk, remains):
    total = stream.filesize
    percent = int((total-remains) / total * 100)
    print('=' * percent + ' ' * (100 - percent))


def convert_playlist(urls, file_root, info_root, icon_root, extension):
    cnt = 1
    tot_cnt = len(urls)
    for i in urls:
        if g_pytube_trigger:
            yt = YouTube(i, on_progress_callback=on_progress)

            name = str(cnt) + ' ' + str(yt.author) + ' ' + str(yt.title)
            name = name.replace('/', '')
            name = name.replace('?', '')
            name = name.replace('"', '')
            name = name.replace('～', '')
            name = name.replace('|', '')
            name = name.replace('@', '')
            fn = name + extension
            print(i, fn)

            f = open(os.getcwd() + info_root + '/' + str(cnt) + '.txt', 'w', encoding='UTF-8')
            f.write(name + '.mp3' + '\n')
            f.write(str(yt.author) + '\n')
            f.write(str(yt.title) + '\n')
            f.write(str(i) + '\n')
            f.write(str(yt.thumbnail_url) + '\n')
            f.close()

            yt.streams.filter().get_audio_only().download(output_path=os.getcwd() + file_root, filename=fn)

            img_data = requests.get(str(yt.thumbnail_url)).content
            with open(os.getcwd() + icon_root + '/' + str(cnt) + '.jpg', 'wb') as handler:
                handler.write(img_data)

            cnt += 1
        else:
            break
    print('playlist conversion finished')
    return


def convert_audio(mp4_root, mp3_root, extension_mp4, extension_mp3):
    extension_mp4 = extension_mp4.replace('.', '')
    extension_mp3 = extension_mp3.replace('.', '')

    for file in os.listdir(os.getcwd() + mp4_root):
        if g_pydub_trigger:
            filename = os.fsdecode(file)
            if filename.endswith(extension_mp4):
                filename_in = os.getcwd().replace('/', '\\') + mp4_root.replace('/', '\\') + '\\' + filename
                sound = AudioSegment.from_file(filename_in, extension_mp4)
                filename_out = os.getcwd().replace('/', '\\') + mp3_root.replace('/', '\\') + '\\' + filename.replace(extension_mp4, extension_mp3)
                sound.export(filename_out, format=extension_mp3)
            else:
                continue
        else:
            break
    print('audio conversion finished')
    return


class UpperView(QWidget):
    def __init__(self, window, device, size):
        super().__init__()

        # New widgets
        self.window = window
        self.size_handler = SizeHandler(UPPER_VIEW, size)
        self.layout = QHBoxLayout()
        self.setStyleSheet("""
                           QPushButton {
                               background-color: """ + white_color + """; 
                               border: 2px solid black;
                               border-radius: 5px;
                               font: bold """ + self.size_handler.font_size + """;
                           }
                           QPushButton:hover {
                               background-color: """ + light_gray_color + """; 
                               border: 2px solid black;
                               border-radius: 5px;
                               font: bold """ + self.size_handler.font_size + """;
                           }
                           """)
        self.exit_button = Button('Exit',
                                  self.size_handler.button_w,
                                  self.size_handler.button_w,
                                  exit_exe,
                                  color=white_color,
                                  hover_color=light_gray_color,
                                  pressed_color=gray_color,
                                  font_size=self.size_handler.font_size,
                                  font_color=white_color,
                                  is_icon=True,
                                  icon=IMAGE_EXIT)

        pixmap = QPixmap(os.getcwd() + IMAGE_MET_LOGO)
        self.logo = QLabel()
        self.logo.setPixmap(pixmap)
        self.logo.show()

        self.layout.addStretch(10)
        self.layout.addWidget(self.exit_button, alignment=Qt.AlignRight)
        self.layout.addWidget(self.logo, alignment=Qt.AlignRight)
        self.setLayout(self.layout)


class BottomView(QWidget):
    def __init__(self, window, device, size):
        super().__init__()
        self.window = window
        self.tot_cnt = 0
        self.mp4_max_cnt = 0
        self.mp3_max_cnt = 0
        self.mp4_root = '/Music/MP4'
        self.mp3_root = '/Music/MP3'
        self.info_root = '/Info'
        self.icon_root = '/Icon'
        self.extension_mp4 = '.mp4'
        self.extension_mp3 = '.mp3'
        self.song_list = QListWidget()
        self._list_items = list()
        self.init_list()
        self.player = MusicPlayer(self.song_list, self.mp3_root)

        self.size_handler = SizeHandler(BOTTOM_VIEW, size)
        self.label_w = self.size_handler.label_w
        self.label_h = self.size_handler.label_h
        self.edit_w = self.size_handler.edit_w
        self.edit_h = self.size_handler.edit_h
        self.msg_box_w = self.size_handler.message_box_w
        self.msg_box_h = self.size_handler.message_box_h
        self.unit_w = self.size_handler.unit_w
        self.unit_h = self.size_handler.unit_h
        self.button_w = self.size_handler.button_w
        self.button_h = self.size_handler.button_h
        self.widget_w = 700
        self.widget_h = 800
        self.label_style = """
                           border: 0px;
                           color: white; 
                           font: bold """ + self.size_handler.font_size + """;
                           """
        self.unit_style = """
                          border: 0px;
                          color: black; 
                          font: bold """ + self.size_handler.font_size + """;
                          """
        self.line_edit_style = """ 
                               QLineEdit  {
                                   background-color: """ + white_color + """; 
                                   border: 2px solid black;
                                   border-radius: 2px;
                                   color: """ + deep_gray_color + """; 
                                   font: """ + self.size_handler.font_size + """
                               }
                               """
        self.widget_style = """ 
                            QWidget  {
                                border: 2px solid black;
                                background-color: """ + light_black_color + """; 
                                border-radius: 10px;
                            }
                            """

        self.playlist_label = QLabel(self)
        self.playlist_label.setFixedWidth(self.label_w)
        self.playlist_label.setFixedHeight(self.label_h)
        self.playlist_label.setText('URL')
        self.playlist_label.setStyleSheet(self.label_style)
        self.playlist_edit = QLineEdit(self)
        self.playlist_edit.setStyleSheet(self.line_edit_style)
        self.playlist_edit.setFixedWidth(self.edit_w)
        self.playlist_edit.setFixedHeight(self.edit_h)
        self.playlist_set_button = ButtonRect('SET',
                                              self.button_w,
                                              self.edit_h,
                                              self.set_playlist,
                                              color=white_color,
                                              hover_color=light_gray_color,
                                              pressed_color=white_color,
                                              font_size=self.size_handler.font_size,
                                              font_color="black",
                                              is_icon=False)
        self.add_song_button = ButtonRect('ADD',
                                          self.button_w,
                                          self.edit_h,
                                          self.add_songs,
                                          color=white_color,
                                          hover_color=light_gray_color,
                                          pressed_color=white_color,
                                          font_size=self.size_handler.font_size,
                                          font_color="black",
                                          is_icon=False)
        self.open_mp3_folder_button = Button('MP3',
                                             self.button_w,
                                             self.button_h,
                                             self.open_mp3_folder,
                                             color=white_color,
                                             hover_color=handle_color,
                                             pressed_color=handle_pressed_color,
                                             font_size=self.size_handler.font_size,
                                             font_color="black",
                                             is_icon=True,
                                             icon=IMAGE_MUSIC)
        self.open_mp4_folder_button = Button('MP4',
                                             self.button_w,
                                             self.button_h,
                                             self.open_mp4_folder,
                                             color=white_color,
                                             hover_color=handle_color,
                                             pressed_color=handle_pressed_color,
                                             font_size=self.size_handler.font_size,
                                             font_color="black",
                                             is_icon=True,
                                             icon=IMAGE_MUSIC)
        self.msg_box_pytube = MessageBox(self.size_handler.msg_w,
                                         self.size_handler.msg_h,
                                         color=light_gray_color,
                                         font_size=self.size_handler.msg_font_size,
                                         font_color=black_color)
        self.msg_box_pydub = MessageBox(self.size_handler.msg_w,
                                        self.size_handler.msg_h,
                                        color=light_gray_color,
                                        font_size=self.size_handler.msg_font_size,
                                        font_color=black_color)
        self.convert_button = ButtonTwoState('CONVERT', 'STOP',
                                             self.button_w,
                                             self.button_h,
                                             self.start_pytube,
                                             self.stop_pytube,
                                             color=white_color,
                                             hover_color=handle_color,
                                             pressed_color=handle_pressed_color,
                                             font_size=self.size_handler.font_size,
                                             font_color=white_color,
                                             is_icon=True,
                                             icon_default=IMAGE_SCAN,
                                             icon_pressed=IMAGE_STOP)
        self.export_button = ButtonTwoState('EXPORT', 'STOP',
                                            self.button_w,
                                            self.button_h,
                                            self.start_pydub,
                                            self.stop_pydub,
                                            color=white_color,
                                            hover_color=handle_color,
                                            pressed_color=handle_pressed_color,
                                            font_size=self.size_handler.font_size,
                                            font_color=white_color,
                                            is_icon=True,
                                            icon_default=IMAGE_EXPORT,
                                            icon_pressed=IMAGE_STOP)

        self.playlist = 'https://youtube.com/playlist?list=PLFdgdNMl_r3Ks7Au7SFJiRaMXwWrdikxR&si=ejV4p3yJ2QZpbaW4'
        self.playlist_edit.setText(self.playlist)
        self.playlist_edit.setCursorPosition(0)
        self.thread_pytube = None
        self.timer_pytube = QTimer()
        self.timer_pytube.timeout.connect(self.update_pytube_status)
        self.yt_title = []
        self.yt_author = []
        self.yt_thumbnail_url = []

        self.thread_pydub = None
        self.timer_pydub = QTimer()
        self.timer_pydub.timeout.connect(self.update_pydub_status)

        self.layout = QHBoxLayout()
        self.layout_convertor = QVBoxLayout()
        self.layout_playlist = QHBoxLayout()
        self.layout_playlist.addStretch(1)
        self.layout_playlist.addWidget(self.playlist_label)
        self.layout_playlist.addWidget(self.playlist_edit)
        self.layout_playlist.addStretch(1)
        self.layout_playlist.addWidget(self.playlist_set_button)
        self.layout_playlist.addStretch(1)
        self.layout_playlist.addWidget(self.add_song_button)
        self.layout_playlist.addStretch(1)
        self.layout_convertor.addItem(self.layout_playlist)
        self.layout_msg_box = QHBoxLayout()
        self.layout_msg_box.addWidget(self.msg_box_pytube, alignment=Qt.AlignCenter)
        self.layout_msg_box.addWidget(self.msg_box_pydub, alignment=Qt.AlignCenter)
        self.layout_convertor.addItem(self.layout_msg_box)
        self.layout_convertor_button = QHBoxLayout()
        self.layout_convertor_button.addWidget(self.convert_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.open_mp4_folder_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.open_mp3_folder_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.export_button, alignment=Qt.AlignCenter)
        self.layout_convertor.addItem(self.layout_convertor_button)
        self.widget_convertor = QWidget()
        self.widget_convertor.setFixedWidth(self.widget_w * 1.2)
        self.widget_convertor.setFixedHeight(self.widget_h)
        self.widget_convertor.setStyleSheet(self.widget_style)
        self.widget_convertor.setLayout(self.layout_convertor)

        self.song_list.setFixedHeight(500)
        self.song_list.setStyleSheet("""
                                     QListWidget{
                                        border-radius: 0px;
                                        color: """ + deep_gray_color + """;
                                        background: """ + light_gray_color + """;
                                     }
                                     QListWidget::item:hover{
                                        color: """ + black_color + """;
                                        background: """ + handle_color + """;
                                     }
                                     QListWidget::item:selected{
                                        color: """ + black_color + """;
                                        background: """ + button_color + """;
                                     }
                                     QScrollBar:vertical {
                                        border-left: 2px solid black;
                                        border-right: 0px solid black;
                                        background: """ + gray_color + """;
                                        width: 25px;
                                        margin: 15px 0 15px 0;
                                        border-radius: 0px;
                                     }
                                     QScrollBar::handle:vertical {
                                        background-color: """ + handle_color + """;
                                        min-height: 30px;
                                     }
                                     QScrollBar::handle:vertical:hover {
                                        background-color: """ + deep_white_color + """;
                                     }
                                     QScrollBar::handle:vertical:pressed {
                                        background-color: """ + light_gray_color + """;
                                     }
                                     QScrollBar::sub-line:vertical {
                                        border-left: 2px solid black;
                                        background-color: """ + button_color + """;
                                        height: 15px;
                                        subcontrol-position: top;
                                        subcontrol-origin: margin;
                                     }
                                     QScrollBar::sub-line:vertical:hover {
                                        background-color: """ + deep_white_color + """;
                                     }
                                     QScrollBar::sub-line:vertical:pressed {
                                        background-color: """ + light_gray_color + """;
                                     }
                                     QScrollBar::add-line:vertical {
                                        border-left: 2px solid black;
                                        background-color: """ + button_color + """;
                                        height: 15px;
                                        subcontrol-position: bottom;
                                        subcontrol-origin: margin;
                                     }
                                     QScrollBar::add-line:vertical:hover {
                                        background-color: """ + deep_white_color + """;
                                     }
                                     QScrollBar::add-line:vertical:pressed { 
                                        background-color: """ + light_gray_color + """;
                                     }
                                     QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                        background: none;
                                     }
                                     QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                        background: none;
                                     }
                                     """)
        self.next_button = Button('Next',
                                  self.button_w,
                                  self.button_h,
                                  self.next,
                                  color=white_color,
                                  hover_color=handle_color,
                                  pressed_color=handle_pressed_color,
                                  font_size=self.size_handler.font_size,
                                  font_color="black",
                                  is_icon=True,
                                  icon=IMAGE_NEXT)
        self.previous_button = Button('Previous',
                                      self.button_w,
                                      self.button_h,
                                      self.previous,
                                      color=white_color,
                                      hover_color=handle_color,
                                      pressed_color=handle_pressed_color,
                                      font_size=self.size_handler.font_size,
                                      font_color="black",
                                      is_icon=True,
                                      icon=IMAGE_PREVIOUS)
        self.play_button = ButtonTwoState('PLAY', 'STOP',
                                          self.button_w,
                                          self.button_h,
                                          self.play,
                                          self.stop,
                                          color=white_color,
                                          hover_color=handle_color,
                                          pressed_color=handle_pressed_color,
                                          font_size=self.size_handler.font_size,
                                          font_color=white_color,
                                          is_icon=True,
                                          icon_default=IMAGE_PLAY_BLANK,
                                          icon_pressed=IMAGE_STOP_BLANK)
        self.pause_button = ButtonTwoState('PAUSE', 'RESUME',
                                           self.button_w,
                                           self.button_h,
                                           self.pause,
                                           self.resume,
                                           color=white_color,
                                           hover_color=handle_color,
                                           pressed_color=handle_pressed_color,
                                           font_size=self.size_handler.font_size,
                                           font_color=white_color,
                                           is_icon=True,
                                           icon_default=IMAGE_PAUSE_BLANK,
                                           icon_pressed=IMAGE_PLAY_BLANK)
        self.progress_bar = Slider(self.widget_w, self.label_h, 0, 100)
        self.progress_bar.valueChanged.connect(self.play_at_current_time)
        self.progress_bar_timer = QTimer()
        self.progress_bar_timer.timeout.connect(self.update_progress_bar)
        self.pre_progress_bar_value = 0
        self.time_is_adjusted = False

        self.current_time = 0
        self.current_time_label = QLabel(self)
        self.current_time_label.setFixedWidth(self.label_w)
        self.current_time_label.setFixedHeight(self.label_h)
        self.current_time_label.setText('0:00')
        self.current_time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.current_time_label.setStyleSheet(self.label_style)
        self.music_length_label = QLabel(self)
        self.music_length_label.setFixedWidth(self.label_w)
        self.music_length_label.setFixedHeight(self.label_h)
        self.music_length_label.setText('0:00')
        self.music_length_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.music_length_label.setStyleSheet(self.label_style)

        self.layout_player = QVBoxLayout()
        self.layout_player.addWidget(self.song_list, alignment=Qt.AlignTop)
        self.layout_player_bar = QHBoxLayout()
        self.layout_player_bar.addWidget(self.current_time_label, alignment=Qt.AlignRight)
        self.layout_player_bar.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        self.layout_player_bar.addWidget(self.music_length_label, alignment=Qt.AlignLeft)
        self.layout_player.addStretch(1)
        self.layout_player.addItem(self.layout_player_bar)
        self.layout_player.addStretch(1)
        self.layout_player_button = QHBoxLayout()
        self.layout_player_button.addWidget(self.previous_button)
        self.layout_player_button.addWidget(self.play_button)
        self.layout_player_button.addWidget(self.pause_button)
        self.layout_player_button.addWidget(self.next_button)
        self.layout_player.addItem(self.layout_player_button)
        self.widget_player = QWidget()
        self.widget_player.setFixedWidth(self.widget_w * 1.2)
        self.widget_player.setFixedHeight(self.widget_h)
        self.widget_player.setStyleSheet(self.widget_style)
        self.widget_player.setLayout(self.layout_player)

        self.layout.addWidget(self.widget_convertor, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addStretch(1)
        self.layout.addWidget(self.widget_player, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.setLayout(self.layout)

    def create_item(self, name, icon, parent):
        item = QListWidgetItem(parent)
        item.setText(name)
        item.setIcon(QIcon(icon))
        item.setStatusTip(name)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    def get_info_and_icon_files(self):
        info_files = [f for f in listdir(os.getcwd() + self.info_root) if isfile(join(os.getcwd() + self.info_root, f))]
        icon_files = [f for f in listdir(os.getcwd() + self.icon_root) if isfile(join(os.getcwd() + self.icon_root, f))]
        mp3_files = [f for f in listdir(os.getcwd() + self.mp3_root) if isfile(join(os.getcwd() + self.mp3_root, f))]
        info_cnt = len(info_files)
        icon_cnt = len(icon_files)
        mp3_cnt = len(mp3_files)
        if mp3_cnt < info_cnt:
            pop_cnt = info_cnt - mp3_cnt
            info_files = info_files[:info_cnt - pop_cnt]
            icon_files = icon_files[:icon_cnt - pop_cnt]
        return info_files, icon_files, mp3_cnt

    def update_list_widget(self):
        info_files, icon_files, mp3_cnt = self.get_info_and_icon_files()
        self.mp3_max_cnt = mp3_cnt
        for info_file, icon_file in zip(info_files, icon_files):
            info_file = os.getcwd() + self.info_root + '/' + info_file
            icon_file = os.getcwd() + self.icon_root + '/' + icon_file
            f = open(info_file, 'r', encoding='UTF-8')
            content = f.read()
            content = content.splitlines()
            self._list_items.append(self.create_item(content[0],
                                                     icon_file,
                                                     self.song_list))

        self.song_list.setCurrentRow(0)
        self.song_list.setViewMode(QListView.ListMode)
        self.song_list.setSpacing(1)
        self.song_list.setItemAlignment(Qt.AlignCenter)
        self.song_list.setEnabled(True)
        self.song_list.setIconSize(QSize(128, 72))

    def init_list(self):
        self.song_list.clear()
        self.update_list_widget()

    def add_songs(self):
        self.song_list.clear()
        self.update_list_widget()
        self.player.add_songs()

    def play(self, start=0):
        self.player.set()
        m = str(int(self.player.music_length // 60))
        s = str(int(self.player.music_length % 60)).zfill(2)
        self.music_length_label.setText(m + ':' + s)
        self.progress_bar.setMaximum(self.player.music_length)
        self.progress_bar_timer.start(1000)
        self.player.play(start)

    def stop(self):
        self.current_time = 0
        self.pre_progress_bar_value = 0
        self.time_is_adjusted = False
        self.current_time_label.setText('0:00')
        self.music_length_label.setText('0:00')
        self.progress_bar.setValue(0)
        self.progress_bar_timer.stop()
        self.player.stop()
        print("stop finish")

    def pause(self):
        self.progress_bar_timer.stop()
        self.player.pause()

    def resume(self):
        self.progress_bar_timer.start(1000)
        self.player.resume()

    def previous(self):
        self.stop()

        if self.mp3_max_cnt == 0:
            return

        self.song_list.currentItem().setSelected(False)

        row = self.song_list.currentIndex().row() - 1
        if row < 0:
            row = 0

        self.song_list.setCurrentItem(self.song_list.item(row))
        self.song_list.currentItem().setSelected(True)

        self.play()

    def next(self):
        self.stop()

        if self.mp3_max_cnt == 0:
            return

        self.song_list.currentItem().setSelected(False)

        row = self.song_list.currentIndex().row() + 1
        if row > self.mp3_max_cnt - 1:
            row = self.mp3_max_cnt - 1

        self.song_list.setCurrentItem(self.song_list.item(row))
        self.song_list.currentItem().setSelected(True)

        self.play()

    def play_at_current_time(self):
        print(self.progress_bar.value(), self.pre_progress_bar_value)
        if abs(self.progress_bar.value() - self.pre_progress_bar_value) <= 1:
            if self.time_is_adjusted:
                print("Handling Start", self.current_time, self.progress_bar.value())
                self.progress_bar.valueChanged.disconnect()
                self.time_is_adjusted = False
                cur = self.current_time
                self.progress_bar_timer.stop()
                self.player.stop()
                self.progress_bar.setValue(cur)
                # self.pre_progress_bar_value = cur - 1
                self.progress_bar_timer.start(1000)
                m = str(int(cur // 60))
                s = str(int(cur % 60)).zfill(2)
                self.current_time_label.setText(m + ':' + s)
                self.progress_bar.valueChanged.connect(self.play_at_current_time)
                self.play(cur)
            return
        else:
            if not self.time_is_adjusted:
                self.time_is_adjusted = True
                print("Set flag")
            self.progress_bar_timer.stop()
            self.current_time = self.progress_bar.value()
            m = str(int(self.current_time // 60))
            s = str(int(self.current_time % 60)).zfill(2)
            self.current_time_label.setText(m + ':' + s)
            self.progress_bar_timer.start(1000)
            print("movvvvvv")

    def update_progress_bar(self):
        self.current_time += 1
        m = str(int(self.current_time // 60))
        s = str(int(self.current_time % 60)).zfill(2)
        self.current_time_label.setText(m + ':' + s)
        self.pre_progress_bar_value = self.current_time - 1
        self.progress_bar.setValue(self.current_time)

    def set_playlist(self):
        self.playlist = self.playlist_edit.text()
        self.tot_cnt = len(Playlist(self.playlist).video_urls)

    def open_mp3_folder(self):
        path = os.path.realpath(os.getcwd() + self.mp3_root)
        if sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            os.startfile(path)

    def open_mp4_folder(self):
        path = os.path.realpath(os.getcwd() + self.mp4_root)
        if sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            os.startfile(path)

    def init_pytube(self):
        self.mp4_max_cnt = 0
        self.msg_box_pytube.clear()
        shutil.rmtree(os.getcwd() + self.mp4_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.mp4_root)
        shutil.rmtree(os.getcwd() + self.info_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.info_root)
        shutil.rmtree(os.getcwd() + self.icon_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.icon_root)

    def update_pytube_status(self):
        max_len = len(os.listdir(os.getcwd() + self.mp4_root))
        if max_len != self.mp4_max_cnt:
            f = open(os.getcwd() + self.info_root + '/' + str(max_len) + '.txt', 'r', encoding='UTF-8')
            content = f.read()
            content = content.splitlines()
            f.close
            self.msg_box_pytube.append_text(content[1] + ' ' + content[2])
            self.mp4_max_cnt = max_len

    def start_pytube(self):
        global g_pytube_trigger
        g_pytube_trigger = True

        playlist = self.playlist_edit.text()
        playlist = Playlist(playlist)

        self.init_pytube()
        self.thread_pytube = threading.Thread(target=convert_playlist,
                                              args=(playlist.video_urls,
                                                    self.mp4_root,
                                                    self.info_root,
                                                    self.icon_root,
                                                    self.extension_mp4))
        self.thread_pytube.start()
        self.timer_pytube.start(1)

    def stop_pytube(self):
        global g_pytube_trigger
        g_pytube_trigger = False
        self.thread_pytube.join()
        self.timer_pytube.stop()

    def init_pydub(self):
        self.mp3_max_cnt = 0
        self.msg_box_pydub.clear()
        shutil.rmtree(os.getcwd() + self.mp3_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.mp3_root)

    def update_pydub_status(self):
        max_len = len(os.listdir(os.getcwd() + self.mp3_root))
        if max_len != self.mp3_max_cnt:
            files = [f for f in listdir(os.getcwd() + self.mp3_root) if isfile(join(os.getcwd() + self.mp3_root, f))]
            file = files[-1]
            self.msg_box_pydub.append_text(file)
            self.mp3_max_cnt = max_len

    def start_pydub(self):
        global g_pydub_trigger
        g_pydub_trigger = True

        self.init_pydub()
        self.thread_pydub = threading.Thread(target=convert_audio, args=(self.mp4_root, self.mp3_root, self.extension_mp4, self.extension_mp3))
        self.thread_pydub.start()
        self.timer_pydub.start(1)

    def stop_pydub(self):
        global g_pydub_trigger
        g_pydub_trigger = False
        self.thread_pydub.join()
        self.timer_pydub.stop()


class Window(QMainWindow):
    def __init__(self, size, w, h):
        super().__init__()
        # Init window attribute
        self.tab_widget = None
        self.screen_size = size
        self.setWindowTitle("YT Converter")
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        icon = QIcon()
        icon.addFile(os.getcwd() + IMAGE_MET_ICON)
        self.setWindowIcon(icon)
        self.setStyleSheet("""
                           QMainWindow > QWidget { background-color: """ + gray_color + """; }
                           """)

        # New a main widget for window
        self.main = QWidget()
        self._device = None

        # Construct upper view
        self.upper_view = UpperView(self, self._device, size)
        self.bottom_view = BottomView(self, self._device, size)

        # Attach views to main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.upper_view)
        self.main_layout.addWidget(self.bottom_view)
        self.main.setLayout(self.main_layout)

        # Attach main widget to window
        self.setCentralWidget(self.main)

    def center(self, size):
        x = (size.width() - self.width()) / 2
        y = (size.height() - self.height()) / 2
        self.move(QPoint(x, y - 30))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Arial")
    app.setFont(font)

    screens = app.screens()
    if len(screens) > 1:
        screen = screens[1]
    else:
        screen = screens[0]
    geometry = screen.geometry()
    size = screen.size()

    window = Window(size, 1200, 900)
    window.center(size)
    window.showFullScreen()

    sys.exit(app.exec_())
