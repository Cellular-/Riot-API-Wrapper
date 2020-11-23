from pytest import fixture
from main.riotapi import RiotApi
import time, sqlite3

rapi = RiotApi()

@fixture
def account_keys():
    """Returns a tuple of complete set of keys that should exist in a valid
    account response from the Riot API.
    """
    return ('id', 'accountId', 'puuid', 'name', 'profileIconId', 'revisionDate', 'summonerLevel')

@fixture
def summoner_not_found_keys():
    """Returns a tuple of complete set of keys and their hierarchy that should
    exits when querying the Riot API for a non-existent summoner.
    """
    return (('status',), ('message', 'status_code'))

@fixture
def summoners_that_exist():
    """Returns a tuple of summoners that exist."""
    return ('Pianowoahman', 'Cellular', 'Uoex')

@fixture
def summoners_that_exist_in_account_table():
    """Returns a tuple of summoners that already exists in the account table."""
    return ('Cellular',)

@fixture
def summoners_that_dont_exist():
    """Returns a tuple of summoners that do not exist."""
    return ('Celullar', 'dsadasdwacasbp2ub3o12c89das')

@fixture
def summoner_that_exists_account_dict():
    """Returns a dict that represents a JSON response from the Riot API"""
    return dict(id='XjHK2w6s7L1RjWJmx5sBCBKyn53W9GkA0sJrfs2yVu6Njq4',
                accountId='zdcbjH8l_JrFOZQUnBhQ1qpfmbatCMRM9cZKUzMXvi9KYg',
                puuid='l31wR_PbYXwS7ieuhjJ1rAEdvlbd_NaQTGKi0Ureh5aQbQ5WjEJQFXEGlsXbgdRdow6J_bFEOZSi8Q',
                name="Cellular",
                profileIconId=1149,
                revisionDate=1604290860000,
                summonerLevel=113)

@fixture
def sqlite_database_name():
    return 'loldata.db'

@fixture
def riot_api_instance():
    """Returns an instance of the riot api client"""
    return RiotApi()

def test_pytest_true():
    assert True

def test_get_account_info(account_keys, summoners_that_exist):
    """Test API call to get an existing summoner's account information
    
    Parameters:
    account_keys - tuple of expected keys in account response
    summoners_that_exist - tuple of summoners that are guaranteed to exist
    """

    for summoner_name in summoners_that_exist:
        response = rapi.summoner_query(name=summoner_name)

        time.sleep(1)

        assert isinstance(response.json(), dict)
        assert response.json()["name"] == summoner_name
        assert set(account_keys).issubset(response.json().keys())

def test_get_account_info_404(summoner_not_found_keys, summoners_that_dont_exist):
    """Test Riot API to get non-existent summoners account.
    
    Parameters:
    summoner_not_found_keys - tuple of expected keys for summoner that cannot be found
    summoners_that_dont_exist - tuple of summoners that are guaranteed to not exist

    Expectations:
    The API should return a response indicating that the summoner could not be found.
    """

    for summoner_name in summoners_that_dont_exist:
        try:
            response = rapi.summoner_query(name=summoner_name)
        except Exception as error:
            pass

        time.sleep(1)

        assert isinstance(response.json(), dict)
        assert response.status_code == 404
        assert set(summoner_not_found_keys[0]).issubset(response.json().keys())
        assert set(summoner_not_found_keys[1]).issubset(response.json()[summoner_not_found_keys[0][0]].keys())

def test_insert_existing_summoner_account(summoner_that_exists_account_dict, summoners_that_exist_in_account_table):
    """Test inserting summoner into Account table that already exists.

    Expectations:
    The row_id returned from summoner_store() should be None because the summoner already
    exists in the Account table.
    """
    for summoner_name in summoners_that_exist_in_account_table:
        row_id = rapi.summoner_store(summoner_that_exists_account_dict)

        assert row_id == None

def test_database_connection(sqlite_database_name):
    connection = sqlite3.connect(sqlite_database_name)
    assert isinstance(connection, sqlite3.Connection)
    connection.close()