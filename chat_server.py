"""
    即时聊天室服务端
    该服务端通过UDP协议实现即时聊天室功能。
"""
import socket
import time
from datetime import datetime


class ChatServer:
    def __init__(self, host: str, port: int):
        """
        初始化ChatServer类实例。
        参数：
            host: string类型，服务器IP地址
            port: int类型，服务器端口号
        返回：
            None
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = {}
        self.administer = {
            "name": "管理员大人",
            "password": "admin",
            "addr": None
        }

    def start(self):
        """
        服务端开启，监听客户端请求。
        参数：
            None
        返回：
            None
        """
        print('Starting server...')
        self.sock.bind((self.host, self.port))
        while True:
            data, address = self.sock.recvfrom(1024)
            if data.decode('utf-8').split("#")[0] == 'join':
                if self.is_duplicate_username(data.decode('utf-8').split("#")[1]):
                    self.sock.sendto('duplicated'.encode('utf-8'), address)
                else:
                    if len(data.decode().split("#")) == 3 and data.decode('utf-8').split('#')[1] == self.administer[
                        "name"] and \
                            data.decode('utf-8').split('#')[2] == self.administer["password"]:
                        self.sock.sendto('to_join_admin'.encode('utf-8'), address)
                        self.clients[address] = "admin"
                        self.administer["addr"] = address
                        time.sleep(0.02)
                        self.send_to_all(f'to_join_admin', address)
                    else:
                        self.sock.sendto('to_join'.encode('utf-8'), address)
                        self.clients[address] = data.decode('utf-8').split("#")[1]
                        time.sleep(0.02)
                        self.send_to_all(f'join#{self.clients[address]}', address)
            elif data.decode('utf-8').split("#")[0] == 'quit':
                self.send_to_all(f'quit#{self.clients[address]}', address)
                del self.clients[address]
            else:
                if address == self.administer["addr"]:
                    print(data.decode())
                    if " " in data.decode() and len(data.decode().split(" ")) == 3:
                        self.execute_cmd(data.decode("utf-8"), self.find_addr_by_name(data.decode().split(" ")[2]),
                                         address)
                    else:
                        self.send_to_all(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} > {data.decode('utf-8').split('#')[0]} {data.decode('utf-8').split(': ')[1]}", address)
                else:
                    self.send_to_all(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} > {data.decode('utf-8')}", address)

    def send_to_all(self, msg, sender_address):
        """
        将消息广播给所有客户端。
        参数：
            msg: string类型，要广播的消息内容
            sender_address: tuple类型，发送消息的客户端地址
        返回：
            None
        """
        for client_address in self.clients:
            if client_address != sender_address:
                self.sock.sendto(msg.encode('utf-8'), client_address)

    def is_duplicate_username(self, name):
        """
        检查新加入的客户端是否与已有客户端用户名重复。
        参数：
            name: string类型，新加入客户端的用户名
        返回：
            bool类型，如果重复返回True，否则返回False
        """
        if name in self.clients.values():
            return True
        else:
            return False

    def execute_cmd(self, cmd, address, admin_addr):
        """
        通过分析命令，解析管理员操作
        """

        operate = cmd.split(" ")[1]
        name = cmd.split(" ")[2]
        if operate == "remove":
            if self.remove_user(name):
                self.sock.sendto("您因违规已被移除聊天室！".encode(), address)
                time.sleep(0.01)
                self.send_to_all(f"成员 {name} 已经被移除聊天室！", address)
                self.sock.sendto("remove@you".encode(), address)
        elif operate == "name":
            self.sock.sendto(
                f"姓名：{name}\nIP地址：{self.find_addr_by_name(name)[0]}\n端口号：{self.find_addr_by_name(name)[1]}\n".encode(),
                admin_addr)

    def remove_user(self, name):
        for k, v in self.clients.items():
            if v == name:
                del [k]
                return True
        return False

    def find_addr_by_name(self, name):
        for k, v in self.clients.items():
            if v == name:
                return k
        return None, None


if __name__ == '__main__':
    server = ChatServer('127.0.0.1', 1234)
    server.start()
