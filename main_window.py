from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QStackedWidget, QLabel, QTextEdit
from PyQt6.QtCore import Qt # Импортируем Qt для использования AlignmentFlag
from transaction_window import TransactionWindow # Импортируем класс окна транзакций
from report_window import ReportWindow # Импортируем класс окна отчетов
from design import setup_button_style, setup_button_style_active # Импортируем функции для настройки стилей кнопок

class MainWindow(QWidget):
    def __init__(self, db, login):
        super().__init__()
        self.login = login # Сохраняем логин пользователя
        self.db = db  # Сохраняем ссылку на объект базы данных
        self.active_button = None # Инициализируем переменную для хранения активной кнопки
        self.initUI()

    def initUI(self):
        # Заголовок окна
        self.setWindowTitle("Система учета личных финансов")
        self.setFixedSize(800, 600)
        main_layout = QVBoxLayout()

        # Верхнее меню
        self.top_menu = QFrame(self)
        self.top_menu.setFixedHeight(70) # Устанавливаем фиксированную высоту для меню
        self.top_menu.setStyleSheet("background-color: #2d3e50; color: white;")
        top_menu_layout = QHBoxLayout() # Создаем горизонтальный компоновщик для кнопок меню

        # Кнопка "Транзакции"
        self.transaction_button = QPushButton("Транзакции")
        setup_button_style(self.transaction_button)
        self.transaction_button.clicked.connect(self.show_transaction_window)
        self.transaction_button.clicked.connect(lambda: self.change_button_style(self.transaction_button)) # Меняем стиль кнопки при нажатии
        top_menu_layout.addWidget(self.transaction_button)

        # Кнопка "Отчеты"
        self.report_button = QPushButton("Отчеты")
        setup_button_style(self.report_button)
        self.report_button.clicked.connect(self.show_report_window)
        self.report_button.clicked.connect(lambda: self.change_button_style(self.report_button)) # Меняем стиль кнопки при нажатии
        top_menu_layout.addWidget(self.report_button)

        self.top_menu.setLayout(top_menu_layout) # Устанавливаем компоновщик для верхнего меню

        # Центральная область для контента
        self.central_widget = QStackedWidget(self) # Создаем стековый виджет для переключения между окнами

        # Создаем виджет с приветственным сообщением
        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_widget) # Создаем вертикальный компоновщик для приветственного виджета

        # Метка с приветствием
        self.welcome_label = QLabel("Добро пожаловать в приложение для учета личных финансов!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Центрируем текст метки
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        # Текстовое поле для информации
        self.info_text = QTextEdit()
        self.info_text.setText(
            "    Добро пожаловать в наше приложение для отслеживания доходов и расходов!\n"
            "    Это приложение создано для того, чтобы предоставить вам удобный и эффективный способ управления вашими финансами. "
            "Вы сможете легко добавлять транзакции, получая детальную информацию о каждой операции.\n"
            "    Основные функции приложения:\n"
            "    1. Добавление транзакций: Легко фиксируйте свои доходы и расходы, указывая необходимые детали, такие как сумма, описание и дата.\n"
            "    2. Анализ финансов: На основании введенных данных приложение генерирует наглядные отчеты, которые помогут вам лучше понять свои финансовые потоки.\n"
            "    3. Экспорт данных: Вы можете экспортировать свои финансовые данные в формате Excel. Это позволит делиться информацией с другими или проводить более углубленный анализ в удобном для вас формате.\n"
            "    Используйте меню сверху, чтобы легко навигировать по всем возможностям приложения. В каждом разделе вы найдете полезные инструменты для управления вашими финансами.\n"
            "    Удачного использования! Пусть контроль над финансами станет для вас простым и приятным процессом!"
        )
        self.info_text.setReadOnly(True) # Делаем текстовое поле только для чтения, чтобы пользователь не мог редактировать текст
        self.info_text.setStyleSheet("font-size: 18px; color: #00575b; background-color: #ecf0f1; padding: 10px; border: 2px solid #bdc3c7; border-radius: 5px;")

        # Добавляем метку и текстовое поле в компоновщик приветственного виджета
        welcome_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(self.info_text)

        # Добавляем виджет с приветственным сообщением в стек
        self.central_widget.addWidget(self.welcome_widget)
        self.central_widget.setStyleSheet("background-color: #f0f4f7;")

        # Добавляем верхнее меню и центральную область в главный компоновщик
        main_layout.addWidget(self.top_menu)
        main_layout.addWidget(self.central_widget)

        self.setLayout(main_layout) # Устанавливаем главный компоновщик для окна
        self.show() # Показываем главное окно

    # Метод для изменения стиля кнопок при переключении между ними
    def change_button_style(self, button):
        # Если есть активная кнопка
        if self.active_button is not None:
            setup_button_style(self.active_button) # Сбрасываем стиль активной кнопки
        setup_button_style_active(button) # Устанавливаем новый стиль для текущей кнопки
        self.active_button = button # Обновляем ссылку на активную кнопку

    # Метод для отображения окна транзакций
    def show_transaction_window(self):
        # Проверяем все виджеты в стеке
        for i in range(self.central_widget.count()):
            widget = self.central_widget.widget(i) # Получаем текущий виджет
            # Если это окно транзакций
            if isinstance(widget, TransactionWindow):
                self.central_widget.setCurrentWidget(widget) # Устанавливаем его как текущий виджет
                return
        # Если окно транзакций не открыто, создаем и добавляем его
        transaction_window = TransactionWindow(self.db, self.login) # Создаем экземпляр окна транзакций
        self.central_widget.addWidget(transaction_window) # Добавляем окно в стек
        self.central_widget.setCurrentWidget(transaction_window) # Устанавливаем его как текущий виджет

    # Метод для отображения окна отчетов
    def show_report_window(self):
        # Проверяем все виджеты в стеке
        for i in range(self.central_widget.count()):
            widget = self.central_widget.widget(i) # Получаем текущий виджет
            # Если это окно отчетов
            if isinstance(widget, ReportWindow):
                self.central_widget.setCurrentWidget(widget) # Устанавливаем его как текущий виджет
                return
        # Если окно отчетов не открыто, создаем и добавляем его
        report_window = ReportWindow(self.db, self.login) # Создаем экземпляр окна отчетов
        self.central_widget.addWidget(report_window) # Добавляем окно в стек
        self.central_widget.setCurrentWidget(report_window) # Устанавливаем его как текущий виджет