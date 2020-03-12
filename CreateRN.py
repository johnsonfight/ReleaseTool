import time
import os, sys
import configparser #-

config = configparser.ConfigParser() #-
config.read('readConfig.ini') #-


date_year = config.get('date', 'year')
date_month = config.get('date', 'month')
date_day = config.get('date', 'day')

user_account = config.get('user', 'account') 

platform_generation = config.get('platform', 'generation')
platform_codeName = config.get('platform', 'codeName') 
platform_subCodeName = config.get('platform', 'subCodeName')
platform_systemName = config.get('platform', 'systemName') 
platform_ver_major = config.get('platform', 'version_major')
platform_ver_minor = config.get('platform', 'version_minor')
platform_ver_main = config.get('platform', 'version_main')

schedule_block = config.get('schedule', 'block')
schedule_revision = config.get('schedule', 'revision')
schedule_softwareBundle = config.get('schedule', 'softwareBundle')

# ### test
Debug_Menu_checkbox = False

contents = []

if Debug_Menu_checkbox == True :
	DebugMenuONOFF_input = 'Enable'
elif Debug_Menu_checkbox == False :
	DebugMenuONOFF_input = 'Disable' # A-Can

Last_ver_RN_File_Name = f'{platform_systemName}-0{platform_ver_major}0{platform_ver_minor}0{1}.txt'
Last_ver_DellBiosVersion = 'DellBiosVersion_test.h'





class RN_data():
	def __init__(self, contents, row):
		self.contents = contents
		self.row = row

#
# Read RN of Last Version
#
def Read_last_version_RN(filename):
	try:
	    RN_last_ver = open(filename, 'r')
	    contents = RN_last_ver.read().splitlines()
	    contents_row = len(contents)
	    RN_last_ver.close()

	except IOError:
	    print(f'Can not find last version of Release Note {Last_ver_RN_File_Name}')

	return contents, contents_row



#
# Create this version of RN
#
def Create_this_version_RN(contents):
	RN_name = 'test_result'

	try:
	    RN = open(f'{RN_name}.txt', 'r')
	    RN.truncate(0) #clear the file
	    RN.close()

	except IOError:
	    RN = open(f'{RN_name}.txt', 'w+')
	    RN.close()
	    # logging.info(f'RN has been created')


	# print(123)
	# string = 'Version:      '
	# contents[1].find(string)
	# with open(f'{RN_name}.txt', 'w+') as RN:
	# 	for line in contents:
	# 		RN.write("%s" % line)

def find_keywords_n_edit_RN(obj, keywords, DebugMenuONOFF):
	index = 0
	i = 0
	while i < obj.row - 1 :
		try:
			index = obj.contents[i].index(keywords)
			if keywords == find_Version:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{platform_ver_major}.{platform_ver_minor}.{platform_ver_main}'
			elif keywords == find_Release_Date:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{date_day}/{date_month}/{date_year}'
			elif keywords == find_SWB:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{schedule_softwareBundle}'
			elif keywords == find_DebugMenu:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{DebugMenuONOFF}' + ' in this version.'
			break

		except ValueError:
			i += 1
	return obj.contents


def find_keywords_n_edit_BV(obj, keywords, Platform):
	index = 0
	i = 0
	while i < obj.row:
		if obj.contents[i].find(f'{Platform}') != -1:
			j = i
			while j < i + 10:
				try:				
					index = obj.contents[j].index(keywords)
					if keywords == find_Major_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_major}'
						print(obj.contents[j])
						break
					elif keywords == find_Minor_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_minor}'
						print(obj.contents[j])
						break
					elif keywords == find_Main_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_main}'
						print(obj.contents[j])
						break
				except ValueError:
					j += 1
			break
		else :
			i += 1
		if i == obj.row :
			print(f"Didn't find {keywords} in {Last_ver_DellBiosVersion}")
	return obj.contents


[get_contents, get_row] = Read_last_version_RN(Last_ver_RN_File_Name)
[get_contents_BV, get_row_BV] = Read_last_version_RN(Last_ver_DellBiosVersion)
# print(get_contents_BV)
# print(get_row_BV)
# exit(1)


RN_obj = RN_data(get_contents, get_row)
# print(RN_obj.contents)
Bios_Ver_obj = RN_data(get_contents_BV, get_row_BV)


#
# (Const)
#
# [RN]
find_Version      = 'Version:      '
find_Release_Date = 'Release Date: '
find_SWB          = 'SWB#:         '
find_DebugMenu    = 'Debug Menu is '

# [DellBiosVersion]
keyword_Platform = f' {platform_codeName} version'
find_Major_ver = '#define DELL_BIOS_MAJOR_VERSION       '
find_Minor_ver = '#define DELL_BIOS_MINOR_VERSION       '
find_Main_ver  = '#define DELL_BIOS_MAIN_VERSION        '
#
#
#
list_keywords = [find_Version, find_Release_Date, find_SWB, find_DebugMenu]
for each_keywords in list_keywords : 
	new_contents = find_keywords_n_edit_RN(RN_obj, each_keywords, DebugMenuONOFF_input)

list_keywords = [find_Major_ver, find_Minor_ver, find_Main_ver]
for each_keywords in list_keywords : 
	new_contents = find_keywords_n_edit_BV(Bios_Ver_obj, each_keywords, keyword_Platform)


# i = 0
# while i < 10 :
# 	print(new_contents[i])
# 	i += 1

# i = 40
# while i < 50 :
# 	print(new_contents[i])
# 	i += 1	

# i = 0
# while i < 30 :
# 	print(get_contents_BV[i])
# 	i += 1	

# print(get_row_BV)


# contents = Read_last_version_RN()
# print(contents)
# Create_this_version_RN(contents)