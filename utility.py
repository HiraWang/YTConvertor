import os
import time
import numpy as np
import multiprocessing
from PySide2.QtGui import QMovie
from PySide2.QtCore import Qt, QThread, Signal
from PySide2.QtWidgets import QLabel, QDialog, QVBoxLayout

UPPER_VIEW = 0
BOTTOM_VIEW = 1
CONSOLE_VIEW = 2

IMAGE_ATTACHED_FILES = "./images/AttachedFiles.png"
IMAGE_CLOSE = "./images/Close.png"
IMAGE_EXIT = "./images/Exit.png"
IMAGE_IMAGE = "./images/Image.png"
IMAGE_MUSIC = "./images/Music.png"
IMAGE_LOADING = "./images/Loading.gif"
IMAGE_MET_ICON_FULL = "/images/met_icon.jpg"
IMAGE_MET_ICON = "/images/eruhi_icon.png"
IMAGE_MET_LOGO = "/images/eruhi_logo.png"
IMAGE_PAUSE = "./images/Pause.png"
IMAGE_POWER = "./images/Power.png"
IMAGE_SCAN = "./images/Scan.png"
IMAGE_SHOW_FULL_SCREEN = "./images/ShowFullScreen.png"
IMAGE_SHOW_NORMAL = "./images/ShowNormal.png"
IMAGE_START = "./images/Start.png"
IMAGE_STOP = "./images/Stop.png"
IMAGE_MENU = "./images/Menu.png"
IMAGE_SETTING = "./images/Setting.png"
IMAGE_PLAY_BLANK = "./images/StartBlank.png"
IMAGE_STOP_BLANK = "./images/StopBlank.png"
IMAGE_PAUSE_BLANK = "./images/PauseBlank.png"
IMAGE_NEXT = "./images/Next.png"
IMAGE_PREVIOUS = "./images/Previous.png"
IMAGE_EXPORT = "./images/Export.png"

CONSOLE_PERIOD_MAX = 5000
MONITOR_Q_TIMER_PERIOD = 25
MONITOR_CHUNKS_PER_SCENE = 5
MONITOR_OFFSET = 64
BUF_SIZE = 4096
# MONITOR_SIGNAL_LEN = MONITOR_CHUNKS_PER_SCENE * BUF_SIZE // MONITOR_OFFSET


class SizeHandler():
    def __init__(self, view, size):
        if size.width() == 1920:
            self.scale = 1
            self.msg_scale = 1
            self.label_scale = 0.8
            self.edit_box_scale = 1
            self.stretch_scale = 1
            self.section_scale = 1
        else:
            self.scale = np.float32(size.width() / 1920.0) * 0.8
            self.msg_scale = np.float32(size.width() / 1920.0)
            self.label_scale = 1
            self.edit_box_scale = np.float32(size.width() / 1920.0)
            self.stretch_scale = 0.1
            self.section_scale = 0.7
        self.lcd_scale = 1

        if self.scale == 1:
            self.font_size = "20px"
            self.msg_font_size = "16px"
            self.set_btn_font_size = "28px"
            self.confirm_btn_font_size = "24px"
            self.tree_section_font_size = "22px"
            self.plot_title_size = "24px"
            self.lcd_font_size = "24px"
            self.ver_font_size = "20px"
        else:
            self.font_size = "12px"
            self.msg_font_size = "8px"
            self.set_btn_font_size = "14px"
            self.confirm_btn_font_size = "12px"
            self.tree_section_font_size = "11px"
            self.plot_title_size = "12px"
            self.lcd_font_size = "12px"
            self.ver_font_size = "7px"

        if view == UPPER_VIEW:
            print("[INFO] Upper View UI Scale: ", self.scale)
            self.button_w = 80 * self.scale
            self.button_h = 25
            self.label_w = 57
            self.label_h = 25 * self.scale
            self.version_w = 60 * self.scale
            self.version_h = 20 * self.scale
        elif view == BOTTOM_VIEW:
            print("[INFO] Bottom View UI Scale: ", self.scale)
            self.width = 100
            self.height = 50
            self.label_w = self.width * 0.5 * self.scale
            self.label_h = self.height * self.scale
            self.valve_label_w = (self.width + 20) * self.scale
            self.valve_label_h = self.height * self.scale
            self.msg_w = 390 * self.scale
            self.msg_h = 550 * self.msg_scale
            self.edit_w = self.width * 5.2 * self.scale
            self.edit_h = (self.height - 10) * self.scale
            self.message_box_w = (self.width * 3) * self.scale
            self.message_box_h = self.height * self.msg_scale
            self.unit_w = 160 * self.scale
            self.unit_h = self.height * self.scale
            self.button_w = self.width * self.scale
            self.button_h = self.height * 2 * self.scale
            self.switch_r = 20 * self.scale
            self.switch_w = 60 * self.scale
            self.switch_max_w = 66 * self.scale
            self.switch_max_h = 55 * self.scale
            self.section_w_1 = 190 * self.section_scale
            self.section_w_2 = 150 * self.section_scale
            self.border_radius = 7
            self.valve_widget_w = self.width * 3.3 * self.scale
            self.fluid_widget_w = (self.label_w + self.edit_w + self.unit_w) * 1.5


class ThreadProcessHandler(QThread):
    def __init__(self, process):
        super().__init__()
        self.stopped = False
        self._process = process

    def run(self):
        if not self._process.is_alive():
            return
        self._process.join()
        time.sleep(1)


class ThreadSignalProcessor(QThread):
    signal = Signal(object)

    def __init__(self,
                 parameters):
        super().__init__()
        self.rn = parameters[0]
        self.fn = parameters[1]
        self.scan_uid = parameters[2]
        self.date_edit = parameters[3]
        self.experiment_title_edit = parameters[4]
        self.device_edit = parameters[5]
        self.sample_edit = parameters[6]
        self.pulse_edit = parameters[7]
        self.flow_rate_edit = parameters[8]
        self.sample_cnt_tot = parameters[9]
        self.extension = parameters[10]
        self.buf_len = parameters[11]
        self.peak_data = []

    def run(self):
        print("[INFO] Start to do signal recording")
        name = self.rn + str(self.scan_uid) + "_ori" + ".csv"
        if os.path.isfile(name):
            print("[INFO] final log file already exist, return now")
            return

        buf_all = []
        fp = open(name, "w")
        for i in range(self.sample_cnt_tot // self.buf_len):
            name = self.fn + str(i) + self.extension
            buf = np.load(name)
            buf_all.extend(buf)
            for j in range(len(buf)):
                fp.write("{:.3f}\n".format(np.float32(buf[j]) / 4095.0 * 3.3))
        fp.close()

        print("[INFO] Start to do signal processing")
        name = self.rn + str(self.scan_uid) + ".csv"
        if os.path.isfile(name):
            print("[INFO] final log file already exist, return now")
            return

        fp = open(name, "w")
        fp.write("Date:,," + self.date_edit.text() + "\n")
        fp.write("Experiment Title:,," + self.experiment_title_edit.text() + "\n")
        fp.write("Device:,," + self.device_edit.text() + "\n")
        fp.write("Sample:,," + self.sample_edit.text() + "\n")
        fp.write("Pulse:,," + self.pulse_edit.text() + "\n")
        fp.write("Flow Rate:,," + self.flow_rate_edit.text() + "\n")
        fp.write("\n")
        fp.write("signal, peak, pulse width, period\n")

        period = get_signal_period(buf_all)
        if period == 0:
            print("invalid period, will not do the following processing")
            fp.close()
            return

        tmp = np.zeros(period)
        print("[INFO] Period: ", period)
        print("[INFO] Samples: ", len(buf_all))

        for j in range(len(buf_all)):
            tmp[j % period] = buf_all[j] / 4095.0 * 3.3
            if (j % period) == (period - 1):
                peak = np.max(tmp)
                tmp_pos = np.where((tmp - np.mean(tmp)) > 0)
                pulse_width = len(tmp_pos[0]) + 1
                self.peak_data.append(peak)
                fp.write("{:.3f}, {}, {}, {}\n".format(np.float32(buf_all[j]), peak, pulse_width, period))
        fp.close()

        self.signal.emit(self.peak_data)
        return


def add_loading_gif_for_process(self, msg_type, name, func, parameter):
    dialog = QDialog(self, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
    dialog.setWindowTitle(msg_type)
    vbox = QVBoxLayout()
    msg = QLabel(self)
    msg.setText(name)
    msg.setStyleSheet("font: 20px")
    label = QLabel(self)
    label.setAlignment(Qt.AlignCenter)
    loading = QMovie(IMAGE_LOADING)
    label.setMovie(loading)
    loading.start()
    vbox.addWidget(msg, alignment=Qt.AlignCenter)
    vbox.addWidget(label)
    dialog.setLayout(vbox)

    p = multiprocessing.Process(target=func, args=parameter)
    p.start()
    thread = ThreadProcessHandler(p)
    thread.finished.connect(dialog.close)
    thread.start()
    dialog.exec()


def add_loading_gif_for_post_process(self, msg_type, name, func, parameter):
    dialog = QDialog(self, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
    dialog.setWindowTitle(msg_type)
    vbox = QVBoxLayout()
    msg = QLabel(self)
    msg.setText(name)
    msg.setStyleSheet("font: 20px")
    label = QLabel(self)
    label.setAlignment(Qt.AlignCenter)
    loading = QMovie(IMAGE_LOADING)
    label.setMovie(loading)
    loading.start()
    vbox.addWidget(msg, alignment=Qt.AlignCenter)
    vbox.addWidget(label)
    dialog.setLayout(vbox)

    thread = ThreadSignalProcessor(parameter)
    thread.signal.connect(func)
    thread.finished.connect(thread.deleteLater)
    thread.finished.connect(dialog.close)
    thread.finished.connect(dialog.deleteLater)
    thread.start()
    dialog.exec()


def get_signal_period(signal):
    signal = np.array(signal, dtype=float)
    signal -= np.mean(signal)
    fourier = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size)
    mags = abs(fourier)
    signal_freq = freq[mags.argmax()]
    if signal_freq == 0:
        return 0
    else:
        return int(1.0 / signal_freq) + 1
