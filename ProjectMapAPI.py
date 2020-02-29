import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic


SCREEN_SIZE = [600, 450]


class ProgectMapAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIProjectMapsAPI.ui', self)
        self.geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba" \
                                "-98533de7710b&geocode=Москва&format=json"
        self.response = requests.get(self.geocoder_request).json()
        self.response_params = {
            'll': ','.join(self.response["response"]["GeoObjectCollection"]["featureMember"][0]
                           ["GeoObject"]["Point"]["pos"].split()),
            'z': '3',
            'l': 'map'}
        self.map_file = "map.png"

        self.initUI()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.map_response and int(self.response_params['z']) < 17:
                self.response_params['z'] = int(self.response_params['z']) + 1
        if event.key() == Qt.Key_PageDown:
            if int(self.response_params['z']) > 2:
                self.response_params['z'] = int(self.response_params['z']) - 1
        if event.key() == Qt.Key_Up:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            if coords[1] + 2 * (1 / z) <= 80:
                coords[1] += 2 * (1 / z)
                self.response_params['ll'] = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Right:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            coords[0] += 2 * (1 / z)
            self.response_params['ll'] = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Down:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            if coords[1] - 2 * (1 / z) >= -70:
                coords[1] -= 2 * (1 / z)
                self.response_params['ll'] = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Left:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            coords[0] -= 2 * (1 / z)
            self.response_params['ll'] = ','.join(list(map(str, coords)))
        self.getImage()
        self.setImage()


    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.response_params['ll']}&" \
                      f"z={self.response_params['z']}&l={self.response_params['l']}"
        self.map_response = requests.get(map_request)

        # Запишем полученное изображение в файл.
        if self.map_response:
            with open(self.map_file, "wb") as file:
                file.write(self.map_response.content)

    def setImage(self):
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def initUI(self):
        self.getImage()
        self.setImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProgectMapAPI()
    ex.show()
    os.remove('map.png')
    sys.exit(app.exec())
