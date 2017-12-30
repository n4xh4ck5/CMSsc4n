#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from modules.send_request import *

def get_prestashop_lastversion ():
	try:
		lista = []
		global PRESTASHOP_LAST_CMS_VERSION
		url='https://www.prestashop.com/en/download'
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		for i in soup.findAll('p',attrs={"class":"p-general"}):
			lista.append(''.join(i.findAll(text=True)))
		for x in lista: 
			if 'Latest' in x:
				version_match = re.findall(r'(?:(\d+\.[.\d]*\d+))',x)
				if len(version_match) > 0:
					version_match = version_match[0]
					PRESTASHOP_LAST_CMS_VERSION = version_match

	except Exception as e:
		print e
		PRESTASHOP_LAST_CMS_VERSION = False

	finally:
		return PRESTASHOP_LAST_CMS_VERSION

def prestashopFunc(data):
	"""FUNCTION prestashopFunc"""

	prestashop_version = False
	version_prestashop = None
	try:
		#Get the last prestashop version
		if PRESTASHOP_LAST_CMS_VERSION == False:
			print "Failed to obtain the last version"
		if data.status_code == 404: #data es response.text
			cms = False
			version_prestashop = None
		else: #200
			prestashop = data.text.find("prestashop")
			if data.text.find("prestashop") > 0:
				cms = True
				print "Prestashop CMS detected.Trying to detect the version."
				version_prestashop = data.text[prestashop+7:12]
				print "Version Prestashop detected in README.md ==> Prestashop " + version_prestashop
				version_prestashop = version_prestashop
				if version_prestashop != prestashop_version:
					print "The version Prestashop is outdate"
				else:
					print "It can't detect the prestashop version"
					version_prestashop = None
			else:
				cms = False
				version_prestashop = None

	except Exception as e:
		print e

	finally:
		return cms, version_prestashop

def identify_prestashop (url):
	"""FUNCTION identify_prestashop"""
	response = ""
	flag = False
	try:
		print "\n*****Checking if the CMS is a Prestashop*****"
		urlprestashop = url + "/README.md"
		response = send_request.send_request(urlprestashop)
		(flag, version_cms) = prestashopFunc (response)
	except Exception as e:
		print e
	finally:
		return flag, version_cms