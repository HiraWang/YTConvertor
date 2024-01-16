from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

white_color = "#ffffff"
gray_color = "rgb(145, 145, 145)"
black_color = "rgb(0, 0, 0)"

light_black_color = "rgb(70, 70, 70)"
light_gray_color = "rgb(200, 200, 200)"

deep_white_color = "rgb(240, 240, 240)"
deep_gray_color = "rgb(90, 90, 90)"

button_color = "#36c7c9"
button_hover_color = "rgb(47, 175, 178)"
button_pressed_color = "#24878a"
pressed_button_color = "#e3170d"
pressed_button_hover_color = "#cb150c"
pressed_button_pressed_color = "#b8130b"

pulse_color = "#a6ffffd9"

handle_color = "#2a2a2a"
handle_hover_color = "#0066cc"
handle_pressed_color = "#0059b3"
widget_background_color = "#ccffff"


class Button(QPushButton):
    def __init__(self,
                 name,
                 w,
                 h,
                 callback_default=None,
                 color: str = button_color,
                 hover_color: str = button_hover_color,
                 pressed_color: str = button_pressed_color,
                 font_size: str = "20px",
                 font_color: str = black_color,
                 is_icon: bool = False,
                 icon: str = None):
        super().__init__()
        self.name = name
        self.info_default = """
                            QPushButton {
                                background-color: """ + color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            QPushButton:hover {
                                background-color: """ + hover_color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """                                
                            }
                            QPushButton:pressed {
                                background-color: """ + pressed_color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            """
        self.callback_default = callback_default
        if is_icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(w, h))
        else:
            self.setText(name)
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setStyleSheet(self.info_default)
        self.status = False
        self.clicked.connect(self.callback_default)


class ButtonTwoState(QPushButton):
    def __init__(self,
                 name_default,
                 name_pressed,
                 w,
                 h,
                 callback_default=None,
                 callback_pressed=None,
                 color: str = button_color,
                 hover_color: str = button_hover_color,
                 pressed_color: str = button_pressed_color,
                 color_1: str = pressed_button_color,
                 hover_color_1: str = pressed_button_hover_color,
                 pressed_color_1: str = pressed_button_pressed_color,
                 font_size: str = "20px",
                 font_color: str = black_color,
                 is_icon: bool = False,
                 icon_default: str = None,
                 icon_pressed: str = None):
        super().__init__()
        self.name_default = name_default
        self.name_pressed = name_pressed
        self.icon_default = icon_default
        self.icon_pressed = icon_pressed
        self.is_icon = is_icon
        self.w = w
        self.h = h
        self.info_default = """
                            QPushButton {
                                background-color: """ + color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            QPushButton:hover {
                                background-color: """ + hover_color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            QPushButton:pressed {
                                background-color: """ + pressed_color + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            """
        self.info_pressed = """
                            QPushButton {
                                background-color: """ + color_1 + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            QPushButton:hover {
                                background-color: """ + hover_color_1 + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            QPushButton:pressed {
                                background-color: """ + pressed_color_1 + """; 
                                border: 2px solid black;
                                border-radius: 5px;
                                font: bold """ + font_size + """;
                                color: """ + font_color + """
                            }
                            """
        self.callback_default = callback_default
        self.callback_pressed = callback_pressed
        if self.is_icon:
            self.setIcon(QIcon(self.icon_default))
            self.setIconSize(QSize(self.w, self.w))
        else:
            self.setText(name_default)
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setStyleSheet(self.info_default)
        self.status = False
        self.clicked.connect(self.toggle_button)

    def toggle_button(self):
        if self.status:
            self.button_status_set_false()
            if self.callback_pressed is not None:
                self.callback_pressed()
        else:
            self.button_status_set_true()
            if self.callback_default is not None:
                self.callback_default()

    def button_status_set_false(self):
        self.status = False
        if self.is_icon:
            self.setIcon(QIcon(self.icon_default))
            self.setIconSize(QSize(self.w, self.w))
        else:
            self.setText(self.name_default)
        self.setStyleSheet(self.info_default)

    def button_status_set_true(self):
        self.status = True
        if self.is_icon:
            self.setIcon(QIcon(self.icon_pressed))
            self.setIconSize(QSize(self.w, self.w))
        else:
            self.setText(self.name_pressed)
        self.setStyleSheet(self.info_pressed)


class MessageBox(QPlainTextEdit):
    def __init__(self, w, h, color: str = white_color, font_size: str = "16px", font_color: str = black_color):
        super().__init__()
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setReadOnly(True)
        self.info = """
                    QPlainTextEdit  {
                        background-color: """ + color + """; 
                        border: 2px solid black;
                        border-radius: 5px;
                        font: """ + font_size + """;
                        color: """ + font_color + """;
                    }
                    """
        self.setStyleSheet(self.info)

    def update_text(self, text: str):
        self.clear()
        self.appendPlainText(text)

    def append_text(self, text: str):
        self.appendPlainText(text)


class Slider(QSlider):
    def __init__(self, w, h, min, max):
        super().__init__()
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(0)
        self.setOrientation(Qt.Horizontal)
        self.info = """
                    QWidget  {
                        border: 0px solid black;
                    }
                    QSlider::groove:horizontal  {
                        border: 2px solid """ + str(black_color) + """;
                        height: 10px;
                    }
                    QSlider::handle:horizontal  {
                        background: """ + str(handle_color) + """;
                        width: 10px;
                        margin: -12px -1px;
                        border-radius: 1px;
                    }
                    QSlider::add-page:horizontal  {
                        background: qlineargradient(0, 0, 0, 1, 0, #B1B1B1, 1, #c4c4c4);
                    }
                    QSlider::sub-page:horizontal  {
                        background: """ + str(handle_hover_color) + """;
                    }
                    QSlider::handle:horizontal:hover  {
                        background: """ + str(handle_hover_color) + """;
                    }
                    """
        self.setStyleSheet(self.info)
        self.setTickPosition(QSlider.TicksBelow)


class RangeSlider(QWidget):
    def __init__(self, edit_1, edit_2, interval: int = 1, parent=None, w: int = 600):
        super().__init__(parent)

        self.first_sc = None
        self.second_sc = None
        self.first_position = 0
        self.second_position = 1
        self.offset = 5
        self.edit_1 = edit_1
        self.edit_2 = edit_2

        self.opt = QStyleOptionSlider()
        self.opt.minimum = 0
        self.opt.maximum = 10

        self.setTickPosition(QSlider.TicksAbove)
        self.setTickInterval(interval)
        self.setFixedWidth(w)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed, QSizePolicy.Slider)
        )

    def setRangeLimit(self, minimum: int, maximum: int):
        self.opt.minimum = minimum
        self.opt.maximum = maximum

    def setRange(self, start: int, end: int):
        self.first_position = start
        self.second_position = end

    def getRange(self):
        return self.first_position, self.second_position

    def setTickPosition(self, position: QSlider.TickPosition):
        self.opt.tickPosition = position

    def setTickInterval(self, ti: int):
        self.opt.tickInterval = ti

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        # Draw rule
        self.opt.initFrom(self)
        self.opt.rect = self.rect()
        self.opt.sliderPosition = 0
        self.opt.subControls = QStyle.SC_SliderGroove | QStyle.SC_SliderTickmarks

        # Draw groove
        self.style().drawComplexControl(QStyle.CC_Slider, self.opt, painter)

        # Draw interval
        color = self.palette().color(QPalette.Highlight)
        color.setNamedColor("#2a2a2a")
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)

        self.opt.sliderPosition = self.first_position
        x_left_handle = (
            self.style()
                .subControlRect(QStyle.CC_Slider, self.opt, QStyle.SC_SliderHandle)
                .right()
        )

        self.opt.sliderPosition = self.second_position
        x_right_handle = (
            self.style()
                .subControlRect(QStyle.CC_Slider, self.opt, QStyle.SC_SliderHandle)
                .left()
        )

        groove_rect = self.style().subControlRect(
            QStyle.CC_Slider, self.opt, QStyle.SC_SliderGroove
        )

        selection = QRect(
            x_left_handle - self.offset,
            groove_rect.y() + self.offset,
            x_right_handle - x_left_handle + self.offset * 2.5,
            groove_rect.height() - self.offset * 1.2,
        ).adjusted(-1, 1, 1, -1)

        painter.drawRect(selection)

        # Draw first handle
        self.opt.subControls = QStyle.SC_SliderHandle
        self.opt.sliderPosition = self.first_position
        self.style().drawComplexControl(QStyle.CC_Slider, self.opt, painter)

        # Draw second handle
        self.opt.sliderPosition = self.second_position
        self.style().drawComplexControl(QStyle.CC_Slider, self.opt, painter)

        range_1, range_2 = self.getRange()
        self.edit_1.setText(str(range_1))
        self.edit_2.setText(str(range_2))

    def mousePressEvent(self, event: QMouseEvent):
        self.opt.sliderPosition = self.first_position
        self.first_sc = self.style().hitTestComplexControl(
            QStyle.CC_Slider, self.opt, event.pos(), self
        )

        self.opt.sliderPosition = self.second_position
        self.second_sc = self.style().hitTestComplexControl(
            QStyle.CC_Slider, self.opt, event.pos(), self
        )

    def mouseMoveEvent(self, event: QMouseEvent):
        distance = self.opt.maximum - self.opt.minimum

        pos = self.style().sliderValueFromPosition(
            0, distance, event.pos().x(), self.rect().width()
        )

        if self.first_sc == QStyle.SC_SliderHandle:
            if pos <= self.second_position:
                self.first_position = pos
                self.update()
                return

        if self.second_sc == QStyle.SC_SliderHandle:
            if pos >= self.first_position:
                self.second_position = pos
                self.update()

    def sizeHint(self):
        """ override """
        SliderLength = 84
        TickSpace = 5

        w = SliderLength
        h = self.style().pixelMetric(QStyle.PM_SliderThickness, self.opt, self)

        if (
                self.opt.tickPosition & QSlider.TicksAbove
                or self.opt.tickPosition & QSlider.TicksBelow
        ):
            h += TickSpace

        return (
            self.style()
                .sizeFromContents(QStyle.CT_Slider, self.opt, QSize(w, h), self)
                .expandedTo(QApplication.globalStrut())
        )


class ComboBox(QComboBox):
    def __init__(self, name, w, h):
        super().__init__()
        self.name = name
        self.info_default = """
                            QComboBox {
                                border: 2px solid black;
                                border-radius: 5px;
                                padding-left: 7px;
                                font: bold 14px;
                                color: """ + black_color + """;
                            }
                            QComboBox QAbstractItemView {
                                background: """ + white_color + """;
                                border: 2px solid black;
                            }
                            QComboBox:!editable, QComboBox::drop-down:editable {
                                background: """ + button_color + """;
                            }
                            QComboBox:disabled {
                                background: """ + gray_color + """;
                            }
                            QComboBox:hover {
                                background-color: """ + light_gray_color + """;
                            }
                            QComboBox:drop-down {
                                background-color: """ + gray_color + """;
                                border-top-right-radius: 3px;
                                border-bottom-right-radius: 3px;
                                border-left: 2px solid black;
                                font: bold 14px;
                            }
                            QComboBox:down-arrow {
                                background-color: """ + black_color + """;
                                border: 2px solid black;
                                border-bottom-left-radius: 4px;
                                border-bottom-right-radius: 4px;
                                width: 4px;
                                height: 5px;
                            }
                            /* shift the arrow when popup is open */
                            QComboBox::down-arrow:on { 
                                background-color: """ + button_color + """;
                                border: 2px solid black;
                                border-bottom-left-radius: 4px;
                                border-bottom-right-radius: 4px;
                                width: 4px;
                                height: 5px;
                            }
                            """
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setStyleSheet(self.info_default)


class Switch(QPushButton):
    def __init__(self,
                 uid,
                 callback=None,
                 r=20,
                 w=60,
                 width=66,
                 height=55,
                 parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.w = w
        self.r = r
        self.uid = uid
        self.callback = callback
        self.clicked.connect(self.toggle_button)

        pulse_unchecked_color = pulse_color
        pulse_checked_color = pulse_color
        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(250)  # time in ms
        self.pulse_anim.setStartValue(self.r)
        self.pulse_anim.setEndValue(self.r * 1.1)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.pulse_anim)

    @Slot(int)
    def setup_animation(self):
        self.animations_group.stop()
        self.animations_group.start()

    def toggle_button(self):
        self.setup_animation()
        if self.isChecked():
            self.callback(self.uid, 1)
        else:
            self.callback(self.uid, 2)

    def paintEvent(self, event):
        red = QColor()
        green = QColor()
        red.setRgb(255, 0, 0)
        green.setRgb(51, 133, 255)
        bg_color = green if self.isChecked() else red

        radius = self.r
        radius_handle = radius * 0.75
        width = self.w
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0, 0, 0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        rect = QRect(-width, -radius, 2 * width, 2 * radius)
        painter.drawRoundedRect(rect, radius, radius)
        painter.setBrush(QBrush(bg_color))

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            painter.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            painter.setPen(Qt.NoPen)
            if self.isChecked():
                painter.drawEllipse(-self._pulse_radius + width - radius, -self._pulse_radius, self._pulse_radius * 2,
                                    self._pulse_radius * 2)
                painter.drawEllipse(rect.right() - radius - radius_handle, -radius_handle, radius_handle * 2,
                                    radius_handle * 2)
            else:
                painter.drawEllipse(-self._pulse_radius - width + radius, -self._pulse_radius, self._pulse_radius * 2,
                                    self._pulse_radius * 2)
                painter.drawEllipse(rect.left() + radius - radius_handle, -radius_handle, radius_handle * 2,
                                    radius_handle * 2)

        if self.isChecked():
            painter.drawEllipse(rect.right() - radius - radius_handle, -radius_handle, radius_handle * 2, radius_handle * 2)
        else:
            painter.drawEllipse(rect.left() + radius - radius_handle, -radius_handle, radius_handle * 2, radius_handle * 2)

        painter.end()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class SwitchInverse(QPushButton):
    def __init__(self,
                 uid,
                 callback=None,
                 r=15,
                 w=60,
                 width=66,
                 height=55,
                 parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.w = w
        self.r = r
        self.uid = uid
        self.callback = callback
        self.clicked.connect(self.toggle_button)

        pulse_unchecked_color = pulse_color
        pulse_checked_color = pulse_color
        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(250)  # time in ms
        self.pulse_anim.setStartValue(self.r)
        self.pulse_anim.setEndValue(self.r * 1.1)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.pulse_anim)

    @Slot(int)
    def setup_animation(self):
        self.animations_group.stop()
        self.animations_group.start()

    def toggle_button(self):
        self.setup_animation()
        if self.callback is not None:
            if self.isChecked():
                self.callback(2)
            else:
                self.callback(1)

    def paintEvent(self, event):
        red = QColor()
        green = QColor()
        red.setRgb(255, 0, 0)
        green.setRgb(51, 133, 255)
        bg_color = red if self.isChecked() else green

        radius = self.r
        radius_handle = radius * 0.75
        width = self.w
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0, 0, 0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        rect = QRect(-width, -radius, 2 * width, 2 * radius)
        painter.drawRoundedRect(rect, radius, radius)
        painter.setBrush(QBrush(bg_color))

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            painter.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            painter.setPen(Qt.NoPen)
            if self.isChecked():
                painter.drawEllipse(-self._pulse_radius + width - radius, -self._pulse_radius, self._pulse_radius * 2,
                                    self._pulse_radius * 2)
                painter.drawEllipse(rect.right() - radius - radius_handle, -radius_handle, radius_handle * 2,
                                    radius_handle * 2)
            else:
                painter.drawEllipse(-self._pulse_radius - width + radius, -self._pulse_radius, self._pulse_radius * 2,
                                    self._pulse_radius * 2)
                painter.drawEllipse(rect.left() + radius - radius_handle, -radius_handle, radius_handle * 2,
                                    radius_handle * 2)

        if self.isChecked():
            painter.drawEllipse(rect.right() - radius - radius_handle, -radius_handle, radius_handle * 2, radius_handle * 2)
        else:
            painter.drawEllipse(rect.left() + radius - radius_handle, -radius_handle, radius_handle * 2, radius_handle * 2)

        painter.end()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class Tree(QTreeWidget):
    def __init__(self,
                 data_list,
                 header_data_list,
                 section_w_1=200,
                 section_w_2=150,
                 border_radius=10,
                 font_size: str = "20px",
                 section_font_size: str = "22px",
                 parent=None):
        super().__init__(parent)
        self.setIndentation(20)
        self.setColumnCount(2)
        header = QTreeWidgetItem(['Name', 'Expected Value', 'Arduino Value', 'Pin', 'Unit'])
        self.setHeaderItem(header)
        self.header().resizeSection(0, section_w_1)
        self.header().resizeSection(1, section_w_1)
        self.header().resizeSection(2, section_w_1)
        self.header().resizeSection(3, section_w_2)
        self.setStyleSheet("""
                           QWidget  {
                               background-color: """ + str(white_color) + """;
                               border-radius: 10px;
                               border: 2px solid black;
                               font: """ + str(font_size) + """;
                           }
                           QHeaderView {
                               background-color: """ + str(black_color) + """;
                               border: 0px;
                           }
                           QHeaderView:section {
                               background-color: """ + str(white_color) + """;
                               border-bottom: 2px solid black;
                               border-right: 1px solid black;
                               border-left: 1px solid black;
                               border-top: 1px solid black;
                               border-top-left-radius: """ + str(border_radius) + """px;
                               border-top-right-radius: """ + str(border_radius) + """px;
                               padding-left: 20px;
                               font: bold """ + str(section_font_size) + """;
                           }
                           QScrollBar:vertical {
                               border: none;
                               background: """ + str(light_gray_color) + """;
                               width: 25px;
                               margin: 15px 0 15px 0;
                               border-radius: 0px;
                           }
                           QScrollBar::handle:vertical {
                               background-color: """ + str(handle_hover_color) + """;
                               min-height: 30px;
                           }
                           QScrollBar::handle:vertical:hover {
                               background-color: """ + str(handle_pressed_color) + """;
                           }
                           QScrollBar::handle:vertical:pressed {
                               background-color: """ + str(light_black_color) + """;
                           }
                           QScrollBar::sub-line:vertical {
                               border: none;
                               background-color: """ + str(gray_color) + """;
                               height: 15px;
                               border-top-left-radius: 8px;
                               border-top-right-radius: 8px;
                               subcontrol-position: top;
                               subcontrol-origin: margin;
                           }
                           QScrollBar::sub-line:vertical:hover {
                               background-color: """ + str(deep_gray_color) + """;
                           }
                           QScrollBar::sub-line:vertical:pressed {
                               background-color: """ + str(light_black_color) + """;
                           }
                           QScrollBar::add-line:vertical {
                               border: none;
                               background-color: """ + str(gray_color) + """;
                               height: 15px;
                               border-bottom-left-radius: 8px;
                               border-bottom-right-radius: 8px;
                               subcontrol-position: bottom;
                               subcontrol-origin: margin;
                           }
                           QScrollBar::add-line:vertical:hover {
                               background-color: """ + str(deep_gray_color) + """;
                           }
                           QScrollBar::add-line:vertical:pressed { 
                               background-color: """ + str(light_black_color) + """;
                           }
                           QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                               background: none;
                           }
                           QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                               background: none;
                           }
                           """)

        self.data_list = data_list
        self.header_data_list = header_data_list
        self.create()

    def create(self):
        for i in range(len(self.data_list)):
            data = self.data_list[i]
            header_data = self.header_data_list[i]
            hero_root = self.create_root(self, header_data[0], data[0])
            child_cnt = len(header_data) - 1
            for idx in range(1, child_cnt + 1):
                if i == 1:
                    hero_attr = self.create_child(header_data[idx], data[idx], data[idx + child_cnt],
                                                  data[idx + 2 * child_cnt], data[idx + 3 * child_cnt])
                else:
                    hero_attr = self.create_child(header_data[idx], data[idx], data[idx + child_cnt],
                                                  data[idx + 2 * child_cnt], data[-1])
                hero_root.addChild(hero_attr)

    def create_root(self, parent, name, value):
        """Create root item of the tree"""
        root = QTreeWidgetItem(parent)
        root.setText(0, name)
        root.setText(1, value)
        root.setTextColor(0, QColor(white_color))
        root.setTextColor(1, QColor(white_color))
        root.setTextColor(2, QColor(white_color))
        root.setTextColor(3, QColor(white_color))
        root.setTextColor(4, QColor(white_color))
        root.setBackgroundColor(0, QColor(handle_hover_color))
        root.setBackgroundColor(1, QColor(handle_hover_color))
        root.setBackgroundColor(2, QColor(handle_hover_color))
        root.setBackgroundColor(3, QColor(handle_hover_color))
        root.setBackgroundColor(4, QColor(handle_hover_color))
        root.setExpanded(True)
        return root

    def create_child(self, name, pc_value, arduino_value, pin, unit):
        """Create child item of the tree"""
        root = QTreeWidgetItem()
        root.setText(0, name)
        root.setText(1, pc_value)
        root.setText(2, arduino_value)
        root.setText(3, pin)
        root.setText(4, unit)
        root.setTextColor(0, QColor(handle_hover_color))
        root.setTextColor(1, QColor(handle_hover_color))
        root.setTextColor(2, QColor(handle_hover_color))
        root.setTextColor(3, QColor(handle_hover_color))
        root.setTextColor(4, QColor(handle_hover_color))
        root.setBackgroundColor(0, QColor(widget_background_color))
        root.setBackgroundColor(1, QColor(widget_background_color))
        root.setBackgroundColor(2, QColor(widget_background_color))
        root.setBackgroundColor(3, QColor(widget_background_color))
        root.setBackgroundColor(4, QColor(widget_background_color))
        return root

    def update_expected_value(self, header, input):
        for i in range(len(self.data_list)):
            if self.data_list[i][0] == header:
                for j in range(len(input)):
                    self.data_list[i][j + 1] = str(input[j])
        self.clear()
        self.create()

    def update(self, data_list):
        self.data_list = data_list
        self.clear()
        self.create()


class Dial(QDial):
    def __init__(self,
                 init,
                 min,
                 max,
                 steps,
                 parent=None):
        super(Dial, self).__init__()
        self.setValue(init)
        self.setSingleStep(steps)
        self.setRange(min, max)
        self.setMinimum(min)
        self.setMaximum(max)
        self.setNotchesVisible(True)
        self.setNotchTarget(0.1)
        self.setWrapping(False)
        self.setStyleSheet("""
                           QDial {
                               background-color:QLinearGradient( 
                                   x1: 0.177, y1: 0.004, x2: 0.831, y2: 0.911, 
                                   stop: 0 white, 
                                   stop: 0.061 white, 
                                   stop: 0.066 lightgray, 
                                   stop: 0.5 #242424, 
                                   stop: 0.505 #000000,
                                   stop: 0.827 #040404,
                                   stop: 0.966 #292929,
                                   stop: 0.983 #2e2e2e
                               );
                           }
                           """)
