# ДЛЯ РЕГИСТРАЦИИ И АВТОРИЗАЦИИ
# Метки
def setup_label_style(label):
    label.setStyleSheet("""
        QLabel {
            font-size: 15px;
            color: #00796b;
            margin-top: 10px;
            margin-bottom: 5px;
            font-weight: bold;
        }
    """)

# Поля ввода
def setup_input_style(input_field):
    input_field.setStyleSheet("""
        QLineEdit {
            background-color: #ffffff;
            border: 2px solid #00796b;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            color: #004d40;
            font-family: Arial, sans-serif;
        }
        QLineEdit:focus {
            border: 2px solid #004d40;
            color: #004d40;
        }
        QLineEdit:disabled {
            background-color: #e0f7fa;
            border: 2px solid #b0bec5;
            color: #90a4ae;
        }
        QLineEdit::placeholder {
            color: #80cbc4;
        }
    """)

# Кнопки
def setup_button_style(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #00796b;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #004d40;
        }
        QPushButton:pressed {
            background-color: #003d33;
        }
    """)

# ДЛЯ ГЛАВНОГО ОКНА
# Кнопки setup_button_style
# Активная кнопка
def setup_button_style_active(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #800000;
            color: white;
            border: none;
            padding: 10px;
            font-size: 14px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5e0000;
        }
    """)

# ДЛЯ ОКНА ТРАНЗАКЦИЙ
# Метки setup_label_style
# Поля ввода
def setup_input_style_t(input_field):
    input_field.setStyleSheet("""
        QLineEdit, QComboBox, QDateEdit {
            background-color: #ffffff;
            border: 2px solid #00796b;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: #004d40;
            font-family: Arial, sans-serif;
            min-height: 30px;  /* Минимальная высота для удобства ввода */
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 2px solid #004d40;
            color: #004d40;
        }
        QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled {
            background-color: #e0f7fa;
            border: 2px solid #b0bec5;
            color: #90a4ae;
        }
        QLineEdit::placeholder, QComboBox::placeholder, QDateEdit::placeholder {
            color: #80cbc4;
        }
    """)

# Кнопки
def setup_button_style_t(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #00796b;
            color: white;
            border: 2px solid #00796b;
            padding: 10px 24px;
            border-radius: 8px;  /* Округленные углы */
            font-weight: bold;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s ease;  /* Плавные переходы */
        }
        QPushButton:hover {
            background-color: #004d40;
            border: 2px solid #004d40;
        }
        QPushButton:pressed {
            background-color: #003d33;
            border: 2px solid #003d33;
        }
        QPushButton:disabled {
            background-color: #b0bec5;
            border: 2px solid #b0bec5;
            color: #90a4ae;
        }
    """)

# Таблица
def setup_table_style(table):
    table.setStyleSheet("""
        QTableWidget {
            border: 2px solid #ddd;
            border-radius: 5px;
            background-color: #f5f5f5;
            font-size: 14px;
        }
        QTableWidget::item {
            padding: 16px;
        }
        QHeaderView::section {
            background-color: #00796b;
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 5px;
            border: 1px solid #ccc;
        }
    """)

# ДЛЯ ОКНА ОТЧЕТОВ
# Метки
def setup_label_style_r(label):
    label.setStyleSheet("""
        QLabel {
            font-size: 15px;
            color: #00796b;
            margin-top: 10px;
            margin-bottom: 1px;
            font-weight: bold;
        }
    """)

# Поля ввода setup_input_style_t
# Кнопки setup_button_style_t