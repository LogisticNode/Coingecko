from Config import *

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

#Requests Functions
def coingecko_login(request_session, login, password, headers):
    # отправляем запрос, чтобы получить Auth_token
    response = request_session.get('https://www.coingecko.com/account/sign_in?locale=en', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
    login_data = {
        'utf8': "✓",
        'authenticity_token': csrf_token,
        'user[redirect_to]': "",
        'user[email]': login,
        'user[password]': password,
        'user[remember_me]': {
            0: '0',
            1: '1'
        },
        'commit': "Log+in"
    }
    # отправляем запрос логина
    login_request = request_session.post(url="https://www.coingecko.com/account/sign_in?locale=en", data=login_data, headers=headers)
    if login_request.ok:
        print(f'[{get_time()}] >> [{login}] >> successfully logged.', end=' ')
        return True
    else:
        print(f'[{get_time()}] >> GG.')
        return False

def get_token(request_session, headers):
    balance_request = request_session.get('https://www.coingecko.com/account/candy?locale=en', headers=headers)
    soup = BeautifulSoup(balance_request.text, 'lxml')
    try:
        csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
        return csrf_token
    except:
        return False

def parse_token(response):
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        token = soup.find('input', {'name': 'authenticity_token'})['value']
        return token
    except:
        return False

def collect_candies(id, csrf_token, request_session, headers):
    # отправляю запрос на сбор конфет
    data = {
        'authenticity_token' : csrf_token
    }
    collect_request = request_session.post('https://www.coingecko.com/account/candy/daily_check_in?locale=en', headers=headers,data=data)
    if collect_request.ok:
        print(f'successfully redeemed.', end=' ')
        # получаю новый баланс
        balance_request = request_session.get('https://www.coingecko.com/account/candy?locale=en', headers=headers)
        soup = BeautifulSoup(balance_request.text, 'lxml')
        balance1 = soup.find('div', {'data-target': 'points.balance'}).text
        Total1 = str(balance1)
        db.update_amount(data=Total1, id=id)
        db.commit()
        print(f'new balance: {balance1} candies.')
    else:
        balance_request = request_session.get('https://www.coingecko.com/account/candy?locale=en', headers=headers)
        soup = BeautifulSoup(balance_request.text, 'lxml')
        balance2 = soup.find('div', {'data-target': 'points.balance'}).text
        Total2 = str(balance2)
        db.update_amount(data=Total2, id=id)
        db.commit()
        print(f'GG.')
def get_reward(link, session, headers):

    # получаем токен
    response = session.get(link, headers=headers)
    token = parse_token(response)
    # если токен получен
    if token != False:

        # получем действие
        soup = BeautifulSoup(response.text, 'lxml')
        action = soup.findAll('form', {'class': 'button_to'})[1]['action']

        # получаем название предмета
        title = soup.find('div', {'class': 'text-lg-2xl text-xl pl-1 font-weight-bold'})
        data = {
            'authenticity_token': token,
        }

        # отправляем запрос покупки реварда
        buy_response = session.post(url="https://www.coingecko.com/"+action, data=data,
                                     headers=headers)
        if buy_response.ok:
            print(f'successfully bought.', end=' ')
            return title.text
        else:
            print(f'GG.')
            return False
    else:
        print(f'GG.')
        return False

def get_promo(title, session, headers):
    response = session.get("https://www.coingecko.com/account/my-rewards?locale=en", headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # получаем список полученных наград
    rewards = soup.findAll('div', {'class': 'ml-3 mr-md-3 ml-lg-4 mb-3 mr-lg-1 voucher-card-section'})
    for reward in rewards:

        # ищем ссылку на награду по названию покупки
        if title in reward.contents[3].text:

            # достаём промо
            href = reward.contents[1].contents[1]['href']
            response = session.get("https://www.coingecko.com/" + href, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            promo = soup.find('input', {'class': 'form-control font-semibold'})['value']
            print(f'promo: {promo}.')
            break

#Action 1
def start_bot(id):
    while True:
        # Получаем данные прокси
        try:
            hostname = db.check_abuse_db(id=id).fetchone()[4]
            port = db.check_abuse_db(id=id).fetchone()[5]
            proxy_username = db.check_abuse_db(id=id).fetchone()[6]
            proxy_password = db.check_abuse_db(id=id).fetchone()[7]
        except:
            print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Сбор конфет - круг пройден.')
            print('================================================================================')
            break
        proxy = {
            'http': f'http://{proxy_username}:{proxy_password}@{hostname}:{port}',
            'https': f'http://{proxy_username}:{proxy_password}@{hostname}:{port}'
        }

        # Генерируем user-agent
        user = fake_useragent.UserAgent().random
        headers = {
            'user-agent': user
        }

        # Cоздаём сессию
        request_session = requests.Session()
        request_session.proxies = proxy

        # Получаем данные от аккаунт
        login = db.check_abuse_db(id=id).fetchone()[1]
        password = db.check_abuse_db(id=id).fetchone()[2]

        # Входим в аккаунт
        coingecko_login(request_session=request_session, login=login, password=password, headers=headers)
        time.sleep(random.randint(5, 15))

        # Получаем токен
        token = get_token(request_session=request_session, headers=headers)
        time.sleep(random.randint(5, 15))

        # Собираем конфеты
        collect_candies(id=id, csrf_token=token, request_session=request_session, headers=headers)
        time.sleep(random.randint(5, 15))

        id += 1

#Action 2
def add_user():
    db.create_table_abuse()
    Email = str(input('Введите почту: '))
    Password = str(input('Введите пароль: '))
    Host = str(input('Введите ip прокси: '))
    Port = str(input('Введите порт прокси: '))
    Proxy_username = str(input('Введите логин прокси: '))
    Proxy_password = str(input('Введите пароль для прокси: '))
    db.add_user_coingecko(Email=Email, Password=Password, Host=Host, Port=Port, Proxy_username=Proxy_username, Proxy_password=Proxy_password)

#Action 3
def report():
    db.report()

#Action 4
def update():
    id = input('Введите id аккаунта, данные котороо хотите обновить: ')
    Old_mail = db.check_abuse_db(id=id).fetchone()[1]
    Old_pass = db.check_abuse_db(id=id).fetchone()[2]
    Amount = db.check_abuse_db(id=id).fetchone()[3]
    Old_host = db.check_abuse_db(id=id).fetchone()[4]
    Old_port = db.check_abuse_db(id=id).fetchone()[5]
    Old_proxy_username = db.check_abuse_db(id=id).fetchone()[6]
    Old_proxy_password = db.check_abuse_db(id=id).fetchone()[7]
    print('1) Email: ' + Old_mail)
    print('2) Password: ' + Old_pass)
    print('3) Amount: ' + str(Amount))
    print('4) Ip: ' + Old_host)
    print('5) Port: ' + Old_port)
    print('6) Proxy login: ' + Old_proxy_username)
    print('7) Proxy password: ' + Old_proxy_password)
    print('')
    edit = input('Введите цифру данных для редактирования: ')
    if edit == '1':
        Email = input('Введите новую почту: : ')
        db.update_email(data=Email, id=id)
        db.commit()
    elif edit == '2':
        Password = input('Введите новый пароль: ')
        db.update_password(data=Password, id=id)
        db.commit()
    elif edit == '3':
        Amount = input('Введите количество конфет: ')
        db.update_amount(data=Amount, id=id)
        db.commit()
    elif edit == '4':
        Ip = input('Введите новый ip: ')
        db.update_host(data=Ip, id=id)
        db.commit()
    elif edit == '5':
        Port = input('Введите новый порт: ')
        db.update_port(data=Port, id=id)
        db.commit()
    elif edit == '6':
        Proxy_username = input('Введите новый логин прокси: ')
        db.update_proxy_login(data=Proxy_username, id=id)
        db.commit()
    elif edit == '7':
        Proxy_password = input('Введите новый пароль прокси: ')
        db.update_proxy_password(data=Proxy_password, id=id)
        db.commit()
    else:
        print("Вы ввели неверное значение")

#Action 5
def buy(id):
    link = input('Введите ссылку на желанный товар: ')
    while True:
        # Получаем данные прокси
        try:
            hostname = db.check_abuse_db(id=id).fetchone()[4]
            port = db.check_abuse_db(id=id).fetchone()[5]
            proxy_username = db.check_abuse_db(id=id).fetchone()[6]
            proxy_password = db.check_abuse_db(id=id).fetchone()[7]
        except:
            print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Трата конфет завершена.')
            print('================================================================================')
            break
        proxy = {
            'http': f'http://{proxy_username}:{proxy_password}@{hostname}:{port}',
            'https': f'http://{proxy_username}:{proxy_password}@{hostname}:{port}'
        }

        # генерируем фейковый юзер-агент
        user = fake_useragent.UserAgent().random
        headers = {
            'user-agent': user
        }

        # создаём сессию и подключаем прокси
        request_session = requests.Session()
        request_session.proxies = proxy
        try:
            # получаем данные
            login = db.check_abuse_db(id=id).fetchone()[1]
            password = db.check_abuse_db(id=id).fetchone()[2]
            # выполняем логин
            if coingecko_login(request_session=request_session, login=login, password=password, headers=headers):
                time.sleep(seconds_to_sleep)

                # получаем баланс
                balance = db.check_abuse_db(id=id).fetchone()[3]
                print('Баланс на аккаунте №' + str(id) + ' = ' + str(balance))
                time.sleep(seconds_to_sleep)

                # покупаем предмет
                title_result = get_reward(link=link, session=request_session, headers=headers)
                if title_result != False:
                    # получаем купленный предмет: ссылка или код
                    get_promo(title=title_result, session=request_session, headers=headers)

                    # обновляем количество конфет
                    balance_request = request_session.get('https://www.coingecko.com/account/candy?locale=en',
                                                          headers=headers)
                    soup = BeautifulSoup(balance_request.text, 'lxml')
                    balance = soup.find('div', {'data-target': 'points.balance'}).text
                    Total = str(balance)
                    db.update_amount(data=Total, id=id)
                    db.commit()
                    print('Оставшиеся конфеты на аккаунте №' + str(id) + ' = ' + str(Total))
            else:
                print(f'something went wrong with [{login}].')

            # пауза между аккаунтами от 3 до 10 минут
        except:
            print(f'something went wrong with [{login}].')

        id += 1

    print(f'we got all of rewards.')

#Main
def main():

    while True:
        print('')
        print("1) Запустить бота")
        print("2) Добавить аккаунт")
        print("3) Посмотреть балансы на аккаунтах")
        print("4) Изменить данные аккаунта")
        print('5) Потратить конфетки')
        print("6) Завершить работу")
        print("Для выбора функции требуется ввести её номер")
        print('')
        cmd = input("Выберите функцию: ")

        if cmd == "1":
            start_bot(id=id)
        elif cmd == "2":
            add_user()
        elif cmd == "3":
            report()
        elif cmd == "4":
            update()
        elif cmd == "5":
            buy(id=id)
        elif cmd == "6":
            break
        else:
            print("Вы ввели не правильное значение")
