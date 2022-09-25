#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testTuyaConnect.py
#  
#  Copyright 2022  <pi@RPi3ShedPower>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# Standard library imports
from datetime import datetime
from shutil import copyfile
from sys import exit as sys_exit
import os
from time import sleep as time_sleep

from tuyaConnect import class_tuyaConnect


#config = class_config(logTime)
connector = class_tuyaConnect("Passtest")
print("Number of Devices : ",len(connector.devices) +1)
ind = 0
for alldevices in connector.devices:
	print("device : ", ind)
	print("Name : " ,connector.devices[ind]['name'])
	print("id : ",connector.devices[ind]['id'])
	print("key : ",connector.devices[ind]['key'])
	print("mac : ",connector.devices[ind]['mac'])
	print("\n")
	#print("Propertie: ",connector.properties[ind])
	ind += 1
	
	
print("\n","Thats it for now")
sys_exit()



