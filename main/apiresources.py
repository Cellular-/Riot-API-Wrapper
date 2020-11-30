class Account():
    def __init__(self, id='', accountId='', puuid='', name='', profileIconId='', revisionDate='', summonerLevel=''):
        self.id = id
        self.accountId = accountId
        self.puuid = puuid
        self.name = name
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel

    def __str__(self):
        return "\n".join([f'{attribute} : {value}' for attribute, value in self.__dict__.items()])

class Matchlist():
    def __init__(self, platformId, gameId, champion, queue, season, timestamp, role, lane):
        self.platformId = platformId
        self.gameId = gameId
        self.champion = champion
        self.queue = queue
        self.season = season
        self.timestamp = timestamp
        self.role = role
        self.lane = lane

    def __str__(self):
        return "\n".join([f'{attribute} : {value}' for attribute, value in self.__dict__.items()])

class Endpoint(object):
    endpoints = {'summoner': {
                    'account': {'info': 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'},
                    'stats': {'matchlist': 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}'}
                }
            }

    account = endpoints['summoner']['account']['info']
    matchlist = endpoints['summoner']['stats']['matchlist']