from PyQt5.QtCore import pyqtSignal, QThread
import time
import threading
from .Database import Database


class MessageFetcher(QThread):
    new_message = pyqtSignal(str)  # Сигнал для передачи нового сообщения

    def __init__(self, db_path, last_id=0):
        super().__init__()
        self.db_path = db_path
        self.last_id = last_id
        self._running = True

    def run(self):
        db = Database()
        db.connect(self.db_path)
        while self._running:
            try:
                # Получаем новые сообщения с ID больше последнего
                # query = "SELECT id, sender_id, message FROM messages WHERE id > ? ORDER BY id ASC"
                query = """
                SELECT messages.id, users.username, messages.message
                FROM messages
                JOIN users ON messages.sender_id = users.id
                WHERE messages.id > ?
                ORDER BY messages.id ASC
                """
                data = db.fetch_data(query, (self.last_id,))
                for row in data:
                    msg_id, sender, message = row
                    formatted_message = f"{sender}: {message}"
                    self.new_message.emit(formatted_message)
                    self.last_id = msg_id  # Обновляем последний ID
                time.sleep(1)  # Пауза перед следующим запросом
            except Exception as e:
                print(f"Ошибка при получении сообщений: {e}")
                time.sleep(5)  # Пауза при ошибке
        db.close()

    def stop(self):
        self._running = False
        self.wait()
