# Librerias Manejo de Archivos
import urllib.request
from pathlib import Path


def descargarData():

    FILE_NAME = 'taylor_swift_spotify.json'
    PATH = 'data/'
    jsonPath = Path(f'{PATH}{FILE_NAME}')

    if not jsonPath.is_file():
        Path(PATH).mkdir(parents=True, exist_ok=True)
        print(f'Directorio "{PATH}" creado')

        URL = 'https://drive.google.com/u/0/uc?id=1O-z8fCDXy5IleKfU6wRAJZjyz_FIGv9F&export=download'
        print('Descargando...')

        urllib.request.urlretrieve(URL, jsonPath)
        print(f'El archivo "{FILE_NAME}" ha sido descargado en: "{PATH}"')
    else:
        print(f'El archivo "{FILE_NAME}" ya existe en el directorio: "{PATH}"')