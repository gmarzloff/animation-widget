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
from PyQt6.QtGui import QPixmap
from pathlib import Path

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.animating_label = QLabel('animation here')
        self.animating_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.animating_label.pixmap().size().setWidth(200)
        self.animating_label.pixmap().size().setHeight(200)

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
        main_layout.addWidget(self.animating_label)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        parent_path = Path(__file__).parent
        self.images_path = parent_path / 'images/animation_set/'
        self.animating_label.setPixmap(QPixmap(self.images_path.__str__() + "/clock01.png"))

        self.pixmaps: [QPixmap] = []
        self.pixmap_current_index = -1
        self.load_images()

        self.timer = QTimer()
        self.timer.timeout.connect(self.advance)
        frames_per_second = 40
        rate_slider.setValue(frames_per_second)
        self.refresh_interval = int(1000/frames_per_second)
        self.timer.start(self.refresh_interval)

    def load_images(self):
        image_suffixes = ['.jpg', '.png', '.gif', '.bmp']
        imgs_found_count = 0
        for filepath in sorted(self.images_path.iterdir()):
            if filepath.suffix in image_suffixes:
                imgs_found_count += 1
                qpixmap = QPixmap(filepath.__str__())
                self.pixmaps.append(qpixmap)

    def advance(self):
        if self.pixmap_current_index >= len(self.pixmaps) - 1:
            self.pixmap_current_index = 0
        else:
            self.pixmap_current_index += 1
        self.animating_label.setPixmap(self.pixmaps[self.pixmap_current_index])
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