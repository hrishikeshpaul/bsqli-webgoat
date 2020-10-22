import datetime
import sys

from helpers import version, usernames, tables, columns, password


def menu():
    print()
    print(f'ASSIGNMENT 1')
    print(f'hrpaul@iu.edu')
    print()
    print(f'Enter option number,')
    print(f'1. Retrieve Table Names')
    print(f'2. Retrieve Database Version')
    print(f'3. Retrieve names of all columns contained in the table whose name starts with ‘CHALLENGE’')
    print(f'4. Retrieve all original usernames stored in the table whose name starts with ‘CHALLENGE’')
    print(f'5. Retrieve the password of user ‘tom’ stored in the table whose name starts with ‘CHALLENGE’.')
    print(f'6. Print all tables')
    print(f'7. Print database version')
    print(f'8. Print all columns of the table CHALLENGE')
    print(f'9. Print all usernames in the table CHALLENGE')
    print(f'10. Print tom\'s password')
    print(f'0. Exit')
    print()


def exit():
    print(f'Thank you.')
    sys.exit(0)


if __name__ == '__main__':
    cookie = "JSESSIONID=_ZbQZICPMUeDulkvuTEokffIx-KsU91i0ZugU7DB"
    start = end = datetime.datetime.now()

    while 1:
        menu()
        try:
            option = int(input())
            if option not in range(0, 11):
                raise ValueError
            if option == 1:
                start = datetime.datetime.now()
                tables.get_table_names(cookie)
                end = datetime.datetime.now()
            if option == 2:
                start = datetime.datetime.now()
                print(f'Version: {version.get_version(cookie)}')
                end = datetime.datetime.now()
            if option == 3:
                start = datetime.datetime.now()
                columns.get_column_names(cookie)
                end = datetime.datetime.now()
            if option == 4:
                start = datetime.datetime.now()
                usernames.get_usernames(cookie)
                end = datetime.datetime.now()
            if option == 5:
                start = datetime.datetime.now()
                print(f'Password: {password.get_password(cookie)}')
                end = datetime.datetime.now()
            if option == 6:
                tables.print_table_names()
            if option == 7:
                version.print_version()
            if option == 8:
                columns.print_columns()
            if option == 9:
                usernames.print_usernames()
            if option == 10:
                password.print_password()
            if option == 0:
                exit()

        except ValueError:
            print("Please enter values from 1-9 only.")

        print(f'Total Time: {(end - start).total_seconds()}s')
