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

    while 1:
        menu()
        try:
            option = int(input())
            if option not in range(0, 11):
                raise ValueError
            if option == 1:
                tables.get_table_names(cookie)
            if option == 2:
                print(f'Version: {version.get_version(cookie)}')
            if option == 3:
                columns.get_column_names(cookie)
            if option == 4:
                usernames.get_usernames(cookie)
            if option == 5:
                print(f'Password: {password.get_password(cookie)}')
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
