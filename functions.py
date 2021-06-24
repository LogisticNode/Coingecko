from config import *

def get_time():
    """Функция получения времени"""
    return datetime.datetime.now().strftime("%H:%M:%S")

def sleep():
    """Функция сна"""
    time.sleep(random.randint(5, 15))

def sleep_between_loop(id):
    """Функция сна между кругами во время выполнения функции 'unlimited_collect'"""
    length = id - 1
    # вычисляем максимальную длительность круга в минутах
    max_time_for_loop = length * 3
    # получаем свободное от 3 обязательных кругов время в минутах
    free_time = 24 * 60 - max_time_for_loop * 3
    # получаем время для 1 отдыха
    sleep_time = int(free_time / 3)
    seconds = int(random.randint(int(sleep_time * 0.7 * 60), int(sleep_time * 1.3 * 60))/2)
    time.sleep(seconds)

def add_user():
    """Функция добавления пользователя в базу данных"""
    db.create_table_abuse()
    email = str(input('Введите почту: '))
    password = str(input('Введите пароль: '))
    host = str(input('Введите ip прокси: '))
    port = str(input('Введите порт прокси: '))
    proxy_username = str(input('Введите логин прокси: '))
    proxy_password = str(input('Введите пароль для прокси: '))
    try:

        print('\nАккаунт будет добавлен после успешной проверки баланса...')
        # id = db.get_id_by_email(email=email)

        # Создаём экземпляр сессии, передавая порядковый номер аккаунта
        coingecko_session = Coingecko(login=email, password=password, hostname=host, port=port, proxy_username=proxy_username, proxy_password=proxy_password)

        # Получаем результат попытки логина
        log_in_result = coingecko_session.log_in()

        # Если успех, то получаем баланс конфет
        if log_in_result == True:
            get_balance_result = coingecko_session.get_balance()
            balance = get_balance_result[0]
            user_agent = get_balance_result[1]['user-agent']
            db.add_user_coingecko(email=email, password=password, host=host, port=port, proxy_username=proxy_username,
                                  proxy_password=proxy_password, amount=balance, user_agent=user_agent)
            print('\nАккаунт добавлен.')
        else:
            print('Введённые данные содержат ошибку, попробуйте ещё раз.')
    except:
        print('Что-то пошло не так.')

def report():
    try:
        db.report()
    except:
        print('Что-то пошло не так.')

def update():
    id = input('\nВведите id аккаунта, данные которого хотите обновить: ')
    old_mail = db.check_abuse_db(id=id).fetchone()[1]
    old_pass = db.check_abuse_db(id=id).fetchone()[2]
    amount = db.check_abuse_db(id=id).fetchone()[3]
    old_host = db.check_abuse_db(id=id).fetchone()[4]
    old_port = db.check_abuse_db(id=id).fetchone()[5]
    old_proxy_username = db.check_abuse_db(id=id).fetchone()[6]
    old_proxy_password = db.check_abuse_db(id=id).fetchone()[7]
    print('\n1) Почта: ' + old_mail)
    print('2) Пароль: ' + old_pass)
    print('3) Баланс: ' + str(amount))
    print('4) IP прокси: ' + old_host)
    print('5) Порт прокси: ' + old_port)
    print('6) Логин прокси: ' + old_proxy_username)
    print('7) Пароль прокси: ' + old_proxy_password)
    print('')
    edit = input('Введите номер данных для редактирования: ')
    if edit == '1':
        try:
            Email = input('Введите новую почту: ')
            db.update_email(data=Email, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '2':
        try:
            Password = input('Введите новый пароль: ')
            db.update_password(data=Password, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '3':
        try:
            Amount = input('Введите количество конфет: ')
            db.update_amount(data=Amount, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '4':
        try:
            Ip = input('Введите новый IP: ')
            db.update_host(data=Ip, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '5':
        try:
            Port = input('Введите новый порт: ')
            db.update_port(data=Port, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '6':
        try:
            Proxy_username = input('Введите новый логин прокси: ')
            db.update_proxy_login(data=Proxy_username, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    elif edit == '7':
        try:
            Proxy_password = input('Введите новый пароль прокси: ')
            db.update_proxy_password(data=Proxy_password, id=id)
            db.commit()
        except:
            print('Что-то пошло не так.')
    else:
        print("Вы ввели неверное значение.")

def unlimited_collect():
    """Функция неограниченного сбора конфет (для серверов)"""
    loop = 1
    while True:
        id = 1
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
                print(f'\n[{get_time()}] >> Сбор конфет - круг #{loop} пройден.\n')
                sleep_between_loop(id=id)
                break

            id += 1
        loop += 1

def collect():
    """Функция сбора конфет один раз"""
    id = 1
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
            print(f'\n[{get_time()}] >> Сбор конфет - круг пройден.')
            break

        id += 1

def get_cost(link):
    """Функция получения цены предмета по ссылке"""
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        cost = soup.find('span', {'class': 'font-weight-bold text-xl'})
        return cost.text
    except:
        print('Ошибка при получении стоимости товара. Возможно, ссылка некорректна.')

def buy():
    """Функция покупки предметов"""
    close = False
    while close == False:
        try:
            # Получаем цену товара
            link = input('\nВведите ссылку на желанный товар: ')
            price = int(re.search(r'\d+', get_cost(link=link)).group(0))
            if db.get_enough_balance(price) > 0:
                while True:

                    # Запрашиваем количество предметов для покупки
                    print(f'Можно купить {db.get_enough_balance(price)} шт.')
                    count = input('Сколько покупать? ')
                    print()
                    # Если запрос валидный, запускаем покупку
                    if int(count) > 0 and int(count) <= db.get_enough_balance(price):
                        bought = 0
                        id = 1
                        while bought < int(count):

                            try:
                                balance = int(db.check_abuse_db(id=id).fetchone()[3])
                            except:
                                close = True
                                break

                            # Если баланс больше цены, то покупаем
                            if balance >= int(price):

                                # Создаём экземпляр сессии, передавая порядковый номер аккаунта
                                coingecko_session = Coingecko(id=id)

                                # Получаем результат попытки логина
                                log_in_result = coingecko_session.log_in()

                                # Если успех, то собираем монеты
                                if log_in_result:

                                    # Покупаем предмет и получаем его название
                                    title = coingecko_session.buy(link=link)

                                    # Если название получили, то покупка успешна
                                    if title != False:

                                        # получаем купленный предмет: ссылка или код
                                        coingecko_session.get_promo(title=title)
                                        bought += 1

                            id += 1
                        print(f'[{get_time()}] >> Трата конфет завершена.')
                        close = True
                        break
                    else:
                        print("Попробуйте заново.\n")
            else:
                print(f'[{get_time()}] >> Слишком мало конфет, не могу купить ни одного предмета.')
                close = True
                break
        except:
            pass

class Coingecko:
    '''Класс Coingecko'''

    def __init__(self, id=None, login=None, password=None, hostname=None, port=None,
                 proxy_username=None, proxy_password=None):

        """Инициализация сессии"""
        try:
            # Вытаскиваем данные из БД
            self.id = id
            self.login = db.check_abuse_db(id=id).fetchone()[1]
            self.password = db.check_abuse_db(id=id).fetchone()[2]
            self.hostname = db.check_abuse_db(id=id).fetchone()[4]
            self.port = db.check_abuse_db(id=id).fetchone()[5]
            self.proxy_username = db.check_abuse_db(id=id).fetchone()[6]
            self.proxy_password = db.check_abuse_db(id=id).fetchone()[7]
            self.headers = db.check_abuse_db(id=id).fetchone()[8]
        except:
            # Получаем данные из параметров 
            self.login = login
            self.password=password
            self.hostname=hostname
            self.port=port
            self.proxy_username=proxy_username
            self.proxy_password=proxy_password
            while True:
                try:
                    self.headers = fake_useragent.UserAgent().random
                    break
                except:
                    pass

        # Генерируем сессию
        self.session = requests.Session()
        self.headers = {
            'user-agent': self.headers
        }

        # Настраиваем прокси
        if not (self.hostname == '' or self.port == '' or self.proxy_username == '' or self.proxy_password == ''):
            self.proxy = {
                'http': f'http://{self.proxy_username}:{self.proxy_password}@{self.hostname}:{self.port}',
                'https': f'http://{self.proxy_username}:{self.proxy_password}@{self.hostname}:{self.port}'
            }
            self.session.proxies = self.proxy

    def log_in(self):
        """Функция авторизации на сайте"""

        try:
            # отправляем запрос, чтобы получить токен
            login_link = 'https://www.coingecko.com/account/sign_in?locale=en'
            token = self.__get_token(login_link)

            login_data = {
                'utf8': "✓",
                'authenticity_token': token,
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

    def __parse_token(self, response):
        """Функция парсинга токена"""
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            token = soup.find('input', {'name': 'authenticity_token'})['value']
            sleep()
            return token
        except:
            return False

    def __get_token(self, url):
        """Функция получения токена"""
        self.response = self.session.get(url=url, headers=self.headers)
        return self.__parse_token(self.response)

    def get_balance(self):
        """Функция проверки баланса"""
        url = 'https://www.coingecko.com/account/candy?locale=en'

        # Получаем баланс и обновляем значение в БД
        balance_request = self.session.get(url=url, headers=self.headers)

        # Проверяем ответ
        if balance_request.ok:
            soup = BeautifulSoup(balance_request.text, 'lxml')
            balance = soup.find('div', {'data-target': 'points.balance'}).text
            print(f'Баланс: {balance} конфет.')
            return balance, self.headers
        else:
            print(f'При получении баланса произошла неизвестная ошибка.')



    def collect_candies(self):
        """Функция сбора монет"""

        try:
            # Получаем токен для авторизации запроса

            url = 'https://www.coingecko.com/account/candy?locale=en'
            auth_token = self.__get_token(url)

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
                    balance_request = self.session.get(url=url, headers=self.headers)
                    soup = BeautifulSoup(balance_request.text, 'lxml')
                    balance = soup.find('div', {'data-target': 'points.balance'}).text
                    db.update_amount(data=str(balance), id=self.id)
                    db.commit()
                    print(f'Баланс: {balance} конфет.')
                    sleep()
                else:
                    print(f'При сборе конфет произошла неизвестная ошибка.')

            # Если токен ложный, конфеты нельзя собрать
            else:
                # Получаем баланс и обновляем значение в БД
                balance_request = self.session.get(url=url, headers=self.headers)

                # Проверяем ответ
                if balance_request.ok:
                    soup = BeautifulSoup(balance_request.text, 'lxml')
                    balance = soup.find('div', {'data-target': 'points.balance'}).text
                    db.update_amount(data=str(balance), id=self.id)
                    db.commit()
                    print(f'Сегодня монеты уже собирались, баланс остался прежним: {balance} конфет.')
                    sleep()
                else:
                    print(f'При сборе конфет произошла неизвестная ошибка.')
        except:
            if not self.over:
                print(f'При сборе конфет произошла неизвестная ошибка.')

    def buy(self, link):
        try:
            # Получаем токен
            token = self.__get_token(link)

            # Если токен получен
            if token != False:

                # Получем действие
                soup = BeautifulSoup(self.response.text, 'lxml')
                action = soup.findAll('form', {'class': 'button_to'})[1]['action']

                # получаем название предмета
                title = soup.find('div', {'class': 'text-lg-2xl text-xl pl-1 font-weight-bold'})
                data = {
                    'authenticity_token': token,
                }

                # отправляем запрос покупки реварда
                buy_response = self.session.post(url="https://www.coingecko.com/" + action, data=data,
                                            headers=self.headers)
                if buy_response.ok:
                    print(f'Купил "{title.text}".', end=' ')
                    return title.text
                else:
                    print(f'Предмет уже куплен, невозможно приобрести ещё.')
                    return False
            else:
                print(f'Предмет уже куплен, невозможно приобрести ещё.')
            return False
        except:
            print('При покупке произошла ошибка.')

    def get_promo(self, title):
        try:
            url = "https://www.coingecko.com/account/my-rewards?locale=en"
            response = self.session.get(url=url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')

            # Получаем список полученных наград
            rewards = soup.findAll('div', {'class': 'ml-3 mr-md-3 ml-lg-4 mb-3 mr-lg-1 voucher-card-section'})

            # ищем ссылку на награду по названию покупки
            for reward in rewards:
                if title in reward.contents[3].text:
                    # достаём промо
                    href = reward.contents[1].contents[1]['href']
                    response = self.session.get("https://www.coingecko.com/" + href, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'lxml')
                    promo = soup.find('input', {'class': 'form-control font-semibold'})['value']
                    print(f'Код: {promo}.', end=' ')
                    break
            try:
                # обновляем количество конфет
                url = 'https://www.coingecko.com/account/candy?locale=en'
                balance_request = self.session.get(url=url, headers=self.headers)
                soup = BeautifulSoup(balance_request.text, 'lxml')
                balance = soup.find('div', {'data-target': 'points.balance'}).text
                db.update_amount(data=str(balance), id=id)
                db.commit()
                print(f'Оставшиеся конфеты: {str(balance)}.')
            except:
                pass
        except:
            print('При получении промокода на товар произошла ошибка.')



