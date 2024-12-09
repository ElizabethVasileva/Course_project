import sys # Импортируем модуль sys для работы с аргументами командной строки и завершения программы
from PyQt6.QtWidgets import QApplication # Импортируем класс QApplication из модуля PyQt6 для создания GUI приложения
from db import DB # Импортируем класс DB из модуля db для работы с базой данных
from login_window import LoginWindow # Импортируем класс LoginWindow из модуля login_window для создания окна входа

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DB()
    login = '' # Инициализируем переменную login пустой строкой, которая будет использоваться для хранения логина пользователя
    login_window = LoginWindow(db, login) # Экземпляр окна входа (передается объект базы данных и логин)
    login_window.show() # Отображаем окно входа на экране
    sys.exit(app.exec()) # sys.exit() гарантирует корректное завершение программы