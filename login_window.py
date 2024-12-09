from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from register_window import RegisterWindow # Импортируем класс окна регистрации
from main_window import MainWindow # Импортируем класс главного окна
from design import setup_label_style, setup_input_style, setup_button_style # Импортируем функции для настройки стилей

class LoginWindow(QWidget):
    def __init__(self, db, login):
        super().__init__()
        self.db = db
        self.login = login
        self.initUI()

    def initUI(self):
        # Настройка окна
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(400, 320)
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #e0f7fa;")

        # Заголовок окна
        title_label = QLabel("Добро пожаловать!")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00796b;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Центрируем заголовок
        layout.addWidget(title_label)

        # Метка для поля ввода "Логин"
        self.login_label = QLabel("Логин:")
        setup_label_style(self.login_label)
        layout.addWidget(self.login_label)

        # Поле для ввода логина
        self.login_input = QLineEdit(self)
        setup_input_style(self.login_input)
        self.login_input.textChanged.connect(self.check_login_input)
        layout.addWidget(self.login_input)

        # Метка для поля ввода "Пароль"
        self.password_label = QLabel("Пароль:")
        setup_label_style(self.password_label)
        layout.addWidget(self.password_label)

        # Поле для ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        setup_input_style(self.password_input)
        self.password_input.setDisabled(True)
        layout.addWidget(self.password_input)

        # Кнопка "Войти"
        self.login_button = QPushButton("Войти", self)
        setup_button_style(self.login_button)
        self.login_button.clicked.connect(self.loginn)
        layout.addWidget(self.login_button)

        # Кнопка "Регистрация"
        self.register_button = QPushButton("Регистрация", self)
        setup_button_style(self.register_button)
        self.register_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.register_button)

        self.setLayout(layout) # Устанавливаем компоновщик для окна

    # Метод для открытия окна регистрации
    def open_register_window(self):
        self.clear_inputs()  # Очищаем поля ввода перед открытием окна регистрации
        self.register_window = RegisterWindow(self.db) # Создаем экземпляр окна регистрации
        self.register_window.show() # Показываем окно регистрации

    # Проверки для поля логина
    def check_login_input(self):
        login = self.login_input.text()

        # Проверка на пустое поле
        if not login:
            self.set_input_enabled(False, self.password_input)
        else:
            self.set_input_enabled(True, self.password_input)

    # Метод для обработки входа пользователя
    def loginn(self):
        login = self.login_input.text()
        password = self.password_input.text()

        # Проверка на заполненность всех полей
        if not login or not password:
            self.show_message("Ошибка", "Все поля должны быть заполнены.")
            return

        user = self.db.get_user(login) # Получаем пользователя из базы данных по логину

        # Если пользователь не найден
        if not user:
            self.show_message("Ошибка", "Пользователь не найден.")
            self.clear_inputs()  # Очищаем поля ввода, если пользователь не найден
            return

        stored_password_hash = user[2]  # Третий элемент в кортежах user - это хеш пароля

        # Проверяем верный ли пароль
        if not self.db.verify_password(stored_password_hash, password):
            self.show_message("Ошибка", "Неверный пароль.")
            return

        # Если вход успешен, открываем главное окно
        self.main_window = MainWindow(self.db, login) # Создаем экземпляр главного окна
        self.main_window.show() # Показываем главное окно
        self.close() # Закрываем окно авторизации

    # Метод для отображения сообщений пользователю
    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical if "Ошибка" in title else QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    # Утилита для включения/выключения нескольких полей ввода
    def set_input_enabled(self, enabled, *inputs):
        # Устанавливаем состояние (включено/выключено) для каждого поля ввода
        for input_field in inputs:
            input_field.setEnabled(enabled)

    # Метод для очистки полей ввода
    def clear_inputs(self):
        self.login_input.clear() # Очищаем поле ввода логина
        self.password_input.clear() # Очищаем поле ввода пароля
        self.set_input_enabled(False, self.password_input) # Блокируем поле пароля