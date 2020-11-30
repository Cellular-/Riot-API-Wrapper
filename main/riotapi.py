import requests as r, json, sqlite3, os, atexit, sys, inspect
import apiresources, customexceptions
from configparser import ConfigParser
from datetime import datetime
from apiresources import Account, Matchlist, Endpoint, Header
from customexceptions import ApiError

parser = ConfigParser()
parser.read('env')

class RiotApi():
    def __init__(self):
        self.header = Header.base_request
        self.header['X-Riot-Token'] = parser.get('api_resources', 'key')

    def dict_factory(self, cursor, row):
        """Converts database results into a dictionary where the 
        key is the column name and the value is the column value.
        """
        results = {}
        for index, col_name in enumerate(cursor.description):
            results[col_name[0]] = row[index]

        return results

    def summoner_store(self, summoner_account):
        id = None

        if not isinstance(summoner_account, Account):
            raise TypeError('An instance of the Account class must be passed in.')

        try:
            db_path = parser.get('database', 'full_path')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = f'''insert into account
                        values (NULL,
                                '%(id)s',
                                '%(accountId)s',
                                '%(puuid)s',
                                '%(name)s',
                                '%(profileIconId)s',
                                '%(revisionDate)s',
                                '%(summonerLevel)d',
                                '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')''' % vars(summoner_account)

            cursor.execute(query)
            conn.commit()
            id = cursor.lastrowid
            cursor.close()
        except sqlite3.IntegrityError as error:
            if 'UNIQUE constraint' in str(error):
                print('The name or account id is not unique for\n %s' % summoner_account)
        except sqlite3.OperationalError as error:
            print(error)
        except Exception as error:
            print(error)
        finally:
            return id

    def summoner_query(self, name=None):
        """
        name - summoner's name of interest

        return - response

        raises - ApiError if summoner does not exist
        """
        if not isinstance(name, str):
            raise TypeError("Summoner name must be a string")

        endpoint = Endpoint.account.format(summoner_name=name)

        response = r.get(endpoint, headers=self.header)
    
        if response.status_code != 200:
            raise ApiError(endpoint, response.status_code, response.reason)

        return Account(**response.json())

    def summoner_get_account_info(self, name=None):
        if not isinstance(name, str):
            raise TypeError("Summoner name must be a string")

    def summoner_matchlist(self, account_id):
        response = r.get(Endpoint.matchlist.format(account_id=account_id), headers=self.header)

        return response

    def summoner_store_matchlist(self, matchlist):
        try:
            db_path = parser.get('database', 'full_path')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = f'''insert into matchlist
                        values (NULL,
                                '%(platformId)s',
                                '%(gameId)s',
                                '%(champion)d',
                                '%(queue)s',
                                '%(season)d',
                                '%(timestamp)d',
                                '%(role)s',
                                '%(lane)s')'''

            for match in matchlist['matches']:
                cursor.execute(query % match)
                conn.commit()
        except sqlite3.IntegrityError as error:
            print(error)
        except sqlite3.OperationalError as error:
            print(error)
        finally:
            cursor.close()

if __name__ == '__main__':
    from atexit_functions import funcs
    for func in funcs:
        atexit.register(func)