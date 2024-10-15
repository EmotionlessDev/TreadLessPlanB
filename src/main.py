import sys
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MainWindow
import qdarktheme
from net.client import Client


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    # window = MainWindow()
    # window.show()
    username = input("Введите ваш username: ")
    client = Client(username)

    while True:
        command = input("Введите команду (send/exit): ")
        if command == "send":
            recipient = input("Кому: ")
            message = input("Сообщение: ")
            client.send_message(recipient, message)
        elif command == "exit":
            client.close_connection()
            break
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
