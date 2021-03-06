import random
from urllib.parse import urlencode

import requests
import time

from Base.common import deprint
from Config.models import Config

try:
    client_id = Config.objects.get(key='unsplash-client-id').value
    secret = Config.objects.get(key='unsplash-secret').value
    redirect_uri = Config.objects.get(key='unsplash-redirect-uri').value
except:
    client_id = 'YOUR CLIENT ID'
    secret = 'YOUR SECRET'
    redirect_uri = 'YOUR REDIRECT URI'

host = 'https://unsplash.com'
api_host = "https://api.unsplash.com"
authorize_url = host + '/oauth/authorize'
token_url = host + '/oauth/token'
user_profile_url = api_host + '/me'
random_photo_url = api_host + '/photos/random'

random.seed(time.time())


def get_oauth_link():
    return '%s?client_id=%s&redirect_uri=%s&response_type=code&scope=public+read_user' \
           % (authorize_url, client_id, redirect_uri)


def get_access_token(code):
    params = {
        'client_id': client_id,
        'client_secret': secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code',
    }

    try:
        resp = requests.post(token_url, json=params)
        deprint('status_code', resp.status_code)
        deprint('token_url', token_url)
        if resp.status_code == 200:
            deprint('CONTENT -- ', resp.content)
            return resp.json()['access_token']
    except:
        return None


def get_user_profile(access_token):
    params = {
        'access_token': access_token,
    }
    params_encoded = urlencode(params)
    headers = {'content-type': 'application/json'}

    try:
        resp = requests.get(user_profile_url, params=params_encoded, headers=headers)
        if resp.status_code == 200:
            deprint('CONTENT -- ', resp.content)
            return resp.json()
        else:
            deprint('STATUS-CODE -- ', resp.status_code)
            return None
    except:
        return None


def get_random_photo(access_token):
    params = {
        'access_token': access_token,
    }
    params_encoded = urlencode(params)
    headers = {'content-type': 'application/json'}

    try:
        resp = requests.get(random_photo_url, params=params_encoded, headers=headers)
        if resp.status_code == 200:
            deprint('CONTENT -- ', resp.content)
            return resp.json()
        else:
            deprint('STATUS-CODE -- ', resp.status_code)
            return None
    except:
        return None
