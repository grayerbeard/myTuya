#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of pwm_fanshim and is used for data logging
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :text_buffer.py
# description     :pwm control for R Pi Cooling Fan
# author          :David Torrens
# start date      :2019 11 20
# version         :0.1
# python_version  :3

# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
import os

###
# import paho.mqtt.client as mqtt
#from time import sleep as time_sleep
#from utility import make_time_text,fileexists
#from datetime import datetime
#from sys import exit as sys_exit

# Third party imports
# None

# Local application imports
from utility import pr,make_time_text,send_by_ftp,fileexists
from buffer_log import class_buffer_log

class class_text_buffer(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
	def __init__(self,headings,config,logtype,logTime):
		#initialization
		self.__config = config
		self.__config.logType = logtype
		print(" Buffer Init for : ",self.__config.prog_name," with a size of : ",self.__config.text_buffer_length, " and  width of : ", len(headings) + 1, " including time stamp")
		if not os.path.exists('log'):
		    os.makedirs('log')

		self.__source_ref = 0 # a number used to control prevention repeat messages
		self.__width = len(headings) + 1
		###                     
		#self.line_values = ["1"]*len(headings)
		
		self.line_values = {} 
		self.email_html = "<p> No Log yet </p>"
		self.__dta = [ [ None for di in range(self.__width+1) ] for dj in range(self.__config.text_buffer_length+1) ]
		self.__size = 0
		self.__posn = self.__config.text_buffer_length-1
		self.__headings = ["Time"]
		for hdg_ind in range(0,self.__width-1):
			#print(hdg_ind,headings[hdg_ind])
			self.__headings.append(headings[hdg_ind])
		#print(self.__headings)
		self.__pr_values = ["text"] * self.__width

		self.__html_filename = config.prog_name + "_" + self.__config.logType + ".html"
		self.__html_filename_save_as = config.prog_path + self.__html_filename
		self.__www_filename = config.local_dir_www + "/" + self.__html_filename
		try:
			self.__ftp_creds = config.ftp_creds_filename
		except:
			self.__ftp_creds = "" # ftp not in use
		self.__send_html_count = 0
		self.logFile = ""
		if self.__config.log_buffer_flag:
			self.__send_log_count = 0
			self.__log = class_buffer_log(self.__config,logTime)
			self.logFile = self.__config.log_directory + self.__log.log_filename
			wwwLogDir = self.__config.log_directory_www.replace(self.__config.local_dir_www, "")
			self.linkLogFile = wwwLogDir + "/" + self.__log.log_filename
			print("self.__config.log_directory : ",self.__config.log_directory)
			print("self.__log.log_filename : ", self.__log.log_filename)
			print("self.__config.log_directory_www : ", self.__config.log_directory_www)
			print("self.__config.local_dir_www : ", self.__config.local_dir_www)
			print("wwwLogDir : ", wwwLogDir)
			print("self.linkLogFile : ", self.linkLogFile)
		else:
			self.logFile = ""	
		#try:
		#	print("mqtt not installed")
			#self.__mqttc = mqtt.Client("python_pub")
			#self.__mqttc.connect(self.__config.broker_address, self.__config.broker_port) # use the ip of your rpi here
		#except:
			#print("mqtt cant connect")
			
	def size(self):
		return self.__config.text_buffer_length

	def update_buffer(self,values,appnd,ref):
		#append a line of info at the current position plus 1 
		# print("Update Buffer appnd and ref are : ",appnd,ref)
		###
		#print("Growing Buffer?  : ",self.__size," >> ",self.__config.text_buffer_length)
		
		
		if (self.__size == 0) and appnd == False:
			appnd = True
			print("Made append true when size zero")
		elif (self.__size == 0):
			print("size zero but append not False")
		
		i = 0
		for value in values:
			self.__dta[self.__posn][i] =value
			i += 1
		
		if appnd + (self.__source_ref != ref):
			#we adding message and incrementing posn
			if self.__size < self.__config.text_buffer_length-1 :
				self.__size += 1
			if self.__posn == self.__config.text_buffer_length-1:
				# last insert was at the end so go back to beginning@@
				self.__posn = 0
			else:
				# first increment insert position by one
				self.__posn += 1
				# then insert a line full of values
			self.__source_ref = ref
		else:
			self.__source_ref = ref		
		if len(values) > self.__width :
			print("Width Error for :",self.__config.prog_name, len(values) , self.__width, values)
			sys.exit()
		###
		#for i in range(0,len(values)):
		#	self.__dta[self.__posn][i] = values[i]

		
		# ##############################################################################
		#  Test WAS HERE
		#i = 0
		#for value in values:
		#	self.__dta[self.__posn][i] = value
		#	i += 1

		#print("Buffer updated and log buffer flag is : ",self.__config.log_buffer_flag)
		if self.__config.log_buffer_flag and appnd:
			self.__log.log_to_file(self.__headings,values)
			#print("Data to text logging")
			#print(self.__headings)
			#print(values)
			
			
			
			if fileexists(self.__www_filename):
				try:
					self.__log.copy_log_to_www(False)
				except:
					print("Failed to copy log file to www because this not there: ",self.__www_filename)
			#send log file to website configevery ten scans
			
			# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   NEXT    Needs to be time based @@@@@@@@@@@@@@@@@@@@@@@@@
			
			
			if self.__send_log_count > 10 and fileexists(self.__ftp_creds):
				self.__log.send_log_by_ftp(False,self.__config.log_directory,self.__config.ftp_timeout)
				self.__send_log_count = 0
			else:
				self.__send_log_count += 1
 
	def get_line_dta(self, key):
		#return stored element from position relative to current insert position in buffer
		line_dta = [" - "]*self.__width 		
		if (self.__posn-key) > -1:
			# need to take values from arlogea before current insert position
			for i in range(self.__width):
				line_dta[i] = self.__dta[self.__posn-key][i]
			return(line_dta)
		else:
			# need to take values from after current insert position
			for i in range(self.__width):
				#following two lines used too debug the calc to get the lower part of status file
				#print("That Calc key,self.__size,self.__config.text_buffer_length, self.__posn-key,key sum",
				 #  key,self.__size,self.__config.text_buffer_length, self.__posn-key,(self.__posn-key),self.(self.__config.text_buffer_length + (self.__posn-key))
				line_dta[i] = self.__dta[self.__config.text_buffer_length + (self.__posn-key)][i]
			return(line_dta)	

	def get_dta(self):
		# get all the data inserted so far, or the whole buffer
		all_data = [ [ None for di in range(self.__width+1) ] for dj in range(self.__config.text_buffer_length+1) ]
		for ind in range(0,self.__size):
			line_dta = self.get_line_dta(ind)
			# Following line for debug data from Buffer
			# print("get_dta >>>",ind,line_dta)
			for i in range(len(line_dta)):    
				all_data[ind][i] = line_dta[i]
		return(all_data)

	def pr(self,appnd,ref,logTime,refresh_interval):
		here = "buffer.pr for " + self.__config.prog_name
		make_values = [" -- "]*self.__width
		prtime = logTime
		for_screen = make_time_text(logTime)
		# following alternative will show more resolution for fractions of a second
		# for_screen = log_time.strftime('%d/%m/%Y %H:%M:%S.%f')      
		make_values[0] = for_screen
		file_start = f'''<head>
<meta http-equiv="refresh" content={str(refresh_interval)}/>
</head>
<caption>{self.__config.location} Buffer Display</caption>'''
		tbl_start = """ <p>
<table style="float: left;" border="1">
<tbody>"""
		tbl_start_line = """<tr>"""
		tbl_end_line = """</tr>"""
		tbl_start_col = """<td>"""
		tbl_end_col= """</td>"""
		tbl_end = """</tbody>
</table>"""
		file_end = """
</body>
</html>"""
		i = 0
		for key in self.line_values:
			make_values[i+1] = self.line_values[key]
			for_screen = for_screen + " " + str(self.line_values[key])
			i += 1
		print(for_screen)

		self.update_buffer(make_values,appnd,ref)
		with open(self.__html_filename,'w') as htmlfile:
			htmlfile.write(file_start)
			if self.__config.log_buffer_flag:			
				htmlfile.write('<p>' + self.__html_filename + ' : ' + 
					make_time_text(logTime)  + '      ' +
					'<a href= "' + self.linkLogFile + 
					'" target="_blank"> View the CSV Log File </a></p>\n<p>')
			else:
				htmlfile.write("<p>" + self.__html_filename + " : " + 
					make_time_text(logTime)  + "</p>\n<p>")
			htmlfile.write(tbl_start + tbl_start_line)
			self.email_html = tbl_start + tbl_start_line
			for ind in range(0,len(self.__headings)):
				htmlfile.write(tbl_start_col + self.__headings[ind] + tbl_end_col)
				self.email_html = self.email_html + tbl_start_col + self.__headings[ind] + tbl_end_col
			htmlfile.write(tbl_end_line)
			self.email_html = self.email_html + tbl_end_line
			buffer_dta = self.get_dta()
			for ind in range(self.__size):
				htmlfile.write(tbl_start_line)
				self.email_html = self.email_html + tbl_start_line
				if str(buffer_dta[ind][0]) != "None":
					for i in range(self.__width):
						htmlfile.write(tbl_start_col + str(buffer_dta[ind][i]) + tbl_end_col)
						self.email_html = self.email_html + tbl_start_col + str(buffer_dta[ind][i]) + tbl_end_col
				htmlfile.write(tbl_end_line)
				self.email_html = self.email_html + tbl_end_line
			htmlfile.write(tbl_end)
			self.email_html = self.email_html + tbl_end
			htmlfile.write(file_end)
			self.email_html = self.email_html + file_end
		
		try:
			if appnd != True:	
				copyfile(self.__html_filename, self.__www_filename)
		except:
			print("Not able to copy : ",self.__html_filename, " to ", self.__www_filename)
		
		#message =  self.line_values[1]
		
		#try:
		#	print("no mqtt")
		#	#self.__mqttc.publish(self.__config.topic,message,retain=True)
		#	#self.__mqttc.loop(2) #timeout = 2s
		#except:
		#	print("Mqtt cant send")
				
		if fileexists(self.__ftp_creds):
			if self.__send_html_count >= 3:
				# To debug FTP change end of following line to " = True"   !!!!!!!!!!!! 
				FTP_dbug_flag = False
				ftp_result = send_by_ftp(FTP_dbug_flag,self.__ftp_creds, self.__html_filename_save_as, self.__html_filename,"",self.__config.ftp_timeout)
				for pres_ind in range(0,len(ftp_result)):
					pr(FTP_dbug_flag,here, str(pres_ind) + " : ", ftp_result[pres_ind])
				self.__send_html_count = 0
			else:
				self.__send_html_count += 1
		return






