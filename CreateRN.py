import time
import os, sys
import configparser #-
import git

config = configparser.ConfigParser() #-
config.read('readConfig_taurus.ini') #-

date_year    = config.get('date', 'year')
date_month   = config.get('date', 'month')
date_day     = config.get('date', 'day')

user_first_name = config.get('user', 'first_name')
user_last_name = config.get('user', 'last_name')

platform_generation  = config.get('platform', 'generation')
platform_codeName    = config.get('platform', 'codeName') 
platform_subCodeName = config.get('platform', 'subCodeName')
platform_systemName  = config.get('platform', 'systemName') 
platform_subCodeName_systemName = config.get('platform', 'subCodeName_systemName')
platform_ver_major   = config.get('platform', 'version_major')
platform_ver_minor   = config.get('platform', 'version_minor')
platform_ver_main    = config.get('platform', 'version_main')

schedule_block          = config.get('schedule', 'block')
schedule_revision       = config.get('schedule', 'revision')
schedule_softwareBundle = config.get('schedule', 'softwareBundle')
schedule_ESGB_number = config.get('schedule', 'ESGB_number')

git_repo_dell = config.get('git', 'repo_dell') 
git_working_branch = config.get('git', 'working_branch') 

# ### test
# X rev : True
# A can : False
Debug_Menu_checkbox = False

contents = []

if Debug_Menu_checkbox == True :
	DebugMenuONOFF_input = 'Enabled' # X rev
elif Debug_Menu_checkbox == False :
	DebugMenuONOFF_input = 'Disabled' # A-Can


#
# Files needed to be modified
#
# Leading_V_RN_File_Name = f'{platform_systemName}-0{platform_ver_major}0{platform_ver_minor}0{1}.txt'
Leading_V_RN_File_Name = f'R740-0{platform_ver_major}0{platform_ver_minor}0{4}.txt'
Last_ver_DellBiosVersion = 'DellBiosVersion_test.h'
Last_ver_PlatformConfig = 'PlatformConfig_taurus.txt'
LV_RN = 'R740-020704.txt'





class File_Data():
	def __init__(self, contents, row):
		self.contents = contents
		self.row = row

#
# Read RN of Last Version
#
def Read_last_version_File(filename):
	try:
	    RN_last_ver = open(filename, 'r')
	    contents = RN_last_ver.read().splitlines()
	    contents_row = len(contents)
	    RN_last_ver.close()

	except IOError:
	    print(f'Can not find last version of Release Note {Leading_V_RN_File_Name}')

	return contents, contents_row

def Prepare_for_repo():
	if os.path.isdir(git_repo_dell):
		repo = git.Repo(git_repo_dell)
		# r = repo.remotes.origin
		print(repo)
	else:
		print('did not get repo')

	repo.git.checkout(f'{git_working_branch}')
	repo.git.pull('origin', f'{git_working_branch}')




# Test name 'R440-TESTRESULT.txt'
#
# Create this version of file
#
def Create_this_version(obj, filename):
	try:
	    file = open(f'R440-TESTRESULT_020704.txt', 'r')
	    file.truncate(0) #clear the file
	    file.close()

	except IOError:
	    file = open(f'R440-TESTRESULT_020704.txt', 'w+')
	    file.close()
	    # logging.info(f'file has been created')

	with open(f'R440-TESTRESULT_020704.txt', 'w+') as file:
		for line in obj.contents:
			file.write("%s\n" % line)
		file.close()

#
#
#
def find_keywords_n_edit_RN_info(obj, keywords, DebugMenuONOFF):
	index = 0
	i = 0
	while i < obj.row - 1 :
		try:
			index = obj.contents[i].index(keywords)
			if keywords == find_Version:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{platform_ver_major}.{platform_ver_minor}.{platform_ver_main}'
			elif keywords == find_System:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{platform_codeName} {platform_subCodeName_systemName}' #!
			elif keywords == find_Release_Date:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{date_month}/{date_day}/{date_year}'
			elif keywords == find_Release_By:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{user_first_name} {user_last_name}' #!
			elif keywords == find_SWB:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{schedule_softwareBundle}'
				if obj.contents[i + 1].index(find_SWB) != -1:
					del obj.contents[i + 1]
			elif keywords == find_AEP_Driver:
				del obj.contents[i]
			elif keywords == find_Important_Note:
				k = 1
				index_of_Important_Note = i
				j = 1
				while j < 10 :
					try:
						index_2 = obj.contents[i+1+j].index('When you encounter listed')
						break
					except ValueError:
						j += 1
				obj.contents[i+1+j] = '1. ' + obj.contents[i+1+j][(index_2):]
				del obj.contents[i+2 : i+2+j-1]

				k += 1
				l = 0
				while obj.contents[i+1+j+l].find(find_Known_Issues) == -1:
					if obj.contents[i+1+j+l] != '':						
						if obj.contents[i+1+j+l][0].isdigit():
							obj.contents[i+1+j+l] = str(k) +  obj.contents[i+1+j+l][1:]
							k += 1
							l += 1
						else:
							l += 1
					else:
						l += 1

			elif keywords == find_DebugMenu:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f'{DebugMenuONOFF}' + ' in this version.'	

			elif keywords == find_CHANGES:
				obj.contents.insert(i+2, f'1. [ESGB-{schedule_ESGB_number}] Change {schedule_block} BIOS version to 0{platform_ver_major}.0{platform_ver_minor}.0{platform_ver_main}')
				obj.contents.insert(i+3, f'2. Sync to 14G codebase to launch-1(Atlas) {platform_ver_major}.{platform_ver_minor}.{platform_ver_main}')
				obj.contents.insert(i+4, f'')
				obj.contents.insert(i+5, '*************************************************')
				obj.contents.insert(i+6, f'Sync to 14G codebase to launch-1(Atlas) {platform_ver_major}.{platform_ver_minor}.{platform_ver_main}')
				obj.contents.insert(i+7, '*************************************************')


			break

		except ValueError:
			i += 1
	return obj.contents



# def find_keywords_n_edit_RN_CodeChanges(obj_lastRN, obj_lastLV, keyword_CHANGES):
# 	i = 0
# 	while i < obj_lastLV
# 	row_of_keyword = 


def find_keywords_n_edit_BV(obj, keywords, Platform):
	index = 0
	i = 0
	while i < obj.row:
		if obj.contents[i].find(f'{Platform}') != -1:
			j = i
			while j < i + 50:
				try:				
					index = obj.contents[j].index(keywords)
					if keywords == find_Major_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_major}'
						break
					elif keywords == find_Minor_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_minor}'
						break
					elif keywords == find_Main_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{platform_ver_main}'
						break
					elif keywords == find_Build_Month:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{date_month}'
						# print(obj.contents[j])
						break
					elif keywords == find_Build_Day:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{date_day}'
						# print(obj.contents[j])
						break
					elif keywords == find_Build_Year:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f'{date_year}'
						# print(obj.contents[j])
						break
				except ValueError:
					j += 1
			break
		else :
			i += 1
		if i == obj.row :
			print(f"Didn't find {keywords} in {Last_ver_DellBiosVersion}")
	return obj.contents


def find_keywords_n_edit_DM(obj, keywords, Platform, DebugMenuONOFF):
	index = 0
	i = 0
	while i < obj.row:
		if obj.contents[i].find(f'{Platform}') != -1:
			j = i
			while j < i + 5:
				try:				
					index = obj.contents[j].index(keywords)
					if keywords == find_DebugMenu_PlatConf:
						if DebugMenuONOFF_input is 'Enabled':
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'TRUE'
							# print(obj.contents[j])
							break
						elif DebugMenuONOFF_input is 'Disabled':
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'FALSE'
							# print(obj.contents[j])
							break
				except ValueError:
					j += 1
			break
		else :
			i += 1
		if i == obj.row :
			print(f"Didn't find {keywords} in {Last_ver_PlatformConfig}")
	return obj.contents




[get_contents_RN, get_row_RN] = Read_last_version_File(Leading_V_RN_File_Name)
[get_contents_BV, get_row_BV] = Read_last_version_File(Last_ver_DellBiosVersion)
[get_contents_DM, get_row_DM] = Read_last_version_File(Last_ver_PlatformConfig)

# print(get_contents_BV)
# print(get_row_BV)
# exit(1)

#
# Get file contents in to obj
#
RN_obj = File_Data(get_contents_RN, get_row_RN)
Bios_Ver_obj = File_Data(get_contents_BV, get_row_BV)
Platform_Config_obj = File_Data(get_contents_DM, get_row_DM)


#
# (Const)
#
# [RN]
find_Version        = 'Version:      '
find_System         = 'System:       ' #+
find_Release_Date   = 'Release Date: '
find_Release_By     = 'Released By:  ' #+
find_SWB            = 'SWB#:         '
find_AEP_Driver     = 'AEP Driver'
find_Important_Note = 'Important Note:'
find_Known_Issues   = 'Known Issues:'
find_DebugMenu      = 'Debug Menu is '
find_CHANGES        = 'CHANGES:'

# [DellBiosVersion]
keyword_Platform = f' {platform_codeName} version'
find_Major_ver = '#define DELL_BIOS_MAJOR_VERSION       '
find_Minor_ver = '#define DELL_BIOS_MINOR_VERSION       '
find_Main_ver  = '#define DELL_BIOS_MAIN_VERSION        '
find_Build_Month = '#define DELL_BIOS_BUILD_MONTH         '
find_Build_Day = '#define DELL_BIOS_BUILD_DAY           '
find_Build_Year = '#define DELL_BIOS_BUILD_YEAR          '

find_DebugMenu_PlatConf = 'DEBUG_MENU_ENABLE                     = '
#
#
list_keywords = [find_Version, find_System, find_Release_Date, find_Release_By, find_SWB, find_AEP_Driver, find_Important_Note, find_Known_Issues, find_DebugMenu, find_CHANGES]
for each_keywords in list_keywords : 
	new_contents = find_keywords_n_edit_RN_info(RN_obj, each_keywords, DebugMenuONOFF_input)

# new_contents = find_keywords_n_edit_RN_CodeChanges(RN_obj, LVRN_obj, list_keywords)

list_keywords = [find_Major_ver, find_Minor_ver, find_Main_ver, find_Build_Month, find_Build_Day, find_Build_Year]
for each_keywords in list_keywords : 
	new_contents = find_keywords_n_edit_BV(Bios_Ver_obj, each_keywords, keyword_Platform)

list_keywords = find_DebugMenu_PlatConf
new_contents = find_keywords_n_edit_DM(Platform_Config_obj, list_keywords, keyword_Platform, DebugMenuONOFF_input)



#
# Create the file!
#

# Prepare_for_repo()

# for RN
Create_this_version(RN_obj, Leading_V_RN_File_Name)

# for DellBiosVersion.h
Create_this_version(Bios_Ver_obj, Last_ver_DellBiosVersion)

# for PlatformConfig_taurus.txt
# Create_this_version(Platform_Config_obj, Last_ver_PlatformConfig)
