import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.MainWindow import Ui_MainWindow

MAP_NAME = 'cache/map.png'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ll = (37.53088, 55.70311)
        self.spn = 0.005
        self.update_map()

    def update_map(self):
        api_address = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': f'{self.ll[0]},{self.ll[1]}',
            'spn': f'{self.spn},{self.spn}',
            'l': 'map',
            'size': '650,450'
        }
        response = requests.get(api_address, params=params)

        if not response:
            sys.exit(f'RequestError[{response.status_code}]: {response.reason} ({response.url})')

        with open(MAP_NAME, 'wb') as f:
            f.write(response.content)

        self.map.setPixmap(QPixmap(MAP_NAME))

    def closeEvent(self, event):
        os.remove(MAP_NAME)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
