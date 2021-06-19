from Config import *


class Sqlighter():


    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

########################################################################################################################

    def commit(self):
        """Сохраняем изменения, внесённые в базу"""
        with self.connection:
            return self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

########################################################################################################################

    def check_abuse_db(self, id):
        """Проверяем есть ли пользователь в базе"""
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM Coingecko where Id ={id}")

########################################################################################################################

    def update_email(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Email=? WHERE id={id}', (data,))

    def update_password(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Password=? WHERE id={id}', (data,))

    def update_amount(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Amount=? WHERE id={id}', (data,))

    def update_host(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Host=? WHERE id={id}', (data,))

    def update_port(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Port=? WHERE id={id}', (data,))

    def update_proxy_login(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Proxy_username=? WHERE id={id}', (data,))

    def update_proxy_password(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET Proxy_password=? WHERE id={id}', (data,))

    def update_user_agent(self, data, id):
        """Обновляем данные в таблице"""
        with self.connection:
            return self.cursor.execute(f'UPDATE Coingecko SET User_agent=? WHERE id={id}', (data,))
########################################################################################################################

    def get_max_accounts(self):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM Config WHERE settings_id=1")

    def update_max_account(self, new_data):
        with self.connection:
            return self.cursor.execute(f"UPDATE Config SET Acc_num=? WHERE settings_id=1", (new_data,))

########################################################################################################################

    def report(self):
        """Выводим все аккаунты и их балансы"""
        summ = 0
        with self.connection:
            for data in self.cursor.execute('SELECT * FROM Coingecko'):
                print(f'[{str(data[1])}] >> Баланс: {str(data[3])}.')
                summ += data[3]
        print(f'\nСумма конфет на всех аккаунтах: {str(summ)}.')



########################################################################################################################

    def add_user_coingecko(self, email, password, host, port, proxy_username, proxy_password):
        """Добавляем данные в таблицу Coingecko"""
        amount = 0
        with self.connection:
            self.cursor.execute(f'INSERT INTO Coingecko (Email, Password, Amount, Host, Port, Proxy_username, Proxy_password) VALUES(?, ?, ?, ?, ?, ?, ?)', (email, password, amount, host, port, proxy_username, proxy_password))

########################################################################################################################
########################################################################################################################

    def create_table_abuse(self):
        """Создаём таблицу Coingecko"""
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS Coingecko
                                          (Id INTEGER PRIMARY KEY,
                                          Email TEXT NOT NULL,
                                          Password TEXT NOT NULL,
                                          Amount INTEGER,
                                          Host TEXT,
                                          Port TEXT,
                                          Proxy_username TEXT,
                                          Proxy_password TEXT,
                                          User_agent TEXT
                                          )""")
