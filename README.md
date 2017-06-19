# CMSsc4n
Tool to identify if a domain is a CMS such as Wordpress, Moodle, Joomla, Drupal or Prestashop

# Use

<pre>python cmssc4n.py -h </pre>
<pre>
   _____ __  __  _____          _  _       
  / ____|  \/  |/ ____|        | || |      
 | |    | \  / | (___  ___  ___| || |_ _ __  
 | |    | |\/| |\___ \/ __|/ __|__   _| '_ \ 
 | |____| |  | |____) \__ \ (__   | | | | | |
  \_____|_|  |_|_____/|___/\___|  |_| |_| |_|

** Tool to scan if a domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and return the version
    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    ** Version 1.0
    ** DISCLAMER This tool was developed for educational goals. 
    ** The author is not responsible for using to others goals.
    ** A high power, carries a high responsibility!
usage: cmssc4n.py [-h] -e EXPORT -i INPUT

This tool verifies if the domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and returns the version

optional arguments:
  -h, --help            show this help message and exit
  -e EXPORT, --export EXPORT
                        Indicate the type of format to export results.
                        	1.json (by default)
                        	2.xlsx
  -i INPUT, --input INPUT
                        File in json format which contains the domains want to know if they are a CMS</pre>
