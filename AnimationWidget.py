from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathlib import Path

class AnimationWidget(QLabel):

    def __init__(self, images_path: Path):
        super().__init__()
        self.pixmaps: [QPixmap] = []
        self.pixmap_current_index = -1
        self.load_images(images_path)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def load_images(self, path: Path):
        image_suffixes = ['.jpg', '.png', '.gif', '.bmp']
        imgs_found_count = 0
        for filepath in sorted(path.iterdir()):
            if filepath.suffix in image_suffixes:
                imgs_found_count += 1
                qpixmap = QPixmap(filepath.__str__())
                self.pixmaps.append(qpixmap)
        print(imgs_found_count, "images found and imported")

    def advance(self):
        if self.pixmap_current_index >= len(self.pixmaps) - 1:
            self.pixmap_current_index = 0
        else:
            self.pixmap_current_index += 1
        self.setPixmap(self.pixmaps[self.pixmap_current_index])


