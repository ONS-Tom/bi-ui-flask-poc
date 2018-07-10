import requests
from flask import Blueprint, jsonify, current_app as app
from flask_login import login_required


api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')


@api_bp.route('/', methods=['POST'])
@login_required
def reroute():
    abc = app.config['SESSION_TYPE']
    print('abc is ', abc)
    response = requests.get('http://localhost:9000/v1/search?query=BusinessName:test')
    json = response.json()
    print("json is: ", json)
    return jsonify(json), 200
