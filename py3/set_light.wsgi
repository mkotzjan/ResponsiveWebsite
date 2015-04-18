#!/usr/bin/env/python3

import json
import subprocess
from cgi import parse_qs, escape

def application(environ, start_response):

	status = '200 OK'
	d = parse_qs(environ['QUERY_STRING'])
	room = d.get('room', [''])[0]
	room = escape(room)

	output = {}

	if str(room) == 'room1':
		pset(17, 1)
		if check(17) == 1:
			output[str(room)] = True
		else:
			output[str(room)] = False
			status = '400 Bad Request'
	elif str(room) == 'room2':
		pset(18, 1)
		if check(18) == 1:
			output[str(room)] = True
		else:
			output[str(room)] = False
			status = '400 Bad Request'
	else:
		status = '400 Bad Request'

	output = json.dumps(output)
	response_body = output

	response_headers = [('Content-Type', 'text/plain'),
						('Content_Length', str(len(response_body)))]

	start_response(status, response_headers)
 
	return [response_body]

def check(pin):
	if subprocess.check_output(["gpio", "-g", "read", str(pin)]) == b'1\n':
		return 1;
	elif subprocess.check_output(["gpio", "-g", "read", str(pin)]) == b'0\n':
		return 2;
	else:
		return 3;

def pset(pin, value):
	subprocess.call(["gpio", "-g", "write", str(pin), str(value)])

