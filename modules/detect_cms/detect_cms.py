#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.wordpress import *
from modules.moodle import *
from modules.joomla import *
from modules.drupal import *
from modules.prestashop import *

def VisuStadistics(data):
	"""VisuStadistics"""
	try:
		wordpress_count=0
		joomla_count=0
		moodle_count=0
		drupal_count=0
		prestashop_count=0
		no_cms = 0

		for cms in data:
			if cms == 'wordpress':
				wordpress_count+=1
			if cms == 'moodle':
				moodle_count+=1
			if cms == 'joomla':
				joomla_count += 1
			if cms == 'drupal':
				drupal_count += 1
			if cms == 'prestashop':
				prestashop_count += 1
			if cms == None:
				no_cms += 1
		print "\n### CMS Stadistics ###"
		print "Wordpress detected: " + str (wordpress_count)
		print "Moodle detected: " + str (moodle_count)
		print "Joomla detected: " + str (joomla_count)
		print "Drupal detected: " + str (drupal_count)
		print "Prestashop detected: " + str (prestashop_count)
		print "No CMS detected: " + str (no_cms)		
	except Exception as e:
		print e

def detect_cms(url,cms_target):
	"""FUNCTION detect_cms"""
	flag = False
	version_cms = None
	cms = False
	try:
		print "\n" + str(url)
		if (flag == False) and (cms_target=='W' or cms_target == 'A'):
			#Wordpress
			cms = 'wordpress'
			(flag, version_cms) = wordpress.identify_wordpress(url)

		if (flag == False) and (cms_target=='M' or cms_target == 'A'):
			#MOODLE
			cms = 'moodle'
			(flag, version_cms) = moodle.identify_moodle (url)

		if (flag == False) and (cms_target=='J' or cms_target == 'A'):
			#JOOMLA
			cms = 'joomla'
			(flag, version_cms) = joomla.identify_joomla (url)	

		if (flag == False) and (cms_target=='D' or cms_target == 'A'):
			#DRUPAL
			cms = 'drupal'
			(flag, version_cms) = drupal.identify_drupal (url)

		if (flag == False) and (cms_target=='P' or cms_target == 'A'):
			#Prestashop
			cms = 'prestashop'
			(flag, version_cms) = prestashop.identify_prestashop (url)

		print "\n"+ str(url)+" is " + str(cms)+ " " + str(version_cms)
	
	except Exception as e:
		print e
	finally:
		return cms, version_cms