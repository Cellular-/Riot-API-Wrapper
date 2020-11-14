import requests as r, json, sqlite3, os, atexit, sys
from enum import Enum

header = { "request_header": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": os.environ["RIOT_API_KEY"]
            }
        }

endpoints = {'summoner': {
                    'account': {'info': 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'},
                    'stats': {'match_list': 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}'}
                }
            }

class Summoner():
    def _init__(self):
        self.summoner_name
        self.matchlist
    
    def ini(self):
        pass

    


class RiotApi():
    def __init__(self):
        pass

    def summoner_store(self, summoner_account):
        id = None
        if len(summoner_account) > 7:
            raise Exception('Summoner account record should only have 7 values.')

        try:
            conn = sqlite3.connect('loldata.db')
            cursor = conn.cursor()

            query = f'''insert into account
                        values (NULL,
                                '%(id)s',
                                '%(accountId)s',
                                '%(puuid)s',
                                '%(name)s',
                                '%(profileIconId)s',
                                '%(revisionDate)s',
                                '%(summonerLevel)d')''' % summoner_account

            cursor.execute(query)
            conn.commit()
            id = cursor.lastrowid
            cursor.close()
        except sqlite3.IntegrityError as error:
            if 'UNIQUE constraint' in str(error):
                print('The name or account id is not unique for\n %s' % summoner_account)
        except sqlite3.OperationalError as error:
            print(error)
        finally:
            return id

    def summoner_query(self, name=None):
        """
        name - summoner's name of interest

        return - response
        """
        response = r.get(endpoints['summoner']['account']['info']\
                        .format(summoner_name=name), headers=header["request_header"])

        return response

    def summoner_matchlist(self, account_id):
        response = response = r.get(endpoints['summoner']['stats']['match_list']\
                            .format(account_id=account_id), 
                            headers=header["request_header"])

        return response

    def run_cli_tool(self):
        def print_menu():
            menu = 'League of Legends Tool\n' \
                's - Get summoner account info\n' \
                'Select an option: '

            print(menu)

        data = None
        while True:
            menuOption = 'z'
            if not menuOption.lower() in ('s', 'q'):
                print_menu()
                menuOption = str(input())

            if menuOption == 's':
                summoner_name = None
                while not summoner_name:
                    summoner_name = str(input('Enter a summoner name: '))
                
                data = self.summoner_query(name=summoner_name)
                record_id = None

                if data:
                    record_id = self.summoner_store(data.json())
                    if record_id:
                        print("Added %s to database with row id %d" % (summoner_name, record_id))
                else:
                    print('Summoner `%s` does not exist' % (summoner_name,))

            if menuOption == 'm':
                summoner_name = None
                while not summoner_name:
                    summoner_name = str(input('Enter a summoner name: '))
                
                data = self.summoner_matchlist(name=summoner_name)
                # record_id = None

                # if data:
                #     record_id = self.summoner_store(data.json())
                #     if record_id:
                #         print("Added %s to database with row id %d" % (summoner_name, record_id))
                # else:
                #     print('Summoner `%s` does not exist' % (summoner_name,))

            elif menuOption == 'q':
                break

            print("\n")

if __name__ == '__main__':
    from atexit_functions import funcs
    for func in funcs:
        atexit.register(func)

    RiotApi().run_cli_tool()