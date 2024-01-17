import os
from os import listdir
from os.path import isfile, join
import sys
import shutil
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

pytube_trigger = True
pydub_trigger = True


def exit_exe(self):
    sys.exit(0)


def on_progress(stream, chunk, remains):
    total = stream.filesize
    percent = int((total-remains) / total * 100)
    print('=' * percent + ' ' * (100 - percent))


def convert_playlist(urls, file_root, info_root, extension):
    cnt = 1
    tot_cnt = len(urls)
    for i in urls:
        if pytube_trigger:
            yt = YouTube(i, on_progress_callback=on_progress)
            # audio = yt.streams.filter(only_audio=True).first()

            fn = str(cnt) + ' ' + str(yt.author) + ' ' + str(yt.title) + extension
            fn = fn.replace('/', '')
            fn = fn.replace('?', '')
            fn = fn.replace('"', '')
            fn = fn.replace('～', '')
            fn = fn.replace('|', '')
            fn = fn.replace('@', '')
            print(i, fn)
            f = open(os.getcwd() + info_root + '/' + str(cnt) + '.txt', 'w', encoding='UTF-8')
            f.write(str(yt.author) + '\n')
            f.write(str(yt.title) + '\n')
            f.write(str(i) + '\n')
            f.write(str(yt.thumbnail_url) + '\n')
            f.close()
            yt.streams.filter().get_audio_only().download(output_path=os.getcwd() + file_root, filename=fn)
            # audio.download(output_path=os.getcwd() + mp4_root, filename=fn)
            cnt += 1
        else:
            break
    return


def convert_audio(mp4_root, mp3_root, extension_mp4, extension_mp3):
    extension_mp4 = extension_mp4.replace('.', '')
    extension_mp3 = extension_mp3.replace('.', '')

    for file in os.listdir(os.getcwd() + mp4_root):
        if pydub_trigger:
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
        self.window_button = ButtonTwoState('Normal', 'FullScreen',
                                            self.size_handler.button_w,
                                            self.size_handler.button_w,
                                            self.window.showMaximized,
                                            self.window.showFullScreen,
                                            color=white_color,
                                            hover_color=light_gray_color,
                                            pressed_color=gray_color,
                                            color_1=white_color,
                                            hover_color_1=light_gray_color,
                                            pressed_color_1=gray_color,
                                            font_size=self.size_handler.font_size,
                                            font_color=white_color,
                                            is_icon=True,
                                            icon_default=IMAGE_SHOW_NORMAL,
                                            icon_pressed=IMAGE_SHOW_FULL_SCREEN)

        pixmap = QPixmap(os.getcwd() + IMAGE_MET_LOGO)
        self.logo = QLabel()
        self.logo.setPixmap(pixmap)
        self.logo.show()

        self.layout.addStretch(10)
        self.layout.addWidget(self.exit_button, alignment=Qt.AlignRight)
        self.layout.addWidget(self.window_button, alignment=Qt.AlignRight)
        self.layout.addWidget(self.logo, alignment=Qt.AlignRight)
        self.setLayout(self.layout)


class BottomView(QWidget):
    def __init__(self, window, device, size):
        super().__init__()

        self.window = window
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
        self.widget_h = 850

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
                                   background-color: white; 
                                   border: 2px solid black;
                                   border-radius: 2px;
                                   font: """ + self.size_handler.font_size + """
                               }
                               """
        self.widget_style = """ 
                            QWidget  {
                                border: 2px solid black;
                                background-color: """ + deep_gray_color + """; 
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
        self.open_result_folder_button = Button('RESULT',
                                                self.button_w,
                                                self.button_h,
                                                self.open_result_folder,
                                                color=white_color,
                                                hover_color=light_gray_color,
                                                pressed_color=gray_color,
                                                font_size=self.size_handler.font_size,
                                                font_color="black",
                                                is_icon=True,
                                                icon=IMAGE_MUSIC)
        self.open_info_folder_button = Button('INFO',
                                              self.button_w,
                                              self.button_h,
                                              self.open_info_folder,
                                              color=white_color,
                                              hover_color=light_gray_color,
                                              pressed_color=gray_color,
                                              font_size=self.size_handler.font_size,
                                              font_color="black",
                                              is_icon=True,
                                              icon=IMAGE_ATTACHED_FILES)
        self.msg_box_pytube = MessageBox(self.size_handler.msg_w / 2,
                                         self.size_handler.msg_h,
                                         color=light_gray_color,
                                         font_size=self.size_handler.msg_font_size,
                                         font_color=black_color)
        self.msg_box_pydub = MessageBox(self.size_handler.msg_w / 2,
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
                                             hover_color=light_gray_color,
                                             pressed_color=white_color,
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
                                            hover_color=light_gray_color,
                                            pressed_color=white_color,
                                            font_size=self.size_handler.font_size,
                                            font_color=white_color,
                                            is_icon=True,
                                            icon_default=IMAGE_EXPORT,
                                            icon_pressed=IMAGE_STOP)

        self.thread_pytube = None
        self.timer_pytube = QTimer()
        self.timer_pytube.timeout.connect(self.update_pytube_status)
        self.mp4_root = '/Music/MP4'
        self.mp3_root = '/Music/MP3'
        self.info_root = '/Info'
        self.extension_mp4 = '.mp4'
        self.extension_mp3 = '.mp3'

        self.mp4_max_cnt = 0
        self.mp3_max_cnt = 0
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
        self.layout_convertor.addItem(self.layout_playlist)
        self.layout_msg_box = QHBoxLayout()
        self.layout_msg_box.addWidget(self.msg_box_pytube)
        self.layout_msg_box.addWidget(self.msg_box_pydub)
        self.layout_convertor.addItem(self.layout_msg_box)
        self.layout_convertor_button = QHBoxLayout()
        self.layout_convertor_button.addWidget(self.convert_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.open_info_folder_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.open_result_folder_button, alignment=Qt.AlignCenter)
        self.layout_convertor_button.addWidget(self.export_button, alignment=Qt.AlignCenter)
        self.layout_convertor.addItem(self.layout_convertor_button)
        self.widget_convertor = QWidget()
        self.widget_convertor.setFixedWidth(self.widget_w)
        self.widget_convertor.setFixedHeight(self.widget_h)
        self.widget_convertor.setStyleSheet(self.widget_style)
        self.widget_convertor.setLayout(self.layout_convertor)

        self.player = MusicPlayer(self.mp4_root)
        self.next_button = Button('Next',
                                  self.button_w,
                                  self.button_h,
                                  self.player.Previous,
                                  color=white_color,
                                  hover_color=light_gray_color,
                                  pressed_color=white_color,
                                  font_size=self.size_handler.font_size,
                                  font_color="black",
                                  is_icon=True,
                                  icon=IMAGE_NEXT)
        self.previous_button = Button('Previous',
                                      self.button_w,
                                      self.button_h,
                                      self.player.Next,
                                      color=white_color,
                                      hover_color=light_gray_color,
                                      pressed_color=white_color,
                                      font_size=self.size_handler.font_size,
                                      font_color="black",
                                      is_icon=True,
                                      icon=IMAGE_PREVIOUS)
        self.play_button = ButtonTwoState('PLAY', 'PAUSE',
                                          self.button_w,
                                          self.button_h,
                                          self.player.Play,
                                          self.player.Stop,
                                          color=white_color,
                                          hover_color=light_gray_color,
                                          pressed_color=white_color,
                                          font_size=self.size_handler.font_size,
                                          font_color=white_color,
                                          is_icon=True,
                                          icon_default=IMAGE_PLAY_BLANK,
                                          icon_pressed=IMAGE_PAUSE_BLANK)

        self.layout_player = QVBoxLayout()
        self.layout_player_button = QHBoxLayout()
        self.layout_player_button.addWidget(self.previous_button)
        self.layout_player_button.addWidget(self.play_button)
        self.layout_player_button.addWidget(self.next_button)
        self.layout_player.addItem(self.layout_player_button)
        self.widget_player = QWidget()
        self.widget_player.setFixedWidth(self.widget_w)
        self.widget_player.setFixedHeight(self.widget_h)
        self.widget_player.setStyleSheet(self.widget_style)
        self.widget_player.setLayout(self.layout_player)

        self.layout.addWidget(self.widget_convertor)
        self.layout.addWidget(self.widget_player)
        self.setLayout(self.layout)

    def open_result_folder(self):
        path = os.path.realpath(os.getcwd() + self.mp3_root)
        if sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            os.startfile(path)

    def open_info_folder(self):
        path = os.path.realpath(os.getcwd() + self.info_root)
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

    def update_pytube_status(self):
        max_len = len(os.listdir(os.getcwd() + self.mp4_root))
        if max_len != self.mp4_max_cnt:
            f = open(os.getcwd() + self.info_root + '/' + str(max_len) + '.txt', 'r', encoding='UTF-8')
            content = f.read()
            content = content.splitlines()
            f.close
            self.msg_box_pytube.append_text(content[0] + ' ' + content[1])
            self.mp4_max_cnt = max_len

    def start_pytube(self):
        global pytube_trigger
        pytube_trigger = True

        playlist = 'https://youtube.com/playlist?list=PLFdgdNMl_r3Ks7Au7SFJiRaMXwWrdikxR&si=ejV4p3yJ2QZpbaW4'
        # playlist = self.playlist_edit.text()
        playlist = Playlist(playlist)

        self.init_pytube()
        self.thread_pytube = threading.Thread(target=convert_playlist,
                                              args=(playlist.video_urls, self.mp4_root, self.info_root, self.extension_mp4))
        self.thread_pytube.start()
        self.timer_pytube.start(1)

    def stop_pytube(self):
        global pytube_trigger
        pytube_trigger = False
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
        global pydub_trigger
        pydub_trigger = True

        self.init_pydub()
        self.thread_pydub = threading.Thread(target=convert_audio, args=(self.mp4_root, self.mp3_root, self.extension_mp4, self.extension_mp3))
        self.thread_pydub.start()
        self.timer_pydub.start(1)

    def stop_pydub(self):
        global pydub_trigger
        pydub_trigger = False
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
                           QMainWindow > QWidget { background-color: """ + deep_white_color + """; }
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
