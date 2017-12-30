#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import jxmlease
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import xlsxwriter
from urlparse import urlparse
from bs4 import BeautifulSoup
import optparse
import argparse
from argparse import RawTextHelpFormatter
from pprint import pprint
import re
import sys

"""IMPORT MODULES"""

from modules.read_input import *
from modules.send_request import *
from modules.export_results import *
from modules.detect_cms import *
from modules.moodle import *
from modules.joomla import *
from modules.drupal import *
from modules.wordpress import *
from modules.prestashop import *
from modules.send_request import *


def banner():

	""" FUNCTION MAIN """
	print """   
		   _____ __  __  _____          _  _       
		  / ____|  \/  |/ ____|        | || |      
		 | |    | \  / | (___  ___  ___| || |_ _ __  
		 | |    | |\/| |\___ \/ __|/ __|__   _| '_ \ 
		 | |____| |  | |____) \__ \ (__   | | | | | |
		  \_____|_|  |_|_____/|___/\___|  |_| |_| |_|    """
	print " \n"
	print """ *** Tool to scan if a domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and return the version
	    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
	    ** Version 2.0
	    ** DISCLAMER: This tool was developed for educational goals. 
	    ** Github: https://github.com/n4xh4ck5/
	    ** The author is not responsible for using to others goals.
	    ** A high power, carries a high responsibility!"""  

def help ():
	"""FUNCTION HELP"""

	print  """ \nTool to scan if a domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and return the version

			Example of usage: python cmsc4n.py -i input.json"""

def main (argv):
	#global var to obtain the last CMS version
	global WORDPRESS_LAST_CMS_VERSION
	global JOOMLA_LAST_CMS_VERSION
	global MOODLE_LAST_CMS_VERSION
	global DRUPAL_LAST_CMS_VERSION
	global PRESTASHOP_LAST_CMS_VERSION

	""" FUNCTION MAIN """
	parser = argparse.ArgumentParser(description="This tool verifies if the domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and returns the version", formatter_class=RawTextHelpFormatter)
	parser.add_argument('-e','--export', help="File in xlsx format which contains the domains want to know if they are a CMS (y/n)",required=False)
	parser.add_argument('-c','--cms', help="Identify a CMS: W-Wordpress, J-Joomla, D-Drupal, M-Moodle or P-PrestaShop.Default:All",required=False)
	parser.add_argument('-i','--input', help="Input in txt o json with the domains which it wants to analyze",required=True)
	args = parser.parse_args()
	path = args.input
	cms = args.cms
	output = args.export
	#functions banner and help
	banner()
	help()

	try:
		#valid parameters input's
		if cms is None:
			cms = 'A'

		if output is None:
			output = 'n'
		output = output.lower()
		if (output != 'y' and output != 'n'):
			print "Incorrect output format selected."
			exit(1)
		#Obtain the CMS's last version
		print "\n Obtainning the CMS last versions...\n"
		WORDPRESS_LAST_CMS_VERSION = wordpress.get_wordpress_lastversion()
		print "Wordpress version: " + str(WORDPRESS_LAST_CMS_VERSION)
		MOODLE_LAST_CMS_VERSION = moodle.get_moodle_lastversion()		
		print "Moodle version: " + str(MOODLE_LAST_CMS_VERSION)
		JOOMLA_LAST_CMS_VERSION = joomla.get_joomla_lastversion()
		print "Joomla version: " + str(JOOMLA_LAST_CMS_VERSION)
		DRUPAL_LAST_CMS_VERSION = drupal.get_drupal_lastversion()
		print "Drupal version: " + str(DRUPAL_LAST_CMS_VERSION)
		PRESTASHOP_LAST_CMS_VERSION = prestashop.get_prestashop_lastversion()
		print "PrestaShop version: " + str(PRESTASHOP_LAST_CMS_VERSION)

		read_input.read_input(path,cms,output)
	except Exception as e:
		print e

# CALL MAIN
if __name__ == "__main__":
   main(sys.argv[1:])