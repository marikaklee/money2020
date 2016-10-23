from flask import Flask, request, session, redirect, url_for, render_template
import json
import base64
import hashlib
import hmac
from config import public_key, private_key
import httplib, urllib
import hashlib
import requests
from requests.auth import HTTPBasicAuth


app = Flask(__name__)

app.debug = True
app.secret_key = 'iF9SW2S6hFgCNpFXDpcoe17HaDWt5N'



@app.route("/check")
def check():
    amount=session.get("amount")
    vendor=session.get("vendor")
    email="marikalee15@gmail.com"
    firstName="Marika"
    lastName="Lee"

    return render_template('check.html', amount=amount, vendor=vendor, email=email, firstName=firstName,lastName=lastName)

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
def listAndPay():
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
		if(session.get('message') != ''):
			message = session['message']
			session['message'] = ''
			return render_template('showAndPayInvoices.html', invoices=invoices, message=message)
		else:
			return render_template('showAndPayInvoices.html', invoices=invoices, message="")

@app.route('/payInvoice', methods=['POST'])
def payInvoice():
    vendor = request.form["vendor"]
    routingNumber = request.form["routingNumber"]
    accountNumber = request.form["accountNumber"]
    name = request.form["Name"]
    cardNumber = request.form["cardNumber"]
    expiryMonth = request.form["expiryMonth"]
    expiryYear = request.form["expiryYear"]
    cvv = request.form["cvv"]
    amount = float(request.form["amount"])

    if(cardNumber and expiryMonth and expiryYear and cvv and amount and routingNumber and accountNumber):

        hash_object = hashlib.sha512(cardNumber)
        hex_dig = hash_object.hexdigest()

        url = "https://sandbox.feedzai.com/v1/payments"
        data = {"user_id": name, "amount": amount, "currency": "USD", "payment_method": "card", "user_fullname": name,"card_fullname": name, "card_hash": hex_dig, "card_exp": expiryMonth + "/" + expiryYear, "billing_country": "US", "shipping_country": "US"}
        headers = {'Authorization': 'UIL7hxQQhziuyL+S9vQzr7WHibsBxXJkocGvs9DWoKzq/ZXExrqHXmr6vBBP:', 'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*'}

        response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth('UIL7hxQQhziuyL+S9vQzr7WHibsBxXJkocGvs9DWoKzq/ZXExrqHXmr6vBBP:', ''))
        
        jsonResponse = response.json()

        session["vendor"]=vendor
        session["amount"]=amount

        if jsonResponse[u'explanation'][u'likelyFraud'] is not False:
            session['message'] = "This transaction cannot be completed because we have identified this transaction as high risk for fraud."
            return redirect(url_for('listAndPay'))
        else:
          
            return redirect(url_for('check'))
    else:
        session['message'] = "This transaction cannot be completed because some form fields are missing."
        return redirect(url_for('listAndPay'))


@app.route('/invoice', methods=['GET', 'POST'])
def invoice_home():
	session['message'] = ''
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

        return redirect(url_for('listAndPay'))



@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run()

    