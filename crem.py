import requests
import urllib
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def get_access_token(base_url:str) -> str:
    r = requests.get(f'{base_url}/auth')
    r.raise_for_status()
    idp_url = r.url
    r2 = requests.post(
    idp_url, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }, data={
        "login": os.getenv('USERNAME'),
        "password": os.getenv('PASSWORD')
    })
    r2.raise_for_status()
    return r2.json()["id_token"]

def set_session_token(token:str) -> requests.Session:
    session = requests.session()
    session.proxies = urllib.request.getproxies()
    session.hooks = {
        'response': lambda r, *args, **kwargs: r.raise_for_status()
    }
    session.headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    return session

def get_terrain_list(path:str) -> list:
    df = pd.read_csv(path)
    terrain_list = df['abrev'].tolist()
    return terrain_list


def get_flight_from_date(url:str,session:requests.Session, start_date:str, end_date:str, time_filter_type:str) -> str:
    url = f'{url}/flight'
    params = {
        'start': start_date,
        'end': end_date,
        'time_filter_type': time_filter_type,
    }
    headers = {
        'accept': 'application/json'
    }
    response = session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")

    #terrain_list = get_terrain_list(os.getenv('TERRAIN_LIST_PATH'))
    #filtered_data = [flight for flight in data if flight['adep'] in terrain_list or flight['ades'] in terrain_list]
    terrain_list_string = os.getenv('TERRAIN_LIST')
    terrain_list = terrain_list_string.split(', ') if terrain_list_string else []

    filtered_data = [flight for flight in data if flight['ades'] in terrain_list]
    return filtered_data

def get_message_from_date(url:str,session:requests.Session, start_date:str, end_date:str) -> str:
    url = f'{url}/message'
    params = {
        'start': start_date,
        'end': end_date
    }
    headers = {
        'accept': 'application/json'
    }
    response = session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data



def get_message_flight_id(flight_messages_url:str) -> str:
    parsed_url = urlparse(flight_messages_url)
    query_params = parse_qs(parsed_url.query)
    message_flight_id = query_params.get('flight_id', [None])[0]
    return message_flight_id

def get_flight_message_from_id(url:str, session:requests.Session, message_flight_id:str) -> str:
    url = f'{url}/flightMessage'
    params = {
        'flight_id': message_flight_id
    }
    headers = {
        'accept': 'application/json'
    }
    response = session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
    return data
    