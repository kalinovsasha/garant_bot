# ip dhcp-server lease remove [find address="100.70.19.13"] -удалить по Ip
# ip dhcp-server lease remove [find mac-address="C0:25:E9:08:BD:C9"] - по маку
# ip firewall address-list print  where address="100.70.19.13 - вывести в каком адреслисте
# queue simple print where target="100.70.56.6/32" -вывести скоростные параметры
import paramiko


class Mikrotik:
    def __init__(self, servers: list) -> None:
        self.servers = servers

    def remove_lease_ip(self, server: str, ip: str) -> None:
        pass

    def print_que(self) -> None:
        pass

    def print(self):
        print(self.servers)
        return self.servers
