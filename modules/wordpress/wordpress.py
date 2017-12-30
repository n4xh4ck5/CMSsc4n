#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, Comment
import re
import json

from modules.send_request import *

def get_wordpress_lastversion():
	global WORDPRESS_LAST_CMS_VERSION
	WORDPRESS_LAST_CMS_VERSION = False
	try:
		url="https://api.wordpress.org/core/version-check/1.7"		
		response = requests.get(url)
		data = json.loads(response.text)
		WORDPRESS_LAST_CMS_VERSION = data['offers'][0]['version'] if data else False

	except exception as e:
		print e
		WORDPRESS_LAST_CMS_VERSION = None

	finally: 
		return WORDPRESS_LAST_CMS_VERSION

def wordpressFuncXml(data):
	cms = False
	comment = ""
	version_match = None
	try:

		soup = BeautifulSoup(data.text, 'lxml')
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))

		if len(comments) > 0:
			cms = True	
			version_match = re.findall(r'(?:(\d+\.[.\d]*\d+))',comments[0])
			if len(version_match) > 0:
				version_match = version_match[0]
			if version_match != WORDPRESS_LAST_CMS_VERSION:
				print "The version wordpress is outdated or not identified"
			else:
				print "The version wordpress is updated"
			
	except Exception as e:
		print e
		version_match = None

	finally:
		return cms,version_match
	
def wordpressFunc(data,firstTime = False):
	"""FUNCTION wordpressfunc"""
	version_wordpress = None
	version_wordpress_ok = False
	soup=""
	cms = False
	try:
		
		if WORDPRESS_LAST_CMS_VERSION == False:
			print "Failed to obtain the last version"

		soup = BeautifulSoup(data.text, 'html.parser')
		#The first option is looking for /wp-content/ in source-font. Only one time enters in this if
		if firstTime == True:
			if data.text.find("wp-content") > 0:
				cms = True
				#It was a Wordpress
				print "wp-content detected in main webpage. Trying to detect the wordpress version"
				generator = soup.findAll(attrs={"name":"generator"});
				generator = generator[0] if len(generator) >= 1 else None
				
				if generator != None:
					
					version_wordpress = generator['content']
					version_wordpress = version_wordpress.replace("WordPress ", "")
					version_wordpress = version_wordpress.strip()
					
					print "Checking correct version number... ", version_wordpress
					if re.match(r'(?:(\d+\.[.\d]*\d+))',version_wordpress):
						version_wordpress_ok = True
					else:
						version_wordpress_ok = False
				else:
					
					version_wordpress = None
				
	
				print "Version Wordpress detected in source font => " + str(version_wordpress)
				if version_wordpress != WORDPRESS_LAST_CMS_VERSION or version_wordpress_ok == False:
					print "The version wordpress is outdated or it can't detect it"
				else:
					print "The wordpress is updated"
			else:
				cms = False
				version_wordpress = None
		else:
			if data.status_code == 200:
				if data.text.find("wp-admin") > 0:
					cms = True
					print "The CMS is a Wordpress! => readme.html file found"
					print "Trying to detect the wordpress version"
					#Parser HTML to <h1> to obtain version Wordpress
					
					h1s = soup.find_all('h1')
					h1s = h1s[0].getText() if len(h1s) > 0 else None
					if h1s:
						
						versions = h1s.split('Version')

						for ver in versions:
							if ver.strip() != '':
								version_wordpress = ver
								break

						print "Version Wordpress detected in /readme.html => " + str(version_wordpress)
					else:
						print "Version Wordpress NOT detected in /readme.html => " + str(version_wordpress)

					if version_wordpress != WORDPRESS_LAST_CMS_VERSION:
						print "The version wordpress is outdated or it can't detect it"
					else:
						print "The wordpress is updated"
						
				else:
					cms = False
					version_wordpress = None
			else:
				cms = False
				version_wordpress = None

	except Exception as e:
		print e

	finally:
		return cms, version_wordpress


def identify_wordpress (url):
	"""FUNCTION identify_wordpress"""
	flag = False
	version_cms = False
	response = ""
	try:
		print "\n*****Checking if the CMS is a wordpress****"
		#Look for "/wp-content" in source font
		response = send_request.send_request (url)
		(flag, version_cms) = wordpressFunc(response, True)
		
		if flag == False:
			urlwordpress = url+"/wp-links-opml.php"			
			response = send_request.send_request (urlwordpress)
			(flag, version_cms) = wordpressFuncXml(response)
		if flag == False:
			urlwordpress =""
			urlwordpress = url+"/readme.html"
			response = send_request.send_request (urlwordpress)
			(flag, version_cms) = wordpressFunc(response)
		if flag == False:
			#Initial urlwordpress to avoid before values
			urlwordpress = ""
			urlwordpress = url + "/wordpress/readme.html"
			response = send_request.send_request (urlwordpress)
			(flag, version_cms) = wordpressFunc(response)
		if flag == False:
			urlwordpress = ""
			urlwordpress = url + "/wp/readme.html"
			response = send_request.send_request (urlwordpress)
			(flag, version_cms) = wordpressFunc(response)
		if flag == False:
			urlwordpress = ""
			urlwordpress = url + "/blog/readme.html"
			response = send_request.send_request (urlwordpress)
			(flag, version_cms) = wordpressFunc(response)
		else:
			flag = True

	except Exception as e:
		print e

	finally:
		return flag, version_cms