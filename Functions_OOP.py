from Config import *

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def sleep():
    time.sleep(random.randint(5, 60))

def collect(id):
    while True:
        # Создаём экземпляр сессии, передавая порядковый номер аккаунта
        coingecko_session = Coingecko(id=id)

        # Получаем результат попытки логина
        log_in_result = coingecko_session.log_in()

        # Если успех, то собираем монеты
        if log_in_result:
            coingecko_session.collect_candies()

        # Если круг окончен, то выходим из цикла
        if log_in_result == 'over':
            break

        id += 1

class Coingecko:
    '''Класс Coingecko'''

    def __init__(self, id):
        """Инициализация сессии"""

        try:
            # Вытаскиваем данные из БД
            self.login = db.check_abuse_db(id=id).fetchone()[1]
            self.password = db.check_abuse_db(id=id).fetchone()[2]
            self.hostname = db.check_abuse_db(id=id).fetchone()[4]
            self.port = db.check_abuse_db(id=id).fetchone()[5]
            self.proxy_username = db.check_abuse_db(id=id).fetchone()[6]
            self.proxy_password = db.check_abuse_db(id=id).fetchone()[7]
            self.headers = db.check_abuse_db(id=id).fetchone()[8]
            if self.headers is None:

                # Генерируем user-agent, если в БД пустой
                self.headers = fake_useragent.UserAgent().random
                db.update_user_agent(data=self.headers, id=id)
                db.commit()

            # Генерируем сессию
            self.proxy = {
                'http': f'http://{self.proxy_username}:{self.proxy_password}@{self.hostname}:{self.port}',
                'https': f'http://{self.proxy_username}:{self.proxy_password}@{self.hostname}:{self.port}'
            }
            self.headers = {
                'user-agent': self.headers
            }
            self.session = requests.Session()
            self.session.proxies = self.proxy
        except:
            print(f'\n[{get_time()}] >> Сбор конфет - круг пройден.\n')


    def log_in(self):
        """Функция авторизации на сайте"""

        try:
            login_link = 'https://www.coingecko.com/account/sign_in?locale=en'

            # отправляем запрос, чтобы получить Auth_token
            response = self.session.get(url=login_link, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
            login_data = {
                'utf8': "✓",
                'authenticity_token': csrf_token,
                'user[redirect_to]': "",
                'user[email]': self.login,
                'user[password]': self.password,
                'user[remember_me]': {
                    0: '0',
                    1: '1'
                },
                'commit': "Log+in"
            }

            # отправляем запрос логина
            login_request = self.session.post(url=login_link, data=login_data, headers=self.headers)

            if login_request.ok:

                # Пытаемся найти форму логина, если не получилось пройти авторизацию
                soup = BeautifulSoup(login_request.text, 'lxml')
                error = soup.find('div', {'class': "card col-lg-4 mx-auto mt-5"})

                if error is None:
                    print(f'[{get_time()}] >> [{self.login}] >> Успешный логин.', end=' ')
                    sleep()
                    return True
                else:
                    print(f'[{get_time()}] >> [{self.login}] >> '
                          f'При входе в аккаунт произошла ошибка. Возможно, указан не верный пароль или логин.')
                    return False
            else:
                print(f'[{get_time()}] >> [{self.login}] >> '
                      f'При входе в аккаунт произошла ошибка при получении запроса.')
                return False
        except:
            self.over = True
            return 'over'


    def __get_token(self):
        """Функция получения токена для сбора монет"""
        url = 'https://www.coingecko.com/account/candy?locale=en'
        auth_token_request = self.session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(auth_token_request.text, 'lxml')
        try:
            auth_token = soup.find('input', {'name': 'authenticity_token'})['value']
            sleep()
            return auth_token
        except:
            return False

    def collect_candies(self):
        """Функция сбора монет"""

        try:
            # Получаем токен для авторизации запроса
            auth_token = self.__get_token()
            balance_check_link = 'https://www.coingecko.com/account/candy?locale=en'

            # Если токен не ложный, начинаем процесс сбора конфет
            if auth_token is not False:
                collect_candies_link = 'https://www.coingecko.com/account/candy/daily_check_in?locale=en'

                # Отправляем запрос на сбор конфет
                data = {
                    'authenticity_token': auth_token
                }
                collect_request = self.session.post(url=collect_candies_link, headers=self.headers, data=data)

                # Проверяем ответ
                if collect_request.ok:
                    print(f'Собрал токены.', end=' ')
                    # Получаем баланс и обновляем значение в БД
                    balance_request = self.session.get(url=balance_check_link, headers=self.headers)
                    soup = BeautifulSoup(balance_request.text, 'lxml')
                    balance = soup.find('div', {'data-target': 'points.balance'}).text
                    db.update_amount(data=str(balance), id=id)
                    db.commit()
                    print(f'Баланс: {balance} конфет.')
                    sleep()
                else:
                    print(f'При сборе конфет произошла неизвестная ошибка.')

            # Если токен ложный, конфеты нельзя собрать
            else:
                # Получаем баланс и обновляем значение в БД
                balance_request = self.session.get(url=balance_check_link, headers=self.headers)

                # Проверяем ответ
                if balance_request.ok:
                    soup = BeautifulSoup(balance_request.text, 'lxml')
                    balance = soup.find('div', {'data-target': 'points.balance'}).text
                    db.update_amount(data=str(balance), id=id)
                    db.commit()
                    print(f'Сегодня монеты уже собирались, баланс остался прежним: {balance} конфет.')
                    sleep()
                else:
                    print(f'При сборе конфет произошла неизвестная ошибка.')
        except:
            if not self.over:
                print(f'При сборе конфет произошла неизвестная ошибка.')

collect(1)