"""
    即时聊天室客户端
    该服务端通过UDP协议实现即时聊天室功能。
"""
import socket
import multiprocessing


class ChatClient:
    def __init__(self, host: str, port: int, name: str):
        """
        初始化客户端，包括指定连接的主机地址、端口号和客户端的用户名。
        参数：
            host: string类型，服务器IP地址
            port: int类型，服务器端口号
            name: string类型，用户姓名
        返回：
            None
        """
        self.host = host
        self.port = port
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_process = None
        self.is_remove = False
        self.queue = multiprocessing.Queue()

    def start(self):
        """
        启动聊天室客户端，包括发送 'join' 消息，开始接收并打印聊天室中的消息，以及发送消息。
        参数：
            None
        返回：
            None
        """
        print('正在加入中...')
        self.login()
        self.message_center()

    def login(self):
        """
        客户端登录入口
        参数：
            None
        返回：
            None
        """
        while True:
            self.sock.sendto(f'join#{self.name}'.encode('utf-8'), (self.host, self.port))
            data, address = self.sock.recvfrom(1024)
            if data.decode('utf-8') == 'duplicated':
                print('用户名已被使用，请重新输入！')
                self.name = input('输入你的名字: ')
            elif data.decode('utf-8') == 'to_join_admin':
                print('您加入了聊天室!')
                print("管理员指令表\n1.移除某一用户：remove <username>\n2.查询某一用户：name <username>\n")
                self.receive_process = multiprocessing.Process(target=self.receive)
                self.receive_process.start()
                break
            else:
                print('你加入了聊天室!')
                self.receive_process = multiprocessing.Process(target=self.receive)
                self.receive_process.start()
                break

    def message_center(self):
        """
        客户端消息收发中心，包括发送信息、创建消息监听进程等
        参数：
            None
        返回：
            None
        """
        while True:
            if self.queue.qsize() > 0:
                self.is_remove = self.queue.get()
            if self.is_remove:
                self.receive_process.terminate()
                break
            msg = input('')
            if msg == 'quit':
                self.sock.sendto(f'quit#{self.name}'.encode('utf-8'), (self.host, self.port))
                self.receive_process.terminate()
                break
            else:
                self.sock.sendto(f'{self.name}: {msg}'.encode('utf-8'), (self.host, self.port))

    def receive(self):
        """
        接收并打印聊天室中的消息。
        参数：
            None
        返回：
            None
        """
        while True:
            data, address = self.sock.recvfrom(1024)
            if data.decode('utf-8').split("#")[0] == 'join':
                print(f"{data.decode('utf-8').split('#')[1]}加入了聊天室")
            elif data.decode('utf-8').split('#')[0] == 'quit':
                print(f"{data.decode('utf-8').split('#')[1]}离开了聊天室")
            elif data.decode('utf-8') == 'to_join_admin':
                print("尊贵的管理员已上线，请文明发言！")
            elif data.decode("utf-8") == "remove@you":
                self.queue.put(True)
            else:
                print(data.decode('utf-8'))


if __name__ == '__main__':
    name = input('输入你的名字: ')
    client = ChatClient('127.0.0.1', 1234, name)
    client.start()
