#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlsxwriter

def export_results(domains,cms,version,export):
	#var's of excel
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	
	if (export =='y'):
		print "Exporting the results in an excel"
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('output.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "Domain")
		worksheet.write(row, col+1, "CMS")
		worksheet.write(row, col+2, "Version")
		row += 1
		# Iterate over the data and write it out row by row.
		for domain in domains:
				col = 0
				worksheet.write(row, col, domain)
				worksheet.write(row, col+1, cms[i])
				worksheet.write (row, col+2, version[i])
				row += 1
				i += 1
		#close the excel
		workbook.close()
	else:
		#Not Export
		exit(0)
