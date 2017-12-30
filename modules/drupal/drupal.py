#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from modules.send_request import *

def get_drupal_lastversion ():
	"""FUNCTION get_drupal_lastversion"""
	text = ""
	try:
		global DRUPAL_LAST_CMS_VERSION
		url='https://www.drupal.org/download'
		response = requests.get(url, allow_redirects=False, timeout=5,verify=False)
		soup = BeautifulSoup(response.text, "html.parser")
		lista=[]
		for i in soup.findAll(attrs={"class":"primary-button"}):
			lista.append(''.join(i.findAll(text=True)))
		for x in lista: 
			if 'Drupal' in x:
				text= x.split(' ')
		DRUPAL_LAST_CMS_VERSION = text[2]
		
	except Exception as e:
		print e
		DRUPAL_LAST_CMS_VERSION = False
	finally: 
		return DRUPAL_LAST_CMS_VERSION


def drupalFunc (data):
	"""FUNCTION drupalFunc"""
	drupal_version = False
	version_drupal = None
	try:
		#Get the drupal last version
		if DRUPAL_LAST_CMS_VERSION == False:
			print "Failed to obtain the last version"
		if data.status_code == 404:
			#Unable to detect Drupal version. No CHANGELOG.txt file found.
			version_drupal = None
			cms = False
			return cms, version_drupal
		drupal = data.text.find("Drupal")
		if data.text.find("Drupal") > 0:
			cms = True
			print "The CMS is a Drupal! => CHANGELOG.txt file found. Trying to detect the version"
			version_drupal = data.text[drupal+7:12]
			print "Version Drupal detected in CHANGELOG.txt ==> Drupal " + version_drupal
			if version_drupal != DRUPAL_LAST_CMS_VERSION:
				version_drupal = version_drupal
				print "The version Drupal is outdated"
			else:
				print "It can't detect the drupal version"
				version_drupal = None

		else:
			version_drupal = None
			cms = False
	except Exception as e:
		print e

	finally:
		return cms, version_drupal

def identify_drupal(url):
	"""FUNCTION identify_drupal"""
	response = ""
	flag = False
	try:
		print "\n*****Checking if the CMS is a Drupal ****"
		urldrupal =  url + "/CHANGELOG.txt"
		response = send_request.send_request (urldrupal)
		(flag, version_cms) = drupalFunc (response)
		if flag == False:
			urldrupal =  url + "drupal/CHANGELOG.txt"
			response = send_request.send_request (urldrupal)
			(flag, version_cms) = drupalFunc (response)
	except Exception as e:
		print e
	finally:
		return flag, version_cms