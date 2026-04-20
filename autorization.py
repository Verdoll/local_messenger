import json


def create_new_person(login, sex="не указан", age="не указан"):
    password = input("Введи пароль: ")
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        data.update({login : [password, sex, age]})
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
            print('вы успешно создали учетную запись. Теперь можете войти в нее')


def print_info(login, data):
    print(f'''данные о учетной записи: {login}!
    login: {login}
    пароль: {data[login][0]}
    пол: {data[login][1]}
    возраст: {data[login][2]}''')


def update_info(login):
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        sex = input("введите ваш пол: ")
        age = input("введите ваш возраст: ")
        print('данные успешно обновлены!')
        data[login][1] = sex
        data[login][2] = age
        json.dump(data, data_file, indent=4)


def check_login(login):
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        if login in data:
            return True
        else:
            return False


def profile(login):
    print(f'вы вошли в профиль {login}!')
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        text = ''
        while text != 'logout':
            text = input()
            if 'update' in text:
                update_info(login)
                print()
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
                print_info(login, data)
                print()
                print(f"вы в профиле {login}!")
            elif 'info' in text:
                print_info(login, data)
            elif 'send' in text:
                login2 = text.split()[1]
                send_message(login, login2)

            elif 'dialog' in text:
                login2 = text.split()[1]
                history(login, login2)
                mes(login)
            else:
                pass


def mes(login):
    print()
    print(f'вы в профиле {login}!')


def login_user(login):
    if check_login(login):
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        while True:
            pas = input('введите пароль: ')
            if pas!= '\logout':
                if data[login][0] == pas:
                    profile(login)
                    print("вы успешно вышли из профиля")
                    break
                else:
                    print('неверно, попробуйте снова')
            else:
                break
    else:
        create_new_person(login)


def check_command(string):
    if "login" in string:
        string = string.split("login ")[1]
        if string != "":
            return [string, "login"]

    elif "update" in string:
        string = string.split("update ")[1]
        return [string, "update"]

    elif "logout" in string:
        return [string, "logout"]
    elif 'clear_data' in string:
        return [string, "clear"]
    elif 'exit' in string:
        return [string, "exit"]
    elif 'send' in string:
        string = string.split("send")[1]
        return [string, "send"]
    else:
        return [string, "error"]

###
###
###
def name_dialog(login1, login2):
    return "".join(sorted([login1, login2]))


def is_dialog_exist(login1, login2):
    with open("mesagges.json", "r") as data_file:
        data = json.load(data_file)
    if name_dialog(login1, login2) in data:
        return True
    else:
        return False


def history(login1, login2):
    with open("mesagges.json", "r") as data_file:
        data = json.load(data_file)
    for _ in data[name_dialog(login1, login2)]:
        print(_)


def create_dialog(login1, login2):
    with open('mesagges.json', 'r') as data_file:
        data = json.load(data_file)
    with open('mesagges.json', 'w') as data_file:
        data_upload = {name_dialog(login1, login2) : []}
        data.update(data_upload)
        json.dump(data, data_file, indent=4)


def send_message(login1, login2):
    with open('mesagges.json', 'r') as data_file:
        data = json.load(data_file)
    if is_dialog_exist(login1, login2):
        print('история диалога:')
        history(login1, login2)
        text = input('введите свое сообщение: ')
        message = f'{login1}: {text}'
        data[name_dialog(login1, login2)].append(message)
        with open('mesagges.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
        print('сообщение успешно отправлено! ')

    elif not is_dialog_exist(login1, login2):
        create_dialog(login1, login2)
        data[name_dialog(login1, login2)] = []
        text = input('введите свое сообщение: ')
        message = f'{login1}: {text}'
        data[name_dialog(login1, login2)].append(message)
        with open('mesagges.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
        print('сообщение успешно отправлено! ')


while True:
    str = input()
    command = check_command(str)
    if command[1] != 'error':
        if command[1] == 'login':
            login_user(command[0])
        elif command[1] == 'update':
            print('вы не вошли в аккаунт')
        elif command[1] == 'logout':
            print("вы не вошли ни в один аккаунт")
        elif command[1] == 'clear':
            with open("data.json", "w") as data_file:
                data = {}
                json.dump(data, data_file, indent=4)
            with open("mesagges.json", "w") as data_file:
                data = {}
                json.dump(data, data_file, indent=4)
            print('все данные успешно удалены')
        elif command[1] == 'exit':
            break

