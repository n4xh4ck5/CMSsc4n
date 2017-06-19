#!/usr/bin/python  
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
#Define parameters with the last version of CMS
wordpress_version = '4.7.5'
drupal_version ='8.3.0'
joomla_version = '3.7'
prestashop_version = '1.7'
moodle_version = '3.2.2'

def ExportResults(data,cms,export):
	#var's of excel
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	#json
	if (export == 1):
		print "Exporting the results in a json"
		for domain in data:
			for j in cms:
				filename = "output_domains" + code + ".json"
				with open(filename, 'w') as f:
					json.dump(domain,j, f)
	#excel
	if (export ==2):
		print "Exporting the results in an excel"
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('Status_domains.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "Domain")
		worksheet.write(row, col+1, "cms")
		row += 1
		# Iterate over the data and write it out row by row.
		for domain in data:
				col = 0
				worksheet.write(row, col, domain)
				worksheet.write(row, col+1, cms[i])
				row += 1
				i += 1
		#close the excel
		workbook.close()

""" WORDPRESS FUNCTION """
def wordpressFunc(data,cms):
	soup=""
	wp_version =""
	#print data.status_code
	soup = BeautifulSoup(data.text, 'html.parser')
	global flag_wp
	#The first option is looking for /wp-content/ in source-font. Only one time enters in this if
	if cms == True:
		cms = False
		if data.text.find("wp-content") > 0:
			#It was a Wordpress
			print "wp-content detected in main webpage. Trying to detect the wordpress version"
			try:
				wp_version = soup.findAll(attrs={"name":"generator"})[0]['content'].replace("WordPress ", "")
				print "Version Wordpress detected in source font => " + wp_version
			except Exception as e:
				#print e
				print "It can't detect the wordpress version"
				pass
			return True	
		else:
			#print "It look likes a wordpress, reviewing possible paths readme.html"
			return False
	else:
		print data.status_code
	#CONSIDERAR REDIRECCIONES A PAGINA DE ERROR PERSONALIZADA Y DEVUELVE 30X -> 200!!!
	#Las redirecciones pueden falsearl os resultados
		if data.status_code == 200:
			if data.text.find("wp-admin") > 0:
				print "The CMS is a Wordpress! => readme.html file found"
				print "Trying to detect the wordpress version"
				#Parser HTML to <h1> to obtain version Wordpress
				try:
					#wp_version = str(str(str(soup.find_all('h1')[0]).split('<br />')[1]).split('\n')[0]).strip()
					wp_version = str(soup.find_all('h1')[0].getText().split('Version')[1].strip())
					print "Version Wordpress detected in /readme.html => " + wp_version
					if wp_version != wordpress_version:
						print "The version wordpress is outdated"
				except Exception as e:
					#print e
					pass
				print "It can't detect the wordpress version"
				return True
			else:
				#print "It is not a Wordpress"
				return False
		else:
			#Wordpress not detect throught readme.html in different possible paths
			#print "Unable to detect wordpress. No /readme.html file found."
			return False
	# Enter one time in wp-content not in somewhere, so False
	return False

""" MOODLE FUNCTION """
def moodleFunc(data,cms):
	version_moodle =0
	#print data.status_code
	if data.status_code == 200:
		if data.text.find("moodle") > 0:
			print "The CMS is a Moodle! => /lib/upgrade.txt file found. Trying to detect the version"
			#Use a regular expression to match the value contains in === X.X ===
			for version_moodle in data.text.split('\n'):
				try:
					if re.match(r"(^=== [0-9.]+ ===$)" ,version_moodle):
						print "Version Moodle detected in /lib/upgrade.txt " + version_moodle
						if version_moodle != moodle_version:
							print "The version Moodle is outdated"
							break
				except Exception as e:
					#print e
					print "It can't detect the moodle version"
			return True
	else:
		#print "Unable to detect Moodle. No /moodle/lib/upgrade.txt file found."
		return False

""" JOOMLA FUNCTION """
def joomlaFunc(data,cms):
	version_joomla =0
	#print data.status_code
	#Parser the code in xml
	xml = jxmlease.parse(data.text)
	version_joomla = xml['metafile']['version']
	#print  xml['metafile']['version']
	#print "ENTRA EN JOOMLA"
	if data.status_code == 404: #data es response.text
		#print "Unable to detect Joomla version. No /language/en-GB/en-GB.xml file found."
		return False
	try:
		print "The CMS is a Joomla! => /language/en-GB/en-GB.xml file found. Trying to detect the version"
		try:
			#Parser the code in xml
			xml = jxmlease.parse(data.text)
			version_joomla = xml['metafile']['version']
			#Obtain vesion to parse XML
			print "Version Joomla detected in /language/en-GB/en-GB.xml ==> Joomla " + version_joomla
			if version_joomla != joomla_version:
				print "The version Joomla is outdated"
		except Exception as e:
			#print e
			print "It can't detect the Joomla version"
		#if the path exists, return True, it a Joomla
		return True
	except:
		#print "Unable to detect Joomla version. No /language/en-GB/en-GB.xml file found"
		return False 
	#if it doesn't enter anywhere -> False
	#return False

""" DRUPAL FUNCTION """
def drupalFunc(data,cms):
	version_drupal =0
	if data.status_code == 404: #data es response.text
		#print "Unable to detect Drupal version. No CHANGELOG.txt file found."
		return False
	try:
		#print "Entra"
		drupal= data.text.find("Drupal")
		if data.text.find("Drupal") > 0:
			print "The CMS is a Drupal! => CHANGELOG.txt file found. Trying to detect the version"
			try: 
				version_drupal = data.text[drupal+7:12]
				#version_drupal = int(data.text[druf+7:9])
				print "Version Drupal detected in CHANGELOG.txt ==> Drupal " + version_drupal
				if version_drupal != drupal_version:
					print "The version Drupal is outdated"
			except:
				print "It can't detect the drupal version"
		return True
	except:
		#print "Unable to detect Drupal version. No CHANGELOG.txt file found."
		return False
""" Prestashop FUNCTION """
def prestashop(data,cms):
	version_prestashop = 0
	if data.status_code == 404: #data es response.text
		return False
		#print "Unable to detect Joomla version. No /language/en-GB/en-GB.xml file found."
	else: #200
		prestashop = data.text.find("prestashop")
		if data.text.find("prestashop") > 0:
			print "Prestashop CMS detected.Trying to detect the version."
			try:
				version_prestashop = data.text[prestashop+7:12]
				print "Version Prestashop detected in README.md ==> Prestashop " + version_prestashop
				if version_prestashop != prestashop_version:
					print "The version Prestashop is outdate"
			except Exception as e:
				#print e
				print "It can't detect the prestashop version"
			return True

def SendRequest(url,funName):
	cms = True
	try:
		response =""
		#print url
		try:
			response = requests.get("https://"+url, allow_redirects=True, timeout=5,verify=False)
		except requests.exceptions.RequestException as e:
			#print "\nError HTTPS " + url,e
			pass
		except requests.exceptions.ConnectTimeout as e:
			print "\nError timeout " + url,e
			pass
		response = requests.get("http://"+url, allow_redirects=True, timeout=5,verify=False)
	except requests.exceptions.RequestException as e:
		print "\nError connection to server! " + url,
		pass	
	flag= globals()[funName+"Func"](response,cms)
	return flag
def DetectCMS (url):
	flag = False
	cms =""
	print "\n",url
	if (flag == False):
		#WORDPRESS
		print "\n*****Checking if the CMS is a Wordpress*****"
		cms = "wordpress"
		#Look for "/wp-content" in source font
		flag = SendRequest(url,'wordpress')
		if flag == False:
			urlwordpress=url+"/readme.html"
			#if flag == False:
			while flag == False:
				flag = SendRequest(urlwordpress,'wordpress')
				if flag == False:
					#Initial urlwordpress to avoid before values
					urlwordpress = ""
					urlwordpress = url + "/wordpress/readme.html"
					flag = SendRequest(urlwordpress,'wordpress')
					if flag == False:
						urlwordpress = ""
						urlwordpress = url + "/wp/readme.html"
						flag = SendRequest(urlwordpress,'wordpress')
						if flag == False:
							urlwordpress =""
							urlwordpress = url + "/blog/readme.html"
							flag = SendRequest(urlwordpress,'wordpress')
							#MOODLE
							if flag == False:
								print "The CMS is not a Wordpress"
								print "\n*****Checking if the CMS is a Moodle*****"
								cms = "moodle"
								urlmoodle = url + "/lib/upgrade.txt"
								flag = SendRequest (urlmoodle,'moodle')
								if flag == False:
									urlmoodle =""
									urlmoodle = url + "/moodle/lib/upgrade.txt"
									flag = SendRequest (urlmoodle,'moodle')
								if flag == False:
									#DRUPAL
									print "The CMS is not a Moodle"
									print "\n*****Checking if the CMS is a Drupal*****"
									cms = "drupal"
									urldrupal = url + "/CHANGELOG.txt"
									flag = SendRequest (urldrupal,'drupal')
									if flag == False:
										#JOOMLA
										print "The CMS is not a Drupal"
										print "\n*****Checking if the CMS is a Joomla*****"
										cms ="joomla"
										urljoomla= url + "/language/en-GB/en-GB.xml"
										flag = SendRequest (urljoomla,'joomla')
										if flag == False:
											#PRESTASHOP
											print "The CMS is not a Joomla"
											print "\n*****Checking if the CMS is a Prestashop*****"
											cms ="prestashop"
											urlprestashop = url + "/README.md"
											flag = SendRequest (urlprestashop,'prestashop')
											if flag == False:
												#The url doesn't belong to a CMS
												cms = "Not a CMS"
		#else:
		#print colored(url," is " + cms,"red",attrs=["bold","blink"])
		print "\n"+ url," is " + cms
		#Only keep the True values of cms
		if flag == True:
			return cms
""" FUNCTION READ DOMAIN """
def ReadDomain(path,export):
	cms_domains=[]
	cms_resolution=[]
	#Open and read the file n json format
	with open(path) as json_data:
		d =json.loads(json_data.read())
		for url in d:
			try:
				cms_domains.append(url)
				cms = DetectCMS(url)
				cms_resolution.append(cms)
			except Exception as e:
				print url, e
		ExportResults(cms_domains,cms_resolution,export)

""" FUNCTION MAIN """
print "   _____ __  __  _____          _  _       "  
print "  / ____|  \/  |/ ____|        | || |      "  
print " | |    | \  / | (___  ___  ___| || |_ _ __  "
print " | |    | |\/| |\___ \/ __|/ __|__   _| '_ \ "
print " | |____| |  | |____) \__ \ (__   | | | | | |"
print "  \_____|_|  |_|_____/|___/\___|  |_| |_| |_|"                                                                                        
print """\n** Tool to scan if a domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and return the version
    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    ** Version 1.0
    ** DISCLAMER This tool was developed for educational goals. 
    ** The author is not responsible for using to others goals.
    ** A high power, carries a high responsibility!"""                                            
parser = argparse.ArgumentParser(description="This tool verifies if the domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and returns the version", formatter_class=RawTextHelpFormatter)
parser.add_argument('-e','--export', help="Indicate the type of format to export results.\n\t1.json (by default)\n\t2.xlsx",required=True)
parser.add_argument('-i','--input', help="File in json format which contains the domains want to know if they are a CMS",required=True)
args = parser.parse_args()
path = args.input
export = (int) (args.export)
if export is None:
	export=1
if ((export != 1) and (export !=2)):
	print "The export is not valid"
	exit(1)
#Call the function KnowState
ReadDomain(path,export)