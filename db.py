import sqlite3 # Импортируем модуль для работы с SQLite базой данных
import bcrypt # Импортируем библиотеку для безопасного хеширования паролей с солью

class DB:
    def __init__(self):
        # Инициализация соединения с базой данных
        self.conn = sqlite3.connect("finance_app.db") # Устанавливаем соединение с базой данных (или создаем ее, если она не существует)
        self.cur = self.conn.cursor() # Создаем курсор для выполнения SQL-запросов
        self.conn.execute("PRAGMA foreign_keys = ON;") # Включаем поддержку внешних ключей в базе данных
        self.create_table() # Вызываем метод для создания необходимых таблиц

    # Метод для создания таблиц
    def create_table(self):
        # Таблица пользователи
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            login TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        );
        """)

        # Таблица транзакций
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS transact (
            ID_transact INTEGER PRIMARY KEY AUTOINCREMENT,                                           
            description TEXT,                             
            amount REAL,                                         
            date DATE,                                          
            type TEXT CHECK(type IN ('доход', 'расход')),
            login TEXT,
            FOREIGN KEY (login) REFERENCES user (login)
        );
        """)

        # Таблица отчетов
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS report (
            ID_report INTEGER PRIMARY KEY AUTOINCREMENT,                                         
            name TEXT,
            start_date DATE,                                    
            end_date DATE,
            login TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,                                   
            FOREIGN KEY (login) REFERENCES user (login)     
        );
        """)

        # Таблица файлов
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            ID_file INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES report (ID_report)
        );
        """)

        self.conn.commit() # Сохраняем изменения в базе данных

    # ПОЛЬЗОВАТЕЛИ
    # Получение всех пользователей из базы данных
    def get_all_users(self):
        self.cur.execute("SELECT * FROM user") # Выполняем запрос на выборку всех пользователей
        return self.cur.fetchall() # Возвращаем все найденные записи

    # Регистрация пользователя
    def register_user(self, login, name, password):
        # Хешируем пароль с использованием bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Вставляем нового пользователя в таблицу пользователей
        self.cur.execute("INSERT INTO user (login, name, password) VALUES (?, ?, ?)",
                         (login, name, password_hash))
        self.conn.commit() # Сохраняем изменения в базе данных

    # Получение информации о пользователе по логину
    def get_user(self, login):
        # Выполняем запрос на выборку пользователя с указанным логином
        self.cur.execute("SELECT * FROM user WHERE login = ?", (login,))
        return self.cur.fetchone() # Возвращаем первую найденную запись

    # Проверка пароля пользователя
    def verify_password(self, stored_hash, input_password):
        # Сравниваем введенный пароль с хешем, хранящимся в базе данных
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)

    # ТРАНЗАКЦИИ
    # Добавление новой транзакции в базу данных
    def add_transaction(self, description, amount, date, type_, login):
        # Вставляем новую транзакцию
        self.cur.execute("INSERT INTO transact (description, amount, date, type, login) VALUES (?, ?, ?, ?, ?)",
                         (description, amount, date, type_, login))
        self.conn.commit() # Сохраняем изменения в базе данных

    # Получение всех транзакций текущего пользователя
    def get_user_transactions(self, login):
        # Выполняем запрос на выборку транзакций пользователя
        self.cur.execute("SELECT * FROM transact WHERE login = ?", (login,))
        return self.cur.fetchall() # Возвращаем все найденные транзакции

    # Получение транзакции по ID для конкретного пользователя
    def get_transaction_by_id(self, txn_id, login):
        # Выполняем запрос на выборку транзакции по ID
        self.cur.execute("SELECT * FROM transact WHERE ID_transact = ? AND login = ?", (txn_id, login))
        return self.cur.fetchone() # Возвращаем первую найденную запись

    # Обновление транзакции по ID
    def update_transaction(self, txn_id, description, amount, date, type_, login):
        # Обновляем данные транзакции
        self.cur.execute(
            "UPDATE transact SET description = ?, amount = ?, date = ?, type = ? WHERE ID_transact = ? AND login = ?",
            (description, amount, date, type_, txn_id, login))
        self.conn.commit() # Сохраняем изменения в базе данных

    # Удаление транзакции по ID
    def delete_transaction(self, txn_id, login):
        try:
            # Выполняем запрос на удаление транзакции
            self.cur.execute("DELETE FROM transact WHERE ID_transact = ? AND login = ?", (txn_id, login))
            # Проверяем количество затронутых строк, если строка не была удалена, вернем False
            if self.cur.rowcount == 0:
                return False # Возвращаем False, если транзакция не найдена
            self.conn.commit() # Сохраняем изменения в базе данных
            return True # Возвращаем True, если транзакция была успешно удалена
        except Exception as e:
            # Обрабатываем возможные ошибки
            print(f"Ошибка при удалении транзакции: {e}")
            return False # В случае ошибки возвращаем False

    # Получение доходов и расходов за определенный период
    def get_income_expense_by_period(self, start_date, end_date, login):
        # Выполняем запрос на выборку сумм доходов и расходов
        self.cur.execute("SELECT type, SUM(amount) FROM transact WHERE date BETWEEN ? AND ? AND login = ? GROUP BY type",
                         (start_date, end_date, login))
        return self.cur.fetchall() # Возвращаем все найденные записи

    # Добавление нового отчета
    def add_report(self, name, start_date, end_date, login):
        # Вставляем новый отчет
        self.cur.execute("INSERT INTO report (name, start_date, end_date, login) VALUES (?, ?, ?, ?)",
                         (name, start_date, end_date, login))
        self.conn.commit() # Сохраняем изменения в базе данных
        return self.cur.lastrowid # Возвращаем ID созданного отчета

    # Добавление файла, связанного с отчетом
    def add_file(self, report_id, file_name, file_path):
        # Вставляем запись о файле
        self.cur.execute("INSERT INTO files (report_id, file_name, file_path) VALUES (?, ?, ?)",
                         (report_id, file_name, file_path))
        self.conn.commit() # Сохраняем изменения в базе данных

    # Получение последнего ID отчета
    def get_last_report_id(self):
        # Выполняем запрос на получение максимального ID отчета
        self.cur.execute("SELECT MAX(ID_report) FROM report")
        return self.cur.fetchone()[0] # Возвращаем найденный ID

    # Закрытие соединения с базой данных
    def close(self):
        self.conn.close() # Закрываем соединение с базой данных