from flask import Flask, request, session, redirect, url_for, render_template
import json
import base64
import hashlib
import hmac
from config import public_key, private_key

app = Flask(__name__)

app.debug = True
app.secret_key = 'THE_SECRET_KEY'


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

@app.route("/", methods=['GET'])
def home():
    # If you're not logged in, go back to login page
    if 'username' not in session.keys() or session['username'] == '':
        return render_template('login.html')
    else: # If you are logged in 
    	return render_template('home.html', user=session['username'])

# Login page
@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        with open('users.json') as data_file:    
            data = json.load(data_file)
        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return render_template('home.html', user=session['username'])
        return render_template('login.html')  
    else:
        return render_template('login.html')

@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = ''
    return render_template('login.html')



@app.route('/invoice', methods=['GET', 'POST'])
def invoice_home():
	if(request.method == 'GET'):
	    if 'username' not in session.keys() or session['username'] == '':
	        return render_template('login.html')
	    session['invoice'] = ''
	    company = ''
	    phone = ''
	    address = ''
	    with open('users.json') as data_file:    
	            data = json.load(data_file)
	            for user in data['users']:
	                if user['username'] == session['username']:
	                    company = user['company']
	                    phone = user['phone']
	                    address = user['address']
	    return render_template("invoice.html", user=session['username'], company=company, phone=phone, address=address)
	else:

		memo = request.form["memo"]
		email = request.form["email"]
		amount = request.form["amount"]
		name = request.form["name"]
		phone = request.form["phone"]
		dueDate = request.form["due"]

		invoice_json = { 
		"Service": memo,
		"Customer": name,
		"Email": email,
		"Phone": phone,
		"Amount": amount,
		"DueDate": dueDate,
		"Status": "Unpaid"
		}

		with open('invoices.json') as data_file:    
			data = json.load(data_file)

        data['invoices'].append(invoice_json)

    	with open('invoices.json', 'w') as f:
        	json.dump(data, f)

        return render_template("home.html", user=session['username'])



@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run()