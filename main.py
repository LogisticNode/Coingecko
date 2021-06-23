from config import *
from functions import *

def main():
    while True:
        if os.path.getsize('DataBase.db') > 0:
            while True:
                print("\n┌────────────────────────────────────────────────────┐ ")
                print("  ///    <<      Coingecko Collect Bot      >>   ///  ")
                print("  ///    <<    by Logistic & cyberomanov    >>   ///  ")
                print("  ///    <<             v1.0.0              >>   ///  ")
                print("└────────────────────────────────────────────────────┘\n")
                print("1) Запустить бота;")
                print("2) Запустить бесконечный сбор конфет (для  серверов);")
                print("3) Добавить аккаунт;")
                print("4) Посмотреть информацию об аккаунтах;")
                print("5) Изменить данные аккаунта;")
                print("6) Потратить конфетки;")
                print("7) Завершить работу.\n")
                print("Для выбора функции требуется ввести её номер.", end=' ')
                cmd = input("Введите номер функции: ")

                if cmd == "1":
                    print()
                    collect()
                elif cmd == "2":
                    print("\nЗапущен бесконечный сбор конфет:\n")
                    unlimited_collect()
                elif cmd == "3":
                    print()
                    add_user()
                elif cmd == "4":
                    print()
                    report()
                elif cmd == "5":
                    print()
                    update()
                elif cmd == "6":
                    buy()
                elif cmd == "7":
                    break
                else:
                    print("\nВы ввели не правильное значение.\n")
        else:
            print("\n┌────────────────────────────────────────────────────┐ ")
            print("  ///    <<      Coingecko Collect Bot      >>   ///  ")
            print("  ///    <<    by Logistic & cyberomanov    >>   ///  ")
            print("  ///    <<             v1.0.0              >>   ///  ")
            print("└────────────────────────────────────────────────────┘\n")
            print("1) Добавить аккаунт;")
            print("2) Завершить работу.\n")
            print("Для выбора функции требуется ввести её номер.", end=' ')
            cmd = input("Введите номер функции: ")

            if cmd == "1":
                print()
                add_user()
            elif cmd == "2":
                break
            else:
                print("\nВы ввели не правильное значение.\n")


main()
