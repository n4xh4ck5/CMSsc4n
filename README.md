# CMSsc4n

 Tool to identify if a domain has got a CMS and determine his version.
 
 At the moment, CMSs supported by CMSsc4n are WordPress,Moodle,Joomla,Drupal and Prestshop.
 
 # Instalation

You can download the latest version of CMSmap by cloning the GitHub repository:

Install the dependencies via pip:

<pre> pip install -r requirements.txt </pre>

# Use

<pre>
python cmssc4n.py -h
usage: cmssc4n.py [-h] [-e EXPORT] [-c CMS] -i INPUT

This tool verifies if the domain is a CMS (Wordpress , Drupal, Joomla, Prestashop or Moodle) and returns the version

optional arguments:
  -h, --help            show this help message and exit
  -e EXPORT, --export EXPORT
                        File in xlsx format which contains the domains want to know if they are a CMS (y/n)
  -c CMS, --cms CMS     Identify a CMS: W-Wordpress, J-Joomla, D-Drupal, M-Moodle or P-PrestaShop.Default:All
  -i INPUT, --input INPUT
                        Input in txt o json with the domains which it wants to analyze
</pre>
