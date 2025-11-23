
import requests


class Zabbix_graphic:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    def download(self):
        session = requests.Session()
        # Логинимся
        login_data = {
            'name': self.login,
            'password': self.password,
            'enter': 'Sign in'
        }
        params = {
                'graphid': '90223',
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


class Cacti_graphic:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    def download(self):
        session = requests.Session()
        # Логинимся
        login_data = {
            'name': self.login,
            'password': self.password,
            'enter': 'Sign in'
        }
        try:
            session.post('http://172.16.0.253/index.php', data=login_data)

            # Скачиваем график
            response = session.get(
                "http://172.16.1.5/chart2.php?graphid=90223&period=7464&stime=20271123170303&updateProfile=1&profileIdx=web.screens&profileIdx2=90223&width=1782&sid=4b79a64389ef53ec&screenid=&curtime=1763914058054")
        except:
            return None
        return response.content
