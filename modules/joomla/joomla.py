#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import jxmlease
import json
from bs4 import BeautifulSoup

from modules.send_request import *

def get_joomla_lastversion ():
	"""FUNCTION get_joomla_lastversion"""
	global JOOMLA_LAST_CMS_VERSION
	try:
		url = "https://downloads.joomla.org/api/v1/latest/cms"

		response = requests.get(url)
		data = json.loads(response.text)
		JOOMLA_LAST_CMS_VERSION = data['branches'][3]['version'] if data else False
	except Exception as e:
		print e
		JOOMLA_LAST_CMS_VERSION = False

	finally:
		return JOOMLA_LAST_CMS_VERSION

def joomlaFunc(data):
	"""FUNCTION joomlafunc"""
	joomla_version =False
	version_joomla= None
	cms = False
	try:
		#Get the joomla last version
		if JOOMLA_LAST_CMS_VERSION == False:
			print "Failed to obtain the last version"
		xml = jxmlease.parse(data.text)
		version_joomla = xml['metafile']['version']
		if data.status_code == 404: #data es response.text
		#Unable to detect Joomla version. No /language/en-GB/en-GB.xml file found."
			version_joomla = None
			cms = False
			return cms, version_joomla
		print "The CMS is a Joomla! => /language/en-GB/en-GB.xml file found. Trying to detect the version"
		cms = True
		#Parser the code in xml
		xml = jxmlease.parse(data.text)
		version_joomla = xml['metafile']['version']
		#Obtain vesion to parse XML
		print "Version Joomla detected in /language/en-GB/en-GB.xml ==> Joomla " + str(version_joomla)
		if version_joomla != JOOMLA_LAST_CMS_VERSION:
			print "The version Joomla is outdated"
	except:
		version_joomla = None
		cms = False
	finally:
		return cms, version_joomla

def identify_joomla (url):
	"""FUNCTION identify_joomla"""
	response = ""
	flag = False
	try:
		print "\n*****Checking if the CMS is a Joomla*****"
		urljoomla=  url + "/language/en-GB/en-GB.xml"
		response = send_request.send_request (urljoomla)
		(flag, version_cms) = joomlaFunc (response)
	except Exception as e:
		print e
	finally:
		return flag, version_cms