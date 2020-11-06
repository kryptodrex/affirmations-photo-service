import requests
import json

import apiEndpoints as endpoint
import localConfig as config


def affirmations():
    response = requests.get(endpoint.affirmations)
    return response.json()

def languageProcessing(input):
    jsonBody = json.dumps({
        'document': {
            'type': 'PLAIN_TEXT',
            'content': input['text']
        },
        'encodingType': 'UTF8'
    })

    # Call Google language API to get entities from text    
    response = requests.post(
        url=endpoint.languageApi, 
        data=jsonBody, 
        params={
            'key': config.languageApi_key
        }
    )

    return response.json()

def pictures():
    