import socket
import json
import threading


class Client:
    """Messenger Client."""

    def __init__(self, username: str, host: str = "127.0.0.1", port: int = 8000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.username = username
        init_data = {
            "action": "init",
            "username": self.username,
        }
        self.client_socket.send(json.dumps(init_data).encode())
        response = self.client_socket.recv(1024).decode()
        response_data = json.loads(response)
        if response_data.get("status") != "success":
            print(f"Ошибка подключения: {response_data.get('msg')}")
            self.client_socket.close()
            return
        print(f"Подключен как {self.username}")

        listener_th = threading.Thread(target=self.listener, daemon=True)
        listener_th.start()

    def listener(self):
        while True:
            data = self.client_socket.recv(4096).decode()
            if not data:
                print("Соедение с сервером потеряно")
                break
            response = json.loads(data)
            action = response.get("action")
            if action == "rcv_msg":
                sender = response.get("sender")
                msg = response.get("msg")
                print(f"От {sender}: {msg}")
            else:
                status = response.get("status")
                msg = response.get("msg")
                print(f"{status} : {msg}")

    def send_message(self, recipient: str, msg: str):
        # Формируем запрос, имя пользователя -> сообщение
        # "action": "send_msg" or "rcv_msg"
        # "sender": username
        # "msg": message
        data = json.dumps({"action": "send_msg", "recipient": recipient, "msg": msg})
        self.client_socket.send(data.encode())

    def close_connection(self):
        self.client_socket.close()
