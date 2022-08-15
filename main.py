import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QLabel,
    QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPixmapCache
from pathlib import Path, PurePath

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.animating_label = QLabel('animation here')
        self.animating_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.animating_label.pixmap().size().setWidth(200)
        self.animating_label.pixmap().size().setHeight(200)
        self.setCentralWidget(self.animating_label)

        parent_path = Path(__file__).parent
        self.images_path = parent_path / 'images/animation_set/'
        self.animating_label.setPixmap(QPixmap(self.images_path.__str__() + "/clock01.png"))

        self.pixmapcache_keys: [str] = []

        self.load_images()
        test = QPixmapCache.find("clock02")
        self.animating_label.setPixmap(test)
        # self.animating_label.setPixmap(QPixmapCache.find("clock03"))
        pass

    def load_images(self):
        image_suffixes = ['.jpg', '.png', '.gif', '.bmp']
        imgs_found_count = 0
        for filepath in self.images_path.iterdir():
            if filepath.suffix in image_suffixes:
                imgs_found_count += 1
                cache_key = filepath.stem
                self.pixmapcache_keys.append(cache_key)

                if not QPixmapCache.find(cache_key):
                    pixmap = QPixmap(filepath.__str__())
                    QPixmapCache.insert(cache_key, pixmap)

                print("pixmap %s" % cache_key, QPixmapCache.find(cache_key))


        print(imgs_found_count, "image(s) found in animation_set directory.", len(self.pixmapcache_keys),
              "keys loaded into QPixmapCache")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

# start Qt event loop
app.exec()

print("Script complete.")
sys.exit(1)