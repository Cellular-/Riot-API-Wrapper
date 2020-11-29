def create_table_from_json(table_name ,json_data):
    create_table_sql = \
    '''CREATE TABLE IF NOT EXISTS {table_name}'''  \
    '''(''' \
    '''record_id INTEGER PRIMARY KEY'''\
    '''{column_definitions}''' \
    ''');'''

    columns = ''.join([f',\n{key} TEXT NOT NULL' for key in json_data])

    return create_table_sql.format(table_name=table_name, column_definitions=columns)

create_table_from_json('account', dict(id='XjHK2w6s7L1RjWJmx5sBCBKyn53W9GkA0sJrfs2yVu6Njq4',
                accountId='zdcbjH8l_JrFOZQUnBhQ1qpfmbatCMRM9cZKUzMXvi9KYg',
                puuid='l31wR_PbYXwS7ieuhjJ1rAEdvlbd_NaQTGKi0Ureh5aQbQ5WjEJQFXEGlsXbgdRdow6J_bFEOZSi8Q',
                name="Cellular",
                profileIconId=1149,
                revisionDate=1604290860000,
                summonerLevel=113))