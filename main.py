import os
import sys
import shutil
import threading
import subprocess
from pytube import Playlist, YouTube
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from utility import *
from ui_unit import *

trigger = True


def exit_exe(self):
    sys.exit(0)


def convert_playlist(urls, file_root, info_root):
    cnt = 1
    tot_cnt = len(urls)
    for i in urls:
        if trigger:
            yt = YouTube(i)
            fn = str(cnt) + ' ' + str(yt.author) + ' ' + str(yt.title) + '.mp3'
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
            cnt += 1
        else:
            break


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
        self.window_button = ButtonTwoState('FullScreen', 'Normal',
                                            self.size_handler.button_w,
                                            self.size_handler.button_w,
                                            self.window.showFullScreen,
                                            self.window.showMaximized,
                                            color=white_color,
                                            hover_color=light_gray_color,
                                            pressed_color=gray_color,
                                            color_1=white_color,
                                            hover_color_1=light_gray_color,
                                            pressed_color_1=gray_color,
                                            font_size=self.size_handler.font_size,
                                            font_color=white_color,
                                            is_icon=True,
                                            icon_default=IMAGE_SHOW_FULL_SCREEN,
                                            icon_pressed=IMAGE_SHOW_NORMAL)

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
        self.qwidget_style = """ 
                             QWidget  {
                                 border: 2px solid black;
                                 background-color: """ + light_gray_color + """; 
                                 border-radius: 10px;
                             }
                             """
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
                                                self.button_w + 20,
                                                self.button_h,
                                                self.open_result_folder,
                                                color=white_color,
                                                hover_color=light_gray_color,
                                                pressed_color=gray_color,
                                                font_size=self.size_handler.font_size,
                                                font_color="black",
                                                is_icon=True,
                                                icon=IMAGE_MUSIC)
        self.open_info_folder_button = Button('RESULT',
                                              self.button_w + 20,
                                              self.button_h,
                                              self.open_info_folder,
                                              color=white_color,
                                              hover_color=light_gray_color,
                                              pressed_color=gray_color,
                                              font_size=self.size_handler.font_size,
                                              font_color="black",
                                              is_icon=True,
                                              icon=IMAGE_ATTACHED_FILES)
        self.msg_box = MessageBox(self.size_handler.msg_w,
                                  self.size_handler.msg_h,
                                  color=light_gray_color,
                                  font_size=self.size_handler.msg_font_size,
                                  font_color=black_color)
        self.convert_button = ButtonTwoState('CONVERT', 'STOP',
                                             self.button_w,
                                             self.button_h,
                                             self.start,
                                             self.stop,
                                             color=white_color,
                                             hover_color=light_gray_color,
                                             pressed_color=gray_color,
                                             font_size=self.size_handler.font_size,
                                             font_color=white_color,
                                             is_icon=True,
                                             icon_default=IMAGE_SCAN,
                                             icon_pressed=IMAGE_STOP)

        self.thread = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.file_root = '/Music'
        self.info_root = '/Info'

        self.max_len = 0
        self.yt_title = []
        self.yt_author = []
        self.yt_thumbnail_url = []

        self.layout_playlist = QHBoxLayout()
        self.layout_playlist.addWidget(self.playlist_label)
        self.layout_playlist.addWidget(self.playlist_edit)

        self.layout = QVBoxLayout()
        self.layout.addItem(self.layout_playlist)
        self.layout.addWidget(self.msg_box, alignment=Qt.AlignCenter)
        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.convert_button, alignment=Qt.AlignCenter)
        self.layout_button.addWidget(self.open_info_folder_button, alignment=Qt.AlignCenter)
        self.layout_button.addWidget(self.open_result_folder_button, alignment=Qt.AlignCenter)
        self.layout.addItem(self.layout_button)
        self.setLayout(self.layout)

    def open_result_folder(self):
        path = os.path.realpath(os.getcwd() + self.file_root)
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

    def init(self):
        self.max_len = 0
        self.msg_box.clear()
        shutil.rmtree(os.getcwd() + self.file_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.file_root)
        shutil.rmtree(os.getcwd() + self.info_root, ignore_errors=True)
        os.mkdir(os.getcwd() + self.info_root)

    def update_status(self):
        max_len = len(os.listdir(os.getcwd() + self.file_root))
        if max_len != self.max_len:
            f = open(os.getcwd() + self.info_root + '/' + str(max_len) + '.txt', 'r', encoding='UTF-8')
            content = f.read()
            content = content.splitlines()
            f.close
            self.msg_box.append_text(content[0] + ' ' + content[1])
            self.max_len = max_len

    def start(self):
        global trigger
        trigger = True

        playlist = 'https://youtube.com/playlist?list=PLFdgdNMl_r3Ks7Au7SFJiRaMXwWrdikxR&si=ejV4p3yJ2QZpbaW4'
        # playlist = self.playlist_edit.text()
        playlist = Playlist(playlist)

        self.init()
        self.thread = threading.Thread(target=convert_playlist, args=(playlist.video_urls, self.file_root, self.info_root))
        self.thread.start()
        self.timer.start(1)

    def stop(self):
        global trigger
        trigger = False
        self.thread.join()
        self.timer.stop()


class Window(QMainWindow):
    def __init__(self, size):
        super().__init__()
        # Init window attribute
        self.tab_widget = None
        self.screen_size = size
        self.setWindowTitle("YT Convertor")
        icon = QIcon()
        icon.addFile(os.getcwd() + IMAGE_MET_ICON)
        self.setWindowIcon(icon)
        self.setStyleSheet("""
                           QMainWindow > QWidget { background-color: """ + deep_gray_color + """; }
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

    window = Window(size)
    window.move(geometry.left(), geometry.top())
    window.showMaximized()

    sys.exit(app.exec_())
