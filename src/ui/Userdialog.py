import sqlite3
from typing import Optional

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QTabWidget,
    QWidget,
)

from .Database import Database


class Userdialog(QDialog):
    """Dialog for user authentication and registration."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize the user dialog."""
        super().__init__(parent)
        self.setWindowTitle("User Authentication")

        # Создание вкладок для регистрации и входа
        self.tabs = QTabWidget()
        self.login_tab = QWidget()
        self.register_tab = QWidget()

        self.create_login_tab()
        self.create_register_tab()

        self.tabs.addTab(self.login_tab, "Login")
        self.tabs.addTab(self.register_tab, "Register")

        # Основная компоновка
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Подключение к базе данных db.db и создание таблицы users, если она еще не существует
        self.db = Database()
        self.db.connect("db.db")
        self.initialize_database()

    def create_login_tab(self) -> None:
        """Создает вкладку для входа."""
        login_layout = QFormLayout()

        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_user)

        login_layout.addRow("Username:", self.login_username_input)
        login_layout.addRow("Password:", self.login_password_input)
        login_layout.addWidget(login_button)

        self.login_tab.setLayout(login_layout)

    def create_register_tab(self) -> None:
        """Создает вкладку для регистрации."""
        register_layout = QFormLayout()

        self.register_username_input = QLineEdit()
        self.register_password_input = QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_user)

        register_layout.addRow("Username:", self.register_username_input)
        register_layout.addRow("Password:", self.register_password_input)
        register_layout.addWidget(register_button)

        self.register_tab.setLayout(register_layout)

    def login_user(self) -> None:
        """Обрабатывает вход пользователя."""
        username = self.login_username_input.text().strip()
        password = self.login_password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Both fields are required!")
            return

        try:
            query = "SELECT id, password FROM users WHERE username = ?"
            result = self.db.fetch_data(query, (username,))
            if result and result[0][1] == password:
                self.current_user_id = result[0][
                    0
                ]  # Сохранение id текущего пользователя
                QMessageBox.information(self, "Success", "Login successful!")
                self.accept()
            else:
                QMessageBox.warning(
                    self, "Login Failed", "Incorrect username or password."
                )
        except Exception as e:
            QMessageBox.critical(self, "Login Error", str(e))

    def register_user(self) -> None:
        """Обрабатывает регистрацию нового пользователя."""
        username = self.register_username_input.text().strip()
        password = self.register_password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Both fields are required!")
            return

        try:
            # Попытка вставить нового пользователя
            self.db.insert_data(
                "users", (None, username, password)
            )  # None используется для автоинкрементируемого id

            QMessageBox.information(self, "Success", "User registered successfully!")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")
        except Exception as e:
            QMessageBox.critical(self, "Registration Error", str(e))

    def closeEv(self, event) -> None:
        """Закрытие окна без сохранения данных."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit without saving?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()

    def initialize_database(self) -> None:
        """Создает таблицу users, если она еще не существует."""
        try:
            self.db.create_table(
                "users",
                "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT",
            )
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
