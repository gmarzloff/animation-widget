import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QWidget,
    QSlider
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPixmapCache
from pathlib import Path

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.animating_label = QLabel('animation here')
        self.animating_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.animating_label.pixmap().size().setWidth(200)
        self.animating_label.pixmap().size().setHeight(200)

        rate_slider = QSlider()
        rate_slider.setMinimum(0)
        rate_slider.setMaximum(20)
        rate_slider.setContentsMargins(120, 120, 120, 120)

        self.layout = QHBoxLayout()
        self.layout.addWidget(rate_slider)
        self.layout.addWidget(self.animating_label)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        parent_path = Path(__file__).parent
        self.images_path = parent_path / 'images/animation_set/'
        self.animating_label.setPixmap(QPixmap(self.images_path.__str__() + "/clock01.png"))

        self.animation_keys: [str] = []
        self.pixmaps: [QPixmap] = []
        self.pixmap_current_index = -1
        self.load_images()

        self.timer = QTimer()
        self.timer.timeout.connect(self.advance)
        frames_per_second = 40
        self.refresh_interval = int(1000/frames_per_second)
        self.timer.start(self.refresh_interval)

    def load_images(self):
        image_suffixes = ['.jpg', '.png', '.gif', '.bmp']
        imgs_found_count = 0
        for filepath in sorted(self.images_path.iterdir()):
            if filepath.suffix in image_suffixes:
                imgs_found_count += 1
                cache_key = filepath.stem
                self.animation_keys.append(cache_key)

                qpixmap = QPixmap(filepath.__str__())
                self.pixmaps.append(qpixmap)

        print(imgs_found_count, "image(s) found in animation_set directory.", len(self.animation_keys),
              "keys loaded into QPixmapCache")

    def advance(self):
        if self.pixmap_current_index >= len(self.pixmaps) - 1:
            self.pixmap_current_index = 0
        else:
            self.pixmap_current_index += 1
        self.animating_label.setPixmap(self.pixmaps[self.pixmap_current_index])
        self.timer.start(self.refresh_interval)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

# start Qt event loop
app.exec()

print("Script complete.")
sys.exit(1)