from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = request.args.get('url')
    if not url:
        return jsonify(error="Missing 'url' parameter"), 400

    headers = {
        'User-Agent': request.headers.get('User-Agent'),
        'Accept-Language': request.headers.get('Accept-Language')
    }

    params = request.args.to_dict()
    params.pop("url")

    try:
        resp = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return resp.content, resp.status_code, headers

def create_app():    
    app.run(debug=True, port=8000)
