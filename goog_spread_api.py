# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import Flask, g, redirect, url_for, escape, request, session, send_from_directory, render_template, send_file, jsonify
import random
import importlib
import pprint
import functools

import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime

import logging


from config import app_config

RELOAD=True
SAMPLE_SPREADSHEET_ID = app_config['SAMPLE_SPREADSHEET_ID']


def readFromGoogleSheet():
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
	client = gspread.authorize(creds)
	#print(client.auth.__dict__)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
	# Extract and print all of the values
	rows = sheet.get_all_records()

	return rows

def home(session, USER=None, _duplicated_row_id=None):
	goog_spread_rows = readFromGoogleSheet() # reload real data from GSuite
	print(goog_spread_rows)
	return "OK", render_template("ajax_lines.html", pagetitle="Google Spreadsheet Content", **vars())


if __name__ == '__main__':
	goog_spread_rows = readFromGoogleSheet()
	print(goog_spread_rows)
