#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from modules.send_request import *

def get_moodle_lastversion ():
	"""FUNCTION get_moodle_lastversion"""
	global MOODLE_LAST_CMS_VERSION
	try:
		url='https://download.moodle.org/'
		response = requests.get(url, allow_redirects=False, timeout=5,verify=False)
		soup = BeautifulSoup(response.text, "html.parser")
		lista=[]
		for i in soup.findAll(attrs={"href":"/releases/latest/"}):
			lista.append(''.join(i.findAll(text=True)))
		for x in lista: 
			if 'Moodle' in x:
				text= x.split(' ')
		MOODLE_LAST_CMS_VERSION = text[1].replace('+',' ')
	except Exception as e:
		print e
		MOODLE_LAST_CMS_VERSION= False

	finally:
		return MOODLE_LAST_CMS_VERSION

def moodleFunc(data):
	"""FUNCTION moodlefunc"""
	moodle_version =False
	version_moodle = None
	try:
		#Get the moodle last version
		if MOODLE_LAST_CMS_VERSION == False:
			print "Failed to obtain the last version"
		if data.status_code == 200:
			if data.text.find("moodle") > 0:
				cms = True
				print "The CMS is a Moodle! => /lib/upgrade.txt file found. Trying to detect the version"
				#Use a regular expression to match the value contains in === X.X ===
				for version_moodle in data.text.split('\n'):

					if re.match(r"(^=== [0-9.]+ ===$)" ,version_moodle):
						version_moodle = version_moodle.replace('=','')
						print "Version Moodle detected in /lib/upgrade.txt " + str(version_moodle)
						if version_moodle != MOODLE_LAST_CMS_VERSION:
							print "The version Moodle is outdated"
							break
					else:
						version_moodle = None
						cms = True
			else:
				version_moodle = None
				cms = False
		else:
			version_moodle = None
			cms = False
	except Exception as e:
		print e
		version_moodle = None
		cms = False

	finally:
		return cms, version_moodle


def identify_moodle (url):
	"""FUNCTION identify_moodle"""
	flag = False
	version_cms = False
	response = ""
	try:
		print "\n*****Checking if the CMS is a Moodle*****"
		#URL where it is the version
		urlmoodle = url + "/lib/upgrade.txt"
		response = send_request.send_request (urlmoodle)
		(flag, version_cms) = moodleFunc(response)
		if flag == False:
			#tipical URL where it is the version
			urlmoodle = url + "/moodle/lib/upgrade.txt"
			response = send_request.send_request (urlmoodle)
			(flag, version_cms) = moodleFunc(response)
	except Exception as e:
		print e

	finally:
		return flag, version_cms