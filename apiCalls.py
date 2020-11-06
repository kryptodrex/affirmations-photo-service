import requests
import json
import random
import os

import apiEndpoints as endpoint

from dotenv import load_dotenv
load_dotenv()

keys = {
    'languageApiKey': os.getenv("LANGUAGES_APIKEY"),
    'unsplashApiKey': os.getenv("UNSPLASH_APIKEY")
}


def affirmations():
    response = requests.get(endpoint.affirmations)
    return response.json()

def analyzeTextEntities(input):
    jsonBody = json.dumps({
        'document': {
            'type': 'PLAIN_TEXT',
            'content': input['text']
        },
        'encodingType': 'UTF8'
    })

    # Call Google language API to get entities from text    
    response = requests.post(
        url=endpoint.languageApi + '/documents:analyzeEntities', 
        data=jsonBody, 
        params={
            'key': keys['languageApiKey']
        }
    )

    return response.json()

def searchPictures(search, size):
    response = (requests.get(
        url=endpoint.unsplash + '/search/photos',
        params={
            'query': search,
            'content_filter': 'high',
            'per_page': 50
        },
        headers={
            'Authorization': 'Client-ID ' + keys['unsplashApiKey']
        }
    )).json()

    choosePhoto = random.choice(response['results'])

    photoData = {
        'url': choosePhoto['urls'][size],
        'user': {
            'name': choosePhoto['user']['name'],
            'portfolio': choosePhoto['user']['portfolio_url'],
            'profile': choosePhoto['user']['links']['html']
        }
    }

    return photoData