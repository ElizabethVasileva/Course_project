from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit, QMessageBox
from PyQt6.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Импорт для работы с графиками
from matplotlib.figure import Figure # Импорт для создания фигур графиков
from design import setup_label_style_r, setup_input_style_t, setup_button_style_t
import pandas as pd # Импорт библиотеки pandas для работы с данными
import os # Импорт модуля для работы с файловой системой
import subprocess # Импорт модуля для выполнения системных команд
import sys # Импорт модуля для работы с системой

class ReportWindow(QWidget):
    def __init__(self, db, login):
        super().__init__()
        self.db = db
        self.login = login
        self.last_report_id = None # Атрибут для хранения ID последнего отчета
        self.initUI()

    def initUI(self):
        self.setFixedSize(780, 500)
        layout = QVBoxLayout() # Создание вертикального компоновщика для основного содержимого
        main_layout = QHBoxLayout() # Создание горизонтального компоновщика для ввода данных и графиков
        input_group_layout = QVBoxLayout() # Создание вертикального компоновщика для меток и полей ввода
        button_layout = QVBoxLayout() # Создание вертикального компоновщика для кнопок

        # Метка для названия отчета
        self.name_label = QLabel("Название отчета:", self)
        setup_label_style_r(self.name_label)

        # Поле для ввода названия отчета
        self.name_input = QLineEdit(self)
        setup_input_style_t(self.name_input)

        # Добавление метки и поля ввода в вертикальный компоновщик
        input_group_layout.addWidget(self.name_label)
        input_group_layout.addWidget(self.name_input)

        # Метка для выбора даты начала
        self.start_date_label = QLabel("Дата начала:", self)
        setup_label_style_r(self.start_date_label)

        # Поле ввода даты начала
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDate(QDate.currentDate()) # Установка текущей даты по умолчанию
        self.start_date_input.setCalendarPopup(True) # Включение всплывающего календаря
        setup_input_style_t(self.start_date_input)

        # Добавление метки и поля ввода в вертикальный компоновщик
        input_group_layout.addWidget(self.start_date_label)
        input_group_layout.addWidget(self.start_date_input)

        # Метка для выбора даты окончания
        self.end_date_label = QLabel("Дата окончания:", self)
        setup_label_style_r(self.end_date_label)

        # Поле ввода даты начала
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        setup_input_style_t(self.end_date_input)

        # Добавление метки и поля ввода в вертикальный компоновщик
        input_group_layout.addWidget(self.end_date_label)
        input_group_layout.addWidget(self.end_date_input)

        # Добавление вертикального компоновщика с метками и полями ввода в основной горизонтальный компоновщик
        main_layout.addLayout(input_group_layout)

        # Создание пространства для отображения графиков
        self.canvas = FigureCanvas(Figure()) # Создание холста для графиков
        main_layout.addWidget(self.canvas) # Добавление холста в основной компоновщик

        # Добавление основного компоновщика в общий компоновщик
        layout.addLayout(main_layout)

        # Кнопка для генерации отчета
        self.generate_report_button = QPushButton("Сгенерировать отчет", self)
        setup_button_style_t(self.generate_report_button)
        self.generate_report_button.clicked.connect(self.generate_report)
        button_layout.addWidget(self.generate_report_button)

        # Кнопка для сохранения диаграммы
        self.save_chart_button = QPushButton("Сохранить диаграмму", self)
        setup_button_style_t(self.save_chart_button)
        self.save_chart_button.clicked.connect(self.save_chart)
        button_layout.addWidget(self.save_chart_button)

        # Кнопка для экспорта в Excel
        self.export_excel_button = QPushButton("Экспортировать в Excel", self)
        setup_button_style_t(self.export_excel_button)
        self.export_excel_button.clicked.connect(self.export_to_excel)
        button_layout.addWidget(self.export_excel_button)

        # Кнопка для открытия папки с отчетами
        self.open_reports_folder_button = QPushButton("Открыть папку с отчетами", self)
        setup_button_style_t(self.open_reports_folder_button)
        self.open_reports_folder_button.clicked.connect(self.open_reports_folder)
        button_layout.addWidget(self.open_reports_folder_button)

        # Кнопка для открытия папки с диаграммами
        self.open_diagrams_folder_button = QPushButton("Открыть папку с диаграммами", self)
        setup_button_style_t(self.open_diagrams_folder_button)
        self.open_diagrams_folder_button.clicked.connect(self.open_diagrams_folder)
        button_layout.addWidget(self.open_diagrams_folder_button)

        # Добавляем вертикальный компоновщик с кнопками в основной вертикальный компоновщик
        input_group_layout.addLayout(button_layout)

        self.setLayout(layout)

    # Метод для генерации отчета (диаграмма)
    def generate_report(self):
        name = self.name_input.text().strip()
        start_date = self.start_date_input.date().toString("yyyy.MM.dd")
        end_date = self.end_date_input.date().toString("yyyy.MM.dd")

        # Проверка на пустое поле названия отчета
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название отчета должно быть заполнено!")
            return

        # Проверка длины названия отчета: не более 50 символов
        if len(name) > 50:
            QMessageBox.warning(self, "Ошибка", "Название отчета не может превышать 50 символов.")
            self.name_input.clear()
            return

        # Запрашиваем данные о доходах и расходах за указанный период из базы данных
        results = self.db.get_income_expense_by_period(start_date, end_date, self.login)

        # Проверяем, есть ли результаты запроса
        if not results:
            # Если нет транзакций за указанный период, выводим предупреждение пользователю
            QMessageBox.warning(self, "Ошибка", "Нет транзакций за указанный период!")
            return

        # Инициализируем переменные для хранения суммарных значений доходов и расходов
        income = 0.0
        expense = 0.0

        # Проходим по результатам и суммируем доходы и расходы
        for type_, total in results:
            # Если тип 'доход', добавляем сумму к переменной income
            if type_ == 'доход':
                income += total  # Используем += для суммирования
            # Если тип 'расход', добавляем сумму к переменной expense
            elif type_ == 'расход':
                expense += total  # Используем += для суммирования

        # Построение круговой диаграммы
        self.canvas.figure.clear() # Очищаем предыдущую фигуру на холсте
        ax = self.canvas.figure.add_subplot(111)

        # Определяем метки и размеры для круговой диаграммы
        labels = ['Доходы', 'Расходы']
        sizes = [income, expense]
        colors = ['#4CAF50', '#FF5733']

        # Функция для форматирования текста на диаграмме
        def func(pct, allvalues):
            # Вычисляем абсолютное значение для каждого сегмента без округления
            absolute = pct / 100. * sum(allvalues)
            # Возвращаем строку с процентом и абсолютным значением, форматируя абсолютное значение
            return f'{pct:.1f}%\n{absolute:.2f} руб.'

        # Строим круговую диаграмму с заданными параметрами
        ax.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: func(pct, sizes), startangle=140)
        ax.axis('equal') # Обеспечиваем равные оси для правильного отображения круговой диаграммы
        ax.set_title(f"Доходы и Расходы за период: {start_date} - {end_date}") # Устанавливаем заголовок диаграммы

        # Обновляем холст, чтобы отобразить новую диаграмму
        self.canvas.draw()

        # Сохраняем отчет в базу данных и получаем ID нового отчета
        self.last_report_id = self.db.add_report(self.name_input.text(), start_date, end_date, self.login)

    # Метод для сохранения диаграммы
    def save_chart(self):
        name = self.name_input.text().strip()
        # Проверка на пустое поле названия отчета
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название отчета должно быть заполнено!")
            return
        # Проверка длины названия отчета: не более 50 символов
        if len(name) > 50:
            QMessageBox.warning(self, "Ошибка", "Название отчета не может превышать 50 символов.")
            self.name_input.clear()
            return
        # Проверяем, был ли сгенерирован отчет
        if self.last_report_id is None:
            # Если отчет не был сгенерирован, отображаем предупреждение пользователю
            QMessageBox.warning(self, "Ошибка", "Сначала сгенерируйте отчет, прежде чем сохранять диаграмму.")
            return

        # Определяем папку для сохранения диаграмм, используя текущую рабочую директорию
        reports_folder = os.path.join(os.getcwd(), 'diagrams') # Создаем папку 'diagrams', если она не существует
        os.makedirs(reports_folder, exist_ok=True) # Параметр exist_ok=True предотвращает ошибку, если папка уже существует
        # Формируем имя файла для сохранения диаграммы
        file_name = f"диаграмма_{self.name_input.text()}.png" # Имя файла диаграммы, основанное на введенном пользователем названии
        file_path = os.path.join(reports_folder, file_name) # Полный путь к файлу, включая имя файла и папку
        # Сохраняем диаграмму в файл
        self.canvas.figure.savefig(file_path, bbox_inches='tight') # Сохраняем текущую фигуру на холсте в указанный файл
        QMessageBox.information(self, "Успех", f"Диаграмма сохранена в {file_path}!") # Информируем пользователя об успешном сохранении диаграммы

        # Сохраняем информацию о файле в базе данных
        self.db.add_file(self.last_report_id, file_name, file_path) # Добавляем запись о сохраненном файле в базу данных

    # Метод для экспорта отчета в Excel
    def export_to_excel(self):
        name = self.name_input.text().strip()
        # Проверка на пустое поле названия отчета
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название отчета должно быть заполнено!")
            return
        # Проверка длины названия отчета: не более 50 символов
        if len(name) > 50:
            QMessageBox.warning(self, "Ошибка", "Название отчета не может превышать 50 символов.")
            self.name_input.clear()
            return
        # Проверяем, был ли сгенерирован отчет
        if self.last_report_id is None:
            # Если отчет не был сгенерирован, выводим предупреждение пользователю
            QMessageBox.warning(self, "Ошибка", "Сначала сгенерируйте отчет, прежде чем экспортировать в Excel.")
            return
        # Получаем даты начала и конца из пользовательского ввода и форматируем их
        start_date = self.start_date_input.date().toString("yyyy.MM.dd")
        end_date = self.end_date_input.date().toString("yyyy.MM.dd")
        # Извлекаем все транзакции пользователя из базы данных
        transactions = self.db.get_user_transactions(self.login)
        # Фильтруем транзакции по дате, выбирая только те, которые попадают в указанный диапазон
        filtered_transactions = [txn for txn in transactions if start_date <= txn[3] <= end_date]
        data = { # Создаем словарь для хранения данных для экспорта в Excel
            'Описание': [],
            'Сумма, руб': [],
            'Дата': [],
            'Тип': []
        }

        # Инициализация переменных для подсчета общей суммы доходов и расходов
        income = 0
        expense = 0
        # Обрабатываем каждую отфильтрованную транзакцию
        for txn in filtered_transactions:
            description = txn[1]
            amount = txn[2]
            date = txn[3]
            type_ = txn[4]

            # Заполняем словарь данными транзакции
            data['Описание'].append(description)
            data['Сумма, руб'].append(amount)
            data['Дата'].append(date)
            data['Тип'].append(type_)

            # Подсчитываем общую сумму доходов и расходов
            if type_ == 'доход':
                income += amount # Увеличиваем сумму доходов
            elif type_ == 'расход':
                expense += amount # Увеличиваем сумму расходов

        df = pd.DataFrame(data)
        # Создаем данные для итогового отчета
        summary_data = {
            'Описание': ['Общая сумма доходов, руб.', 'Общая сумма расходов, руб.'],
            'Сумма, руб.': [income, expense],
            'Дата': ['', ''],
            'Тип': ['', '']
        }
        summary_df = pd.DataFrame(summary_data)
        final_df = pd.concat([df, summary_df], ignore_index=True)
        # Определяем папку для сохранения отчетов, используя текущую рабочую директорию
        reports_folder = os.path.join(os.getcwd(), 'reports')
        os.makedirs(reports_folder, exist_ok=True) # Создаем папку 'reports', если она не существует
        # Формируем имя файла для сохранения отчета
        file_name = f"отчет_{self.name_input.text()}.xlsx" # Имя файла основано на введенном пользователем названии
        file_path = os.path.join(reports_folder, file_name) # Полный путь к файлу
        # Экспортируем собранные данные в Excel-файл
        final_df.to_excel(file_path, index=False)
        QMessageBox.information(self, "Успех", f"Отчет экспортирован в {file_path}!") # Информируем пользователя об успешном экспорте отчета

        self.db.add_file(self.last_report_id, file_name, file_path) # Сохраняем информацию о файле в базе данных

    # Метод для открытия папки с отчетами
    def open_reports_folder(self):
        # Определяем путь к папке с отчетами, которая находится в текущем рабочем каталоге
        reports_folder = os.path.join(os.getcwd(), 'reports')
        # Проверяем, существует ли папка с отчетами
        if os.path.exists(reports_folder):
            # Если Windows
            if sys.platform == "win32":
                subprocess.Popen(f'explorer "{reports_folder}"')
            # Для Linux
            else:
                subprocess.Popen(['xdg-open', reports_folder])
        else:
            # Если папка с отчетами не найдена, выводим предупреждение пользователю
            QMessageBox.warning(self, "Ошибка", "Папка с отчетами не найдена! Пожалуйста, создайте хотя бы один отчет.")

    # Метод для открытия папки с диаграммами
    def open_diagrams_folder(self):
        # Определяем путь к папке с диаграммами, которая находится в текущем рабочем каталоге
        diagrams_folder = os.path.join(os.getcwd(), 'diagrams')
        # Проверяем, существует ли папка с диаграммами
        if os.path.exists(diagrams_folder):
            # Если Windows
            if sys.platform == "win32":
                subprocess.Popen(f'explorer "{diagrams_folder}"')
            # Для Linux
            else:
                subprocess.Popen(['xdg-open', diagrams_folder]) # Открываем папку с диаграммами с помощью команды 'xdg-open'
        else:
            # Если папка с диаграммами не найдена, выводим предупреждение пользователю
            QMessageBox.warning(self, "Ошибка", "Папка с диаграммами не найдена! Пожалуйста, создайте хотя бы одну диаграмму.")