#!/usr/bin/python

# require python > 2.6

import os
import re
import json
import time
from time import strftime
from collections import OrderedDict

import notification


#write json data to file
def write_log(command, ip_list, path, last_checked_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))):
	data = {
		"command": command,
		"last_checked_time": last_checked_time,
		"ip": ip_list
	}

	try:
		f = open(path,'w')
		f.write(json.dumps(data))
		f.close()
		return True
	except Exception, e:
		print e

#load log file
def load_log(path):
	with open(path) as data_file:
		data = json.load(data_file)
	return data

if __name__ == '__main__':
	with open('command_list.json') as command_list_file:
		commands = json.load(command_list_file)

	for key in commands:
		log_file_path 	= "log/current_%s.json" % key
		command 		= commands[key]

		current_check_time = strftime("%Y%m%d-%H-%M-%S", time.localtime(time.time()))
		response = os.popen(command).read()

		# remove first two lines to remove [server & address]
		response = '\n'.join(response.split('\n')[2:]) 

		# find ip from current string using regex
		current_ip_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response)

		# remove duplicate ip
		current_ip_list = list(OrderedDict.fromkeys(current_ip_list))

		# check is there a previous log file to be compared
		if os.path.isfile(log_file_path):
			# load previous ip list
			previous_log = load_log(log_file_path)
			previous_ip_list = previous_log['ip']
			# check equal
			if set(previous_ip_list) == set(current_ip_list):
				print "sama"

				# only update 'last_checked_time' at previous log.
				write_log(command, previous_log['ip'], log_file_path)
				
			else:
				print "beda. send notification. write log file"

				# log previous
				log_file_name = "log/%s-%s.json" % (key, current_check_time)
				write_log(command, previous_log['ip'], log_file_name, previous_log['last_checked_time'])

				# log current
				write_log(command, current_ip_list, log_file_path)

				print "sending notification..."
				try:
					# send notification
					notification.send_email(key, command, previous_ip_list, previous_log['last_checked_time'], current_ip_list, current_check_time)
				except Exception, e:
					print e
					print "error while sending notification"
				
				print "done."

		else:
			# no log file to be compared, so write the new one.
			write_log(command, current_ip_list, log_file_path)
			print "no log file. print a new one."