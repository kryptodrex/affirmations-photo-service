import requests
import json
import random
import base64
import os
import zlib

import apiEndpoints as endpoint

from dotenv import load_dotenv
load_dotenv()

keys = {
    'languageApiKey': os.getenv("LANGUAGES_APIKEY"),
    'unsplashApiKey': os.getenv("UNSPLASH_APIKEY")
}


def affirmations(token):
    reloadToken = str(token)

    # Check if there is a reloadToken (base64 encoded affirmation text)
    if (reloadToken == 'None'):
        # Get a new affirmation from API
        response = (requests.get(endpoint.affirmations)).json()
        affirmationText = response['affirmation']

        entity = (analyzeTextEntities({
            'text': affirmationText
        }))['result']
        # affirmationText = response['affirmation'].replace("'","\'")
        # print(affirmationText)

        if (entity != ""):
            strToEncode = affirmationText + '|' + entity
        else:
            strToEncode = affirmationText + '|'

        message_bytes = strToEncode.encode()
        base64_bytes = base64.b64encode(message_bytes)
        reloadToken = base64_bytes.decode()
    else:
        # Decode the existing reloadToken into its affirmation text and entity
        base64_bytes = reloadToken.encode()
        message_bytes = base64.b64decode(base64_bytes)
        decodedStr = message_bytes.decode()
        
        affirmationText = decodedStr.split("|")[0]
        entity = decodedStr.split("|")[1]

    return {
        'affirmation': affirmationText,
        'reloadToken': reloadToken,
        'entity': entity
    }

# Calls the Google Cloud NLP API to extract entities
def analyzeTextEntities(textToAnalyze):
    jsonBody = json.dumps({
        'document': {
            'type': 'PLAIN_TEXT',
            'content': textToAnalyze['text']
        },
        'encodingType': 'UTF8'
    })

    # Call Google language API to get entities from text    
    response = (requests.post(
        url=endpoint.languageApi + '/documents:analyzeEntities', 
        data=jsonBody, 
        params={
            'key': keys['languageApiKey']
        }
    )).json()

    if (len(response['entities']) != 0):
        responseText = response['entities'][0]['name']
    else: 
        responseText = ""

    return {
        'result': responseText
    }

# Calls Unsplash's photo API to retrieve a photo based on search query
def searchPhotos(search, size):
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

    return returnPhotoData(random.choice(response['results']), size)

# Calls Unsplash photo API to get one photo by its ID
def getPhotoById(photoId, size):
    response = (requests.get(
        url=endpoint.unsplash + '/photos/' + photoId,
        headers={
            'Authorization': 'Client-ID ' + keys['unsplashApiKey']
        }
    )).json()

    return returnPhotoData(response, size)

# Trigger download for photo
def downloadPhoto(photoId):
    response = (requests.get(
        url=endpoint.unsplash + '/photos/' + photoId + '/download',
        headers={
            'Authorization': 'Client-ID ' + keys['unsplashApiKey']
        }
    )).json()
    return {
        'message': 'Download successful',
        'link': response['url']
    }

# Create the response for the photo data
def returnPhotoData(data, size):
    return {
        'alt_description': '' if 'None' else data['alt_description'],
        'photo_id': data['id'],
        'urls': {
            'direct': data['urls'][size],
            'download': data['links']['download'],
            'html': data['links']['html']
        },
        'user': {
            'name': data['user']['name'],
            'portfolio': '' if 'None' else data['user']['portfolio_url'],
            'profile': data['user']['links']['html']
        }
    }