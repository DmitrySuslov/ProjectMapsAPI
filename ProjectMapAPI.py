import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap

SCREEN_SIZE = [600, 450]


class ProgectMapAPI(QWidget):
    def __init__(self):
        self.geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba" \
                                "-98533de7710b&geocode=Австралия&format=json"
        self.response = requests.get(self.geocoder_request).json()
        self.response_params = {
            'll': ','.join(self.response["response"]["GeoObjectCollection"]["featureMember"][0]
                           ["GeoObject"]["Point"]["pos"].split()),
            'z': '3',
            'l': 'sat'}
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.response_params['ll']}&" \
                      f"z={self.response_params['z']}&l={self.response_params['l']}"
        response = requests.get(map_request)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('ProjectMapsAPI')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ProgectMapAPI = ProgectMapAPI()
    ProgectMapAPI.show()
    os.remove('map.png')
    sys.exit(app.exec())
