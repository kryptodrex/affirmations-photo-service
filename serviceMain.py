from flask import Flask, request, abort
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
    data = api.analyzeTextEntities(json.loads(request.data))
    return data

@app.route(basePath + '/photos', methods=['GET'])
def get_photoSearch():
    queries = {
        'search': request.args.get('search'),
        'size': request.args.get('size')
    }
    # print(queries)
    
    data = api.searchPictures(queries['search'],queries['size'])
    return data

### Error handling ###
@app.errorhandler(400)
def error_400():
    response = {
        "message": "Bad request"
    }
    return json.dumps(response)


if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000