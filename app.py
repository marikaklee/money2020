from flask import Flask, request, session, redirect, url_for
import json
import base64
import hashlib
import hmac

app = Flask(__name__)



def authorization_header(endpoint, verb, content_type, timestamp, public_key, private_key):
    """Generate Authroization header for Checkbook.io API requests

    Args:
        endpoint (str)- API endpoint (e.g. /v2/check)
        timestamp (str)- timestamp in HTTP Date header
        verb (str)- HTTP verb [GET, POST, PUT, DELETE]
        content_type (str)- HTTP content type (typically application/json for POST and empty for GET)
        public_key (str)- public API key
        private_key (str)- private API key
    """
    message = verb + content_type + timestamp + endpoint
    dig = hmac.new(private_key, msg=str(message), digestmod=hashlib.sha256).digest()
    sig = base64.b64encode(dig).decode()
    return '%s:%s' % (public_key, sig)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run()