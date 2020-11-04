import requests as r, json, sqlite3, os

os.environ["RIOT_API_KEY"] = 'RGAPI-c0c7b4d8-e52d-46cd-b3d8-2f085e6636ca'

header = { "request_header": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": os.environ["RIOT_API_KEY"]
            }
        }

endpoints = {
    "summoner": {"url": "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"}
}

def summoner_store(summoner_account):
    if len(summoner_account) > 7:
        raise Exception("Summoner account record should only have 7 values.")

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
        cursor.close()
    except Exception as error:
        print(error)

def summoner_query():
    menuOption = None
    while menuOption != 'q':
        print_menu()
        menuOption = str(input())

        if not menuOption in ('s'):
            print_menu()
            menuOption = str(input())

        if menuOption == 's':
            summoner_name = None
            while not summoner_name:
                summoner_name = str(input("Enter a summoner name: "))

            response = None
            try:
                response = r.get(endpoints["summoner"]["url"].format(summoner_name=summoner_name), headers=header["request_header"])
            except r.HTTPError as error:
                print(error)

            if response.status_code == '404':
                print(f"Summoner {summoner_name} not exist.")
                continue

            summoner_store(response.json())

def print_menu():
    menu = f'''
    League of Legends Tool
    s - Get summoner account info
    Select an option: 
    '''
    print(menu)
                

if __name__ == '__main__':
    summoner_query()