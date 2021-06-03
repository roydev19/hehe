import os
import requests
from utils import gdrive
from flask import Flask, jsonify, abort

MANIFEST = {
    "id": "roydev.stremio.googledrive",
    "version": "1.0.6",
    "name": "DNS_testing",
    "description": "If you know, you know.",
    "logo": "https://github.com/roydev19/hehe/raw/main/cover.jpg",
    "resources": ["stream"],
    "types": ["movie", "series"],
    "catalogs": []
}

app = Flask(__name__)
gd = gdrive()
gd.cf_proxy_url = os.environ.get('CF_PROXY_URL')


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['X-Robots-Tag'] = 'noindex'
    return resp


@app.route('/')
def init():
    return 'Addon is working. Click <a href="/resetcache">here</a> to reset stream cache.'


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)


@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)
    return respond_with({'streams': gd.get_streams(type, id)})


@app.route('/resetcache')
def reset_cache():
    gd.streams_cache = {}
    print("Stream cache has been reset!")
    return 'Successfully reset stream cache!'


if __name__ == '__main__':
    app.run(debug=True)
