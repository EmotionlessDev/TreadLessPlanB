import socket
import sqlite3
import json
import threading
from src.ui.Database import Database

active_clients: dict[str, socket.SocketType] = {}
user_id: dict[str, int] = {}
db = Database()


def load_all_id() -> None:
    db.connect("db.db")
    rows = db.fetch_data("SELECT id, username FROM users")
    db.close()
    for row in rows:
        id, username = row
        user_id[username] = id


def handle_client(client_socket: socket.SocketType, username: str, address: str) -> None:
    print(f"Соединение от {address} установлено для пользователя {username}!")
    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break
            request = json.loads(data)
            action = request.get("action")
            if action == "send_msg":
                # recipient = request.get("recipient")
                # recipient_id = user_id[recipient]
                msg = request.get("msg")
                sender_id = user_id[username]

                if not sender_id:
                    response = {"status": "error", "msg": "Неизвестный отправитель"}
                    client_socket.send(json.dumps(response).encode())
                    continue
                # if not recipient_id:
                #     response = {"status": "error", "msg": "Неизвестный получатель"}
                #     client_socket.send(json.dumps(response).encode())
                #     continue
                db.connect("db.db")
                db.insert_data("messages", (None, sender_id, sender_id, msg))
                db.close()
                response = {"status": "success", "msg": "Сообщение отправлено"}

                # if recipient in active_clients:
                #     recipient_socket = active_clients[recipient]
                # msg_data = {
                #     "action": "rcv_msg",
                #     "sender": username,
                #     "msg": msg,
                # }
                # try:
                #     recipient_socket.send(json.dumps(msg_data).encode())
                # except Exception as e:
                #     print(
                #         f"Не удалось отправить сообщение пользователю {recipient}: {e}"
                #     )
            else:
                response = {"status": "error", "msg": "Неизвестное действие"}
                client_socket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Ошибка при обработке клиента {address}: {e}")
    finally:
        if username in active_clients:
            del active_clients[username]
        client_socket.close()
        print(f"Соединение от {address} для пользователя {username} закрыто!")


def main():
    load_all_id()
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8000
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("Server started and listening")

    while True:
        clientsocket, address = serversocket.accept()

        data = clientsocket.recv(4096)
        if not data:
            clientsocket.close()
            continue
        init_data = json.loads(data)
        action = init_data.get("action")
        if action == "init":
            username = init_data.get("username")
            if username in active_clients:
                clientsocket.close()
                continue
            active_clients[username] = clientsocket
            success_response = {"status": "success", "message": "Initialization successful"}
            clientsocket.send(json.dumps(success_response).encode())
            print(f"Пользователь {username} подключен из {address}")
            client_thread = threading.Thread(
                target=handle_client, args=(clientsocket, username, address)
            )
            client_thread.start()


if __name__ == "__main__":
    main()
