import re # Импортируем модуль регулярных выражений для валидации ввода
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from design import setup_label_style, setup_input_style, setup_button_style

class RegisterWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db # Сохраняем ссылку на объект базы данных
        self.initUI() # Инициализируем пользовательский интерфейс

    def initUI(self):
        # Настройка окна
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 360)
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #e0f7fa;")

        # Заголовок окна
        title_label = QLabel("Регистрация")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00796b;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Центрируем заголовок
        layout.addWidget(title_label)

        # Метка для поля ввода "Имя"
        self.name_label = QLabel("Имя:")
        setup_label_style(self.name_label)
        layout.addWidget(self.name_label)

        # Поле для ввода имени
        self.name_input = QLineEdit(self)
        setup_input_style(self.name_input)
        self.name_input.textChanged.connect(self.check_name_input)
        layout.addWidget(self.name_input)

        # Метка для поля ввода "Логин"
        self.login_label = QLabel("Логин:")
        setup_label_style(self.login_label)
        layout.addWidget(self.login_label)

        # Поле для ввода логина
        self.login_input = QLineEdit(self)
        setup_input_style(self.login_input)
        self.login_input.textChanged.connect(self.check_login_input)
        self.login_input.setDisabled(True) # Блокируем логин до ввода имени
        layout.addWidget(self.login_input)

        # Метка для поля ввода "Пароль"
        self.password_label = QLabel("Пароль:")
        setup_label_style(self.password_label)
        layout.addWidget(self.password_label)

        # Поле для ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Устанавливаем режим скрытия ввода пароля
        setup_input_style(self.password_input)
        self.password_input.textChanged.connect(self.check_password_input)
        self.password_input.setDisabled(True) # Блокируем пароль до ввода логина
        layout.addWidget(self.password_input)

        # Кнопка для регистрации
        self.register_button = QPushButton("Зарегистрироваться", self)
        setup_button_style(self.register_button)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    # Проверки для поля "Имя"
    def check_name_input(self):
        name = self.name_input.text()

        # Проверка на пустое поле
        if not name:
            self.set_input_enabled(False, self.login_input) # Блокируем поле логина
            return

        # Проверка, что имя состоит только из букв
        if re.match("^[a-zA-Zа-яА-ЯёЁ]+$", name):
            self.set_input_enabled(True, self.login_input) # Разблокируем поле логина
        else:
            self.show_message("Ошибка", "В поле «Имя» не допускаются цифры и символы.")
            self.name_input.clear() # Очищаем поле ввода имени
            self.set_input_enabled(False, self.login_input) # Блокируем поле логина

        self.set_input_enabled(True, self.login_input) # Разблокируем поле логина

    # Проверки для поля "Логин"
    def check_login_input(self):
        login = self.login_input.text()

        # Проверка на пустое поле
        if not login:
            self.set_input_enabled(False, self.password_input)
            return

        # Проверка, что в логине нет кириллических символов
        if re.search("[а-яА-ЯёЁ]", login):
            self.show_message("Ошибка", "В поле «Логин» не должно быть кириллицы.")
            self.login_input.clear()
            self.set_input_enabled(False, self.password_input)
            return

        # Проверка, что логин начинается с латинских букв
        if not re.match("[a-zA-Z]", login):
            self.show_message("Ошибка", "Логин должен начинаться с латинских букв.")
            self.login_input.clear()
            self.set_input_enabled(False, self.password_input)
            return

        # Проверка на длину логина
        if len(login) > 20:
            self.show_message("Ошибка", "Логин должен содержать до 20 символов.")
            self.login_input.clear()
            self.set_input_enabled(False, self.password_input)
            return

        self.set_input_enabled(True, self.password_input)

    # Проверки для поля "Пароль"
    def check_password_input(self):
        password = self.password_input.text()

        # Проверка длины пароля
        if len(password) > 255:
            self.show_message("Ошибка", "Поле «Пароль» не должно превышать 255 символов.")
            self.password_input.clear()
            return

    # Проверки для кнопки регистрации
    def register(self):
        name = self.name_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        # Проверка на заполненность всех полей
        if not name or not login or not password:
            self.show_message("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверка на существование пользователя с таким логином
        if self.db.get_user(login):
            self.show_message("Ошибка", "Пользователь с таким логином уже существует.")
            return

        # Регистрация пользователя в базе данных
        self.db.register_user(login, name, password)
        self.show_message("Успех", "Регистрация прошла успешно!")
        self.close()

    # Метод для отображения сообщений пользователю
    def show_message(self, title, message):
        msg = QMessageBox() # Создаем новое окно сообщения
        msg.setIcon(QMessageBox.Icon.Critical if "Ошибка" in title else QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    # Утилита для включения/выключения нескольких полей ввода
    def set_input_enabled(self, enabled, *inputs):
        # Устанавливаем состояние (включено/выключено) для каждого поля ввода
        for input_field in inputs:
            input_field.setEnabled(enabled)