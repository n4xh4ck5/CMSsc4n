#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def send_request(url):
	"""FUNCTION send_request"""
	flag =  False
	version_cms = False
	try:
		response =""
		try:
			response = requests.get("https://"+url, allow_redirects=True, timeout=5,verify=False)
		except requests.exceptions.RequestException as e:
			#print "\nError HTTPS " + url,e
			pass
		except requests.exceptions.ConnectTimeout as e:
			#print "\nError timeout " + url,e
			pass
		response = requests.get("http://"+url, allow_redirects=True, timeout=5,verify=False)

	except Exception as e:
		print e
	finally:
		return response