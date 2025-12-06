
import requests


class Zabbix_graphic:
    types: dict = {
        "btk": "90223",
        "lancache": "110949"}

    def __init__(self, login: str, password: str, type:str) -> None:
        self.login = login
        self.password = password
        self.type = self.types[type]

    def download(self):
        session = requests.Session()
        # Логинимся
        login_data = {
            'name': self.login,
            'password': self.password,
            'enter': 'Sign in'
        }
        params = {
            'graphid': self.type,
            'period': '7200',
            'width': '1782'
        }
        try:
            session.post('http://172.16.1.5/index.php', data=login_data)

            # Скачиваем график
            response = session.get(
                "http://172.16.1.5/chart2.php",
                params=params)
        except:
            return None
        return response.content
