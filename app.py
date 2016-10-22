from flask import Flask, request, session, redirect, url_for, render_template
import json
import base64
import hashlib
import hmac
from config import public_key, private_key

app = Flask(__name__)

app.debug = True
app.secret_key = 'iF9SW2S6hFgCNpFXDpcoe17HaDWt5N'



@app.route("/check")
def charge():
    return render_template('check.html')

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

@app.route('/listInvoices', methods = ['GET'])
def list():
	if 'username' not in session.keys() or session['username'] == '':
		return render_template('login.html')
	else:
		invoices = []
	
		with open('invoices.json') as data_file:    
			data = json.load(data_file)
		for invoice in data['invoices']:
			invoices.append({ 
        		"DueDate": invoice['DueDate'], 
        		"Vendor": invoice['Vendor'],
        		"Status": invoice['Status'],
        		"Amount": invoice['Amount'],
        		"Service": invoice['Service']
        		})
		print invoices
		return render_template('showAndPayInvoices.html', invoices=invoices)

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
		"Vendor": name,
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