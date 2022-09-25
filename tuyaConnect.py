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

# title           :tuyaConnect.py
# description     :connect to Tuya devices to read status/data and control them
# author          :David Torrens
# start date      :2022 09 29
# version         :0.1
# python_version  :3

# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
import os
from time import sleep as time_sleep
# from os import path

# Special imports this module
import tinytuya

class class_tuyaConnect:
	# Tuya connect facilities

	def __init__(self,teststring):
		# Connect to Tuya Cloud
		self.tcloud = tinytuya.Cloud()  # uses tinytuya.json 
		self.devices = self.tcloud.getdevices()
		self.testString = teststring
		self.numDevices = len(self.devices)
		self.properties = [self.tcloud.getproperties(self.devices[0]['id'])]
		if self.numDevices > 0 :
			for ind in range(1,len(self.devices)):
				self.properties.append(self.tcloud.getproperties(self.devices[ind]['id']))
		
		
		
	def fff(self,ff1,ff2,ff3,ff4):



		# Display list of devicesapiKey
		
		print("Device List: %r" % devices)
		print("\n""\n")
		# Select a Device ID to Test
		#
		id = "bf5723e4b65de4a64fteqz"
		
		# Display Properties of Device
		result = c.getproperties(id)
		print("Properties of Switch 1:\n", result)
		print("\n""\n")
		# Display Status of Device
		result = c.getstatus(id)
		print("Status of Switch 1:\n", result)
		print("\n""\n")
		
		
		
		id = "bf6f1291cc4b30aa8d1wsv" # Code for sensor
		# Display Properties of Device
		result = c.getproperties(id)
		print("Properties of T & H Sensor:\n", result)
		print("\n""\n")
		# Display Status of Device
		result = c.getstatus(id)
		print("Status of T & H Sensor:\n", result)
		print("\n""\n")
		
		print("@@@@@@@@@@@@@@@@@")
		for sub in result:
			print(sub)
		print(result['result'][0]['value'])
		print("@@@@@@@@@@@@@@@@@")      
		    
		id = "bf5723e4b65de4a64fteqz" # Code for switch
		
		# Send Command - Turn on switch
		commands = {
			'commands': [{
				'code': 'switch_1',
				'value': True
			}, {
				'code': 'countdown_1',
				'value': 0
			}]
		}
		print("Sending command...")
		result = c.sendcommand(id,commands)
		print("Results\n:", result)
		
		time_sleep(10) 
		#sys_exit()
		
		# Send Command - Turn on switch
		commands = {
			'commands': [{
				'code': 'switch_1',
				'value': False
			}, {
				'code': 'countdown_1',
				'value': 0
			}]
		}
		print("Sending command...")
		result = c.sendcommand(id,commands)
		print("Results\n:", result)
		
		
		#----------------Test Module------------------------------
		if __name__ == '__main__':
			sys_exit()
