import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSlider
)
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path
from AnimationWidget import AnimationWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        parent_path = Path(__file__).parent
        images_path = parent_path / 'images/animation_set/'
        self.animation_widget = AnimationWidget(images_path)

        self.frame_rate_label = QLabel('0')
        self.frame_rate_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        font = self.frame_rate_label.font()
        font.setPointSizeF(18)
        font.setBold(True)
        self.frame_rate_label.setFont(font)

        rate_slider = QSlider()
        rate_slider.setMinimum(1)
        rate_slider.setMaximum(50)
        rate_slider.setFixedWidth(80)
        rate_slider.valueChanged.connect(self.slider_changed)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.frame_rate_label)
        left_layout.addWidget(rate_slider)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.animation_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        frames_per_second = 40
        rate_slider.setValue(frames_per_second)
        self.refresh_interval = int(1000/frames_per_second)
        self.timer = QTimer()
        self.timer.timeout.connect(self.animation_handler)
        self.timer.start(self.refresh_interval)

    def animation_handler(self):
        self.animation_widget.advance()
        self.timer.start(self.refresh_interval)

    def slider_changed(self):
        new_frame_rate = self.sender().value()
        self.frame_rate_label.setText("%s fps" % str(new_frame_rate))
        self.refresh_interval = int(1000/new_frame_rate)

app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Control frame rate of animation example")
window.show()

# start Qt event loop
app.exec()

print("Script complete.")
sys.exit(1)