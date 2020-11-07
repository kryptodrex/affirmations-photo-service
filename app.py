from flask import Flask, request, abort
from flask_cors import CORS
import json
import base64

import apiCalls as api

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

basePath = '/api/v1'

@app.route(basePath + '/')
def service_status():
    return 'Service is up and working!'

@app.route(basePath + '/affirmation', methods=['GET'])
def get_affirmation():
    reloadToken = request.args.get('reloadToken')
    data = api.affirmations(reloadToken)
    return data

# Analyze the text for its entities
@app.route(basePath + '/analyze-entities', methods=['POST'])
def post_text():
    data = api.analyzeTextEntities(json.loads(request.data))
    return data

# Retrieve a random photo based on search query
@app.route(basePath + '/photos', methods=['GET'])
def get_photos():
    queries = {
        'search': request.args.get('search'),
        'size': request.args.get('size')
    }
    
    data = api.searchPhotos(queries['search'],queries['size'])
    return data

# Retrieve a photo by its ID
@app.route(basePath + '/photos/<photoId>', methods=['GET'])
def get_photoById(photoId):
    size = request.args.get('size')
    data = api.getPhotoById(photoId, size)
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