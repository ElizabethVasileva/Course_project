from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QDate
from design import setup_label_style, setup_input_style_t, setup_button_style_t, setup_table_style

class TransactionWindow(QWidget):
    def __init__(self, db, login):
        super().__init__()
        self.db = db # Сохранение ссылки на объект базы данных
        self.login = login # Сохранение информации о текущем пользователе
        self.selected_txn_id = None # Идентификатор выбранной транзакции (для редактирования)
        self.initUI()

    def initUI(self):
        self.setFixedSize(780, 500)
        layout = QHBoxLayout() # Горизонтальный макет для основного окна
        form_layout = QVBoxLayout() # Вертикальный макет для формы ввода

        # Элементы формы для ввода транзакции
        # Метка для ввода описания транзакции
        self.description_label = QLabel("Описание транзакции:", self)
        setup_label_style(self.description_label)

        # Поле для ввода описания транзакции
        self.description_input = QLineEdit(self)
        setup_input_style_t(self.description_input)
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_input)

        # Метка для ввода суммы транзакции
        self.amount_label = QLabel("Сумма транзакции (вид: 0,00):", self)
        setup_label_style(self.amount_label)

        # Поле для ввода суммы транзакции
        self.amount_input = QLineEdit(self)
        setup_input_style_t(self.amount_input)

        double_validator = QDoubleValidator(-99999.99, 99999.99, 2)  # Ограничиваем диапазон значений и количество знаков после запятой
        self.amount_input.setValidator(double_validator)

        form_layout.addWidget(self.amount_label)
        form_layout.addWidget(self.amount_input)

        # Метка для выбора даты транзакции
        self.date_label = QLabel("Дата транзакции:", self)
        setup_label_style(self.date_label)

        # Поле для выбора даты транзакции
        self.date_input = QDateEdit(self)
        self.date_input.setDate(QDate.currentDate()) # Установка текущей даты по умолчанию
        self.date_input.setCalendarPopup(True) # Включение всплывающего календаря
        setup_input_style_t(self.date_input)
        form_layout.addWidget(self.date_label)
        form_layout.addWidget(self.date_input)

        # Метка для выбора типа транзакции
        self.type_label = QLabel("Тип транзакции:", self)
        setup_label_style(self.type_label)

        # Поле для выбора типа транзакции
        self.type_input = QComboBox(self)
        self.type_input.addItems(['расход', 'доход']) # Добавление вариантов в комбобокс
        setup_input_style_t(self.type_input)
        form_layout.addWidget(self.type_label)
        form_layout.addWidget(self.type_input)

        # Кнопка для добавления транзакции
        self.add_transaction_button = QPushButton("Добавить", self)
        setup_button_style_t(self.add_transaction_button)
        self.add_transaction_button.clicked.connect(self.add_transaction)
        form_layout.addWidget(self.add_transaction_button)

        # Кнопка для редактирования транзакции
        self.edit_transaction_button = QPushButton("Редактировать", self)
        setup_button_style_t(self.edit_transaction_button)
        self.edit_transaction_button.clicked.connect(self.edit_transaction)
        form_layout.addWidget(self.edit_transaction_button)

        # Кнопка для удаления транзакции
        self.delete_transaction_button = QPushButton("Удалить", self)
        setup_button_style_t(self.delete_transaction_button)
        self.delete_transaction_button.clicked.connect(self.delete_transaction)
        form_layout.addWidget(self.delete_transaction_button)

        # Таблица для отображения всех транзакций
        self.transaction_table = QTableWidget(self)
        self.transaction_table.setColumnCount(5) # Установка количества столбцов в таблице
        self.transaction_table.setHorizontalHeaderLabels(["ID", "Описание", "Тип", "Сумма, руб.", "Дата"]) # Установка заголовков столбцов
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Установка поведения выбора строк
        self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Запрет на редактирование ячеек таблицы
        self.transaction_table.setColumnHidden(0, True) # Скрываем столбец ID, так как он не нужен для отображения
        self.transaction_table.setFixedSize(453, 470) # Размер таблицы
        setup_table_style(self.transaction_table)

        layout.addLayout(form_layout) # Добавление формы в основной макет
        layout.addWidget(self.transaction_table) # Добавление таблицы в основной макет

        self.load_transactions() # Загружаем транзакции из базы данных

        self.setLayout(layout) # Установка основного макета для виджета

    # Добавление новой транзакции
    def add_transaction(self):
        description = self.description_input.text().strip()
        amount_input = self.amount_input.text().strip()
        date = self.date_input.date().toString("yyyy.MM.dd")
        transaction_type = self.type_input.currentText()

        # Проверка на пустые поля
        if not description or not amount_input:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        # Проверка длины описания: не более 50 символов
        if len(description) > 50:
            QMessageBox.warning(self, "Ошибка", "Описание транзакции не может превышать 50 символов.")
            self.description_input.clear()
            return

        # Проверка, что введена сумма с использованием цифр
        try:
            amount = float(amount_input.replace(',', '.'))
        except ValueError:
            # Если преобразование не удалось (например, введены буквы), показываем предупреждение
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите сумму с использованием цифр (вид: 0,00).")
            self.amount_input.clear()
            return

        # Сумма должна быть больше 0
        if amount <= 0:
            QMessageBox.warning(self, "Ошибка", "Сумма транзакции должна быть больше 0.")
            self.amount_input.clear()
            return

        # Проверяем, выбрана ли существующая транзакция для редактирования
        if self.selected_txn_id is None:
            # Если транзакция новая (т.е. не выбрана для редактирования), добавляем ее в базу данных
            self.db.add_transaction(description, amount, date, transaction_type, self.login)
        else:
            # Если транзакция выбрана для редактирования, обновляем ее в базе данных по ID
            self.db.update_transaction(self.selected_txn_id, description, amount, date, transaction_type, self.login)

        # Очищаем поля ввода после добавления
        self.description_input.clear()
        self.amount_input.clear()
        self.selected_txn_id = None  # Сбрасываем идентификатор выбранной транзакции

        # Загружаем обновленный список транзакций из базы данных и отображаем его в таблице
        self.load_transactions()

    # Редактирование транзакции
    def edit_transaction(self):
        selected_row = self.transaction_table.currentRow() # Получаем индекс выбранной строки в таблице транзакций

        # Проверяем, выбрана ли строка. Если нет, показываем предупреждение
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите транзакцию для редактирования.")
            return

        # Получаем идентификатор транзакции из первой ячейки выбранной строки
        txn_id = int(self.transaction_table.item(selected_row, 0).text())
        # Извлекаем данные транзакции из базы данных по идентификатору
        txn = self.db.get_transaction_by_id(txn_id, self.login)

        # Проверяем, была ли найдена транзакция
        if txn:
            self.selected_txn_id = txn[0] # Сохраняем идентификатор выбранной транзакции для дальнейшего редактирования

            # Заполняем поля ввода данными транзакции
            self.description_input.setText(txn[1]) # Устанавливаем описание транзакции
            self.amount_input.setText(str(txn[2])) # Устанавливаем сумму транзакции
            self.date_input.setDate(QDate.fromString(txn[3], "yyyy.MM.dd")) # Устанавливаем дату транзакции

            amount_str = f"{txn[2]:.2f}"  # Форматируем сумму с двумя знаками после запятой
            self.type_input.setCurrentText(amount_str) # Устанавливаем тип транзакции

    # Удаление транзакции
    def delete_transaction(self):
        selected_row = self.transaction_table.currentRow() # Получаем индекс выбранной строки в таблице транзакций

        # Проверяем, выбрана ли строка. Если нет, показываем предупреждение
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите транзакцию для удаления.")
            return

        # Извлекаем идентификатор транзакции из первой ячейки выбранной строки таблицы
        txn_id = int(self.transaction_table.item(selected_row, 0).text())
        # Вызываем метод удаления транзакции из базы данных, передавая идентификатор и логин пользователя
        success = self.db.delete_transaction(txn_id, self.login)

        # Проверяем, успешно ли была удалена транзакция
        if success:
            # Если удаление прошло успешно, загружаем обновленный список транзакций из базы данных
            self.load_transactions()
        else:
            # Если удаление не удалось, показываем сообщение об ошибке пользователю
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить транзакцию.")

    # Загружаем транзакции текущего пользователя
    def load_transactions(self):
        # Очищаем таблицу, чтобы удалить старые данные перед загрузкой новых транзакций
        self.transaction_table.setRowCount(0)
        # Получаем транзакции текущего пользователя из базы данных
        transactions = self.db.get_user_transactions(self.login)

        # Сортируем транзакции по дате (четвертый элемент в каждой транзакции)
        transactions.sort(key=lambda txn: QDate.fromString(txn[3], "yyyy.MM.dd"))

        # Проходим по каждой транзакции и добавляем её в таблицу
        for txn in transactions:
            # Получаем текущее количество строк в таблице, чтобы добавить новую строку в конец
            row_position = self.transaction_table.rowCount()
            self.transaction_table.insertRow(row_position) # Вставляем новую строку в таблицу

            # Устанавливаем значения для каждой ячейки в новой строке
            self.transaction_table.setItem(row_position, 0, QTableWidgetItem(str(txn[0]))) # Устанавливаем идентификатор транзакции
            self.transaction_table.setItem(row_position, 1, QTableWidgetItem(txn[1])) # Устанавливаем описание транзакции
            self.transaction_table.setItem(row_position, 2, QTableWidgetItem(txn[4])) # Устанавливаем тип транзакции

            # Форматируем сумму, добавляя два знака после запятой, если сумма целая
            amount_str = f"{txn[2]:.2f}"  # Форматируем сумму с двумя знаками после запятой
            self.transaction_table.setItem(row_position, 3, QTableWidgetItem(amount_str)) # Устанавливаем сумму транзакции
            self.transaction_table.setItem(row_position, 4, QTableWidgetItem(txn[3])) # Устанавливаем дату транзакции