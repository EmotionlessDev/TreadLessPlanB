from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QListWidget, QTextEdit, QLineEdit, QPushButton
from .Userdialog import Userdialog
from .Database import Database
from .MessageFetcher import MessageFetcher


class MainWindow(QMainWindow):
    """
    Main window widget.
    """
    def __init__(self):
        super().__init__()
        entry = Userdialog()
        entry.exec()
        self.setWindowTitle("TreadLess")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        self.contacts_list = QListWidget()
        self.contacts_list.setMaximumWidth(200)
        main_layout.addWidget(self.contacts_list)

        chat_layout = QVBoxLayout()
        main_layout.addLayout(chat_layout)

        self.chat_window = QTextEdit()
        self.chat_window.setReadOnly(True)
        chat_layout.addWidget(self.chat_window)

        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Отправить")
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        chat_layout.addLayout(input_layout)

        self.send_button.clicked.connect(self.send_message)
        # Инициализируем последний ID
        self.last_message_id = 0

        # Запускаем поток для получения сообщений
        self.fetcher = MessageFetcher("db.db", self.last_message_id)
        self.fetcher.new_message.connect(self.display_message)
        self.fetcher.start()

    def send_message(self):

        message = self.message_input.text().strip()
        if message:
            self.chat_window.append(f"Вы: {message}")
            self.message_input.clear()
            self.message_input.returnPressed.connect(self.send_message)

    def display_message(self, message):
        self.chat_window.append(message)
