from flask import Flask, request
import json

import apiCalls as api

app = Flask(__name__)

basePath = '/api/v1'

@app.route(basePath + '/')
def service_status():
    return 'Service is up and working!'

@app.route(basePath + '/affirmation', methods=['GET'])
def get_affirmation():
    data = api.affirmations()
    return data

@app.route(basePath + '/analyze-entities', methods=['POST'])
def post_text():
    data = api.languageProcessing(json.loads(request.data))
    return data

@app.route(basePath + '/pictures', methods=['GET'])
    searchText = request.args.get('search')
    data = api

if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000