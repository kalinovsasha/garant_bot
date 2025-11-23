# ip dhcp-server lease remove [find address="100.70.19.13"] -удалить по Ip
# ip dhcp-server lease remove [find mac-address="C0:25:E9:08:BD:C9"] - по маку
# ip firewall address-list print  where address="100.70.19.13 - вывести в каком адреслисте
# queue simple print where target="100.70.56.6/32" -вывести скоростные параметры
import paramiko
funeral: tuple = []

class Mikrotik:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
        self.ssh: paramiko.SSHClient = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def print_que(self, server: str, client_ip: str) -> None:
        try:
            # подключается по ssh
            self.ssh.connect(server,
                             username=self.login,
                             password=self.password,
                             look_for_keys=False,
                             allow_agent=False,
                             timeout=10)
            # вводит команду и и cохраняет stdin, stdout, stderr
            stdin, stdout, stderr = self.ssh.exec_command(
                f'queue simple print where target="{client_ip}/32"')
            resp = stdout.read().decode('utf-8', errors='ignore')
            self.ssh.close()
            resp = resp[resp.find("limit-at"):resp.find("max-limit")]
            resp = resp.replace("limit-at=", "Скорость тарифа: ")
            if resp:
                return resp
            else:
                return f'Для {client_ip} не найден, возможно не верный bras ip'
        except Exception as e:
            return f"Error {e}"

    def print_acl(self, client_ip: str):
        server = self.detect_bras_ip(client_ip)
        try:
            # подключается по ssh
            self.ssh.connect(server,
                             username=self.login,
                             password=self.password,
                             look_for_keys=False,
                             allow_agent=False,
                             timeout=10)
            # вводит команду и и cохраняет stdin, stdout, stderr
            _, stdout, _ = self.ssh.exec_command(
                f'ip firewall address-list print  where address="{client_ip}"')
            resp = stdout.read().decode('utf-8', errors='ignore')
            self.ssh.close()
            if resp:
                return resp.replace("   ", " ")
            else:
                return f'acl для {client_ip} не найден'
        except Exception as e:
            return f"Error {e}"

    def remove_lease_ip(self, client_ip: str) -> None:
        server = self.detect_bras_ip(client_ip)
        try:
            # подключается по ssh
            self.ssh.connect(server,
                             username=self.login,
                             password=self.password,
                             look_for_keys=False,
                             allow_agent=False,
                             timeout=10)
            # вводит команду и и cохраняет stdin, stdout, stderr
            _, stdout, _ = self.ssh.exec_command(
                f'ip dhcp-server lease remove [find address="{client_ip}"]')
            resp = stdout.read().decode('utf-8', errors='ignore')
            self.ssh.close()
            return f'Команда на удаление {client_ip} отправлена на {server}'
        except Exception as e:
            return f"Error {e}"

    # Вычисляет Ip браса по ip клиента
    def detect_bras_ip(self, client_ip: str) -> str:
        client = client_ip.split('.')
        match client[1]:
            case "71":
                return "172.16.9.24"
            case "70":
                return "172.16.9.21"
            case "72":
                return "172.16.9.23"
        return "Введен не верный, либо не ipoe адрес"