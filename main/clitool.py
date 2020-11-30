import riotapi
import sqlite3, sys
from configparser import ConfigParser
from apiresources import Account, Matchlist, Endpoint
from customexceptions import ApiError

rapi = riotapi.RiotApi()
parser = ConfigParser()
parser.read('env')

def run_cli_tool():
    def add_summoner():
        summoner_name = None
        while not summoner_name:
            summoner_name = str(input('Enter a summoner name: '))

        try:
            account = rapi.summoner_query(name=summoner_name)

            record_id = rapi.summoner_store(account)
            if record_id:
                print("Added %s to database with row id %d" % (account.name, record_id))
        except ApiError as error:
            print(error)
        finally:
            record_id = None

    def get_matchlist():
        summoner_name = None
        while not summoner_name:
            summoner_name = str(input('Enter a summoner account ID: '))
        
        try:
            matchlist_data = rapi.summoner_matchlist(account_id=summoner_name)
            matchlist = Matchlist(**matchlist_data)

            rapi.summoner_store_matchlist(matchlist.json())
        except Exception as error:
            print(error)

    def get_account_info():
        summoner_name = None
        results = None
        while not summoner_name:
            summoner_name = str(input('Enter a summoner name: '))

        conn = sqlite3.connect(parser.get('database', 'full_path'))
        conn.row_factory = rapi.dict_factory
        cursor = conn.cursor()

        query = f'''select id, accountId, name, summonerLevel
                    from account 
                    where lower(name) = \'{summoner_name.lower()}\''''

        cursor.execute(query)
        conn.commit()
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            print(f'{summoner_name} does not exist in the Account table yet.')
        else:
            account_info = Account(**result)
            print('\n')
            print('*' * len(account_info.accountId))
            print("Account information for {}".format(account_info.name))
            print(account_info)
            print('*' * 50)
            print('\n')

    def print_menu():
        menu = 'League of Legends Tool\n' \
            's - Create account record for given summoner name\n' \
            'r - Get summoner account info from database\n' \
            'm - Get summoner matchlist\n' \
            'p - Print menu\n' \
            'q - quit\n' \
            'Select an option: '

        print(menu)

    menu_commands = {'s': add_summoner,
                        'm': get_matchlist,
                        'r': get_account_info,
                        'q': lambda: sys.exit(0),
                        'p': print_menu}

    def is_valid_menu_option(menu_option):
        return menu_option in [command for command in menu_commands.keys()]

    while(True):
        print_menu()
        menu_option = str(input())
        
        while(not is_valid_menu_option(menu_option)):
            menu_option = str(input())
        
        menu_commands[menu_option]()

if __name__ == '__main__':
    run_cli_tool()
