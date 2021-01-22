from flask import Flask, g, redirect, url_for, escape, request, session, send_from_directory, render_template, send_file, make_response
import sys
import random
import pprint
import time
import os
import json
import traceback
import zipfile
import hashlib
import importlib

## protection by login
from functools import wraps
from config import USERS_CREDENTIALS
import goog_sendemail
import goog_spread_api


def protected(fnz):
	@wraps(fnz)
	def f(*args, **kwargs):
		if not session.get("USER"):
			return login(*args, **kwargs)
		global USER
		USER = session.get("USEROBJ")
		return fnz(*args, **kwargs)
	return f

VERSION = "1.0.0"
app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)

MAINPROJECTTITLE = "Flask + Python access to Google Spreadsheet via API"
MAINLOGINTITLE = MAINPROJECTTITLE + " - Login"
LEFTPANELTITLE = "Function Panel"
COPYRIGHT = "&copy; Somebody - 2020"

def errormsg(msg, info='info', specmsg=''):
	return render_template("error_msg.html", msg=msg, tipoinfo=info, specmsg=specmsg)

def checkUser(username, password):
	# modifica questa procedura se hai l'autenticazione su DB
	info = USERS_CREDENTIALS.get(username, None)
	if not info or info['password'] != password:
		return None
	return {
		"username": username,
		"description": info["description"],
		"role": info["role"],
		"preferences": {
			"lang": "IT",
		},
	}


@app.route('/')
@app.route('/home')
@protected
def home():
	HOMETITLE = "Home page"
	return render_template("home.html", MAINPROJECTTITLE=MAINPROJECTTITLE, **vars())

@app.route('/login')
def login():
#	global MAINLOGINTITLE
	return render_template("login.html", MAINLOGINTITLE=MAINLOGINTITLE)

@app.route('/check', methods=['POST'])
def check():
	username = request.form.get('usr', "")
	password = request.form.get('pwd', "")

	result = {
		"status": "KO"
	}
	userinfo = checkUser(username, password)
	if userinfo:
		session["USER"] = username
		session["USEROBJ"] = userinfo
		result["status"] = "OK"

	return json.dumps(result)

@app.route('/logout')
def logout():
#	print(session.items())
#	print(session.keys())
	try:
		del session["USER"]
		del session["USEROBJ"]
	except:
		print("NO KEYS PRESENT")
	return home()

@app.route('/images/<path:path>')
def send_images(path):
	 return send_from_directory('static/images', path)

@app.route('/static/<path:path>')
def send_static(path):
	 return send_from_directory('static', path)

@app.route('/showSpreadsheetContent')
@protected
def showSpreadsheetContent():
	(status, html) = goog_spread_api.home(session)
	return genericJsonResponse(status, html)


@app.route('/sendEmail/<to_address>')
@protected
def sendEmail(to_address):
	print("Sending mail to ", to_address)
	send_result = goog_sendemail.inviaMail("Primo messaggio con python e Gmail spreadsheet", 
												to_address, 
												"Il testo della mia mail")
	print(send_result)
	if send_result:
		return render_template("home.html", MAINPROJECTTITLE="Mail inviata", **vars())
	else:
		return render_template("home.html", MAINPROJECTTITLE="Mail NON inviata", **vars())

def genericJsonResponse(status, html):
    result = {
        "status": status,
        "html": html
    }
    return json.dumps(result)


if __name__ == '__main__':

	import sys

	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 9500

	app.secret_key = "mysecretkey"
	app.config["TEMPLATES_AUTO_RELOAD"] = True
	app.run(
		host="0.0.0.0",
		port=port,
	)
