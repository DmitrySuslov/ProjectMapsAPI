import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic


class ProgectMapAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIProjectMapsAPI.ui', self)
        self.initUI()
        self.comboBox.activated[str].connect(self.map_changed)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.map_response and int(self.response_params['z']) < 17:
                self.z += 1
        if event.key() == Qt.Key_PageDown:
            if int(self.response_params['z']) > 2:
                self.z -= 1
        if event.key() == Qt.Key_Up:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            if coords[1] + 2 * (1 / z) <= 80:
                coords[1] += 2 * (1 / z)
                self.ll = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Right:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            coords[0] += 2 * (1 / z)
            self.ll = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Down:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            if coords[1] - 2 * (1 / z) >= -70:
                coords[1] -= 2 * (1 / z)
                self.ll = ','.join(list(map(str, coords)))
        if event.key() == Qt.Key_Left:
            coords = self.response_params['ll'].split(',')
            z = int(self.response_params['z'])
            coords[0], coords[1] = float(coords[0]), float(coords[1])
            coords[0] -= 2 * (1 / z)
            self.ll = ','.join(list(map(str, coords)))
        self.getImage(1)
        self.setImage()

    def find_map(self):
        map = self.comboBox.currentText()
        if map == 'Схема':
            self.map_file = "map.png"
            return 'map'
        elif map == 'Спутник':
            self.map_file = "map.jpg"
            return 'sat'
        elif map == 'Гибрид':
            self.map_file = "map.jpg"
            return 'sat,skl'

    def map_changed(self):
        self.getImage(0)
        self.setImage()

    def getImage(self, b):
        self.geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba" \
                                f"-98533de7710b&geocode={self.object}&format=json"
        self.response = requests.get(self.geocoder_request).json()
        self.coords = self.response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        if not b:
            ll = ','.join(self.response["response"]["GeoObjectCollection"]["featureMember"][0]
                           ["GeoObject"]["Point"]["pos"].split())
            self.ll = ll
        else:
            ll = self.ll
        self.response_params = {
            'll': self.ll,
            'z': self.z,
            'l': self.find_map(),
            'pt': ",".join([str(self.coords[0]), str(self.coords[1]), "pm2dom"])}

        self.set_address(self.response)

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.response_params['ll']}&" \
                      f"z={self.response_params['z']}&l={self.response_params['l']}&pt={self.response_params['pt']}"

        self.map_response = requests.get(map_request)

        if self.map_response:
            file = open(self.map_file, "wb")
            file.write(self.map_response.content)
            file.close()


    def set_address(self, response):
        address = (response["response"]["GeoObjectCollection"]["featureMember"]
                        [0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"])
        self.object_address.setText(address)

    def setImage(self):
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def searching(self):
        self.object = self.address.text()
        self.getImage(0)
        self.setImage()

    def initUI(self):
        self.search.clicked.connect(self.searching)
        self.object = 'Москва'
        self.map_file = "map.png"
        self.z = 4
        self.getImage(0)
        self.setImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ProgectMapAPI = ProgectMapAPI()
    ProgectMapAPI.show()
    os.remove('map.png')
    os.remove('map.jpg')
    sys.exit(app.exec())