#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from modules.detect_cms import *
from modules.export_results import *

def read_input(path,cms_target,export):

	""" FUNCTION READ DOMAIN """
	extension = path.split(".")[1]
	cms_domains=[]
	cms_resolution=[]
	versions = []
	version = False
	d = []
	try:
		if extension == "json":
			#Open and read the file n json format
			with open(path) as json_data:
				d =json.loads(json_data.read())
		if extension == "txt":
			with open(path) as f:
				lines = f.readlines() 
				for line in lines:
					d.append(line.rstrip('\n'))
				f.close()
		for url in d:
			cms_domains.append(url)
			(cms, version)= detect_cms.detect_cms(url,cms_target)
			cms_resolution.append(cms)
			versions.append(version)
		#Visu CMS stadistics
		detect_cms.VisuStadistics(cms_resolution)
		#Export Results
		export_results.export_results(cms_domains,cms_resolution,versions,export)
	except Exception as e:
		print e
		return False