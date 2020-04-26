import os
import git
import configparser
from datetime import date
import subprocess

config = configparser.ConfigParser() #-
config.read('readConfig_all.ini') #-

DebugMenu_Enable_checkbox = False
DUP_Checkbox = True #INPUT
# DUP_Checkbox = False



Mail_Title = ''
Mail_Content = ''

if DebugMenu_Enable_checkbox == True :
	DebugMenuONOFF_input = 'Enabled' # X rev
elif DebugMenu_Enable_checkbox == False :
	DebugMenuONOFF_input = 'Disabled' # A-Can


PLATFORM = 'Taurus' #INPUT
v = dict(config.items(f"{PLATFORM}"))

version = v['ver_major'] + '.' + v['ver_minor'] + '.' + v['ver_main']
Codename_lower = v['codename'].lower()

if os.path.isdir(v['repo_dell']):
	repo = git.Repo(v['repo_dell'])
	# r = repo.remotes.origin
	print(repo)
else:
	print('did not get repo')


New_rel_branch          = f"rel/{Codename_lower}/{Codename_lower}_{v['ver_major']}_{v['ver_minor']}_{v['ver_main']}"
New_rel_tag             = f"{v['codename']}/{v['ver_major']}_{v['ver_minor']}_{v['ver_main']}"
DUP_Available_string    = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'
DUP_text = ''
if DUP_Checkbox is True: #INPUT
	DUP_text = DUP_Available_string
else:
	DUP_text = DUP_NOT_Avaiable_string


#
# Files needed to be modified
#
Leading_V_RN_File_Name   = f"{v['leading_v']}-0{v['ver_major']}0{v['ver_minor']}0{v['ver_main']}.txt"
This_ver_RN              = f"{v['systemname']}-0{v['ver_major']}0{v['ver_minor']}0{v['ver_main']}_test.txt"
Last_ver_DellBiosVersion = 'DellBiosVersion.h'
Last_ver_PlatformConfig  = 'PlatformConfig.txt'



#
# Const
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
keyword_Platform = f" {v['codename']} version"
find_Major_ver = '#define DELL_BIOS_MAJOR_VERSION       '
find_Minor_ver = '#define DELL_BIOS_MINOR_VERSION       '
find_Main_ver  = '#define DELL_BIOS_MAIN_VERSION        '
find_Build_Month = '#define DELL_BIOS_BUILD_MONTH         '
find_Build_Day = '#define DELL_BIOS_BUILD_DAY           '
find_Build_Year = '#define DELL_BIOS_BUILD_YEAR          '

find_DebugMenu_PlatConf = 'DEBUG_MENU_ENABLE                     = '


#
# Keywords for get/set code change
#

RN_list_keywords = [find_Version, find_System, find_Release_Date, find_Release_By, find_SWB, find_AEP_Driver, find_Important_Note, find_Known_Issues, find_DebugMenu, find_CHANGES]
BV_list_keywords = [find_Major_ver, find_Minor_ver, find_Main_ver, find_Build_Month, find_Build_Day, find_Build_Year]
DM_list_keywords = find_DebugMenu_PlatConf





#  === === === === ===   Functions   === === === === ===  #

class File_Data():
	def __init__(self, contents, row):
		self.contents = contents
		self.row = row


def Prepare_for_repo():
	if os.path.isdir(v['repo_dell']):
		repo = git.Repo(v['repo_dell'])
		# r = repo.remotes.origin
		print(repo)
	else:
		print('did not get repo')

	repo.git.checkout(f"{git_working_branch}")
	repo.git.pull('origin', f"{git_working_branch}")

def Read_last_version_File(filename):
	contents_row = 0
	try:
		RN_last_ver = open(filename, 'r')
		contents = RN_last_ver.read().splitlines()
		contents_row = len(contents)
		RN_last_ver.close()

	except IOError:
		print(f"Can not find last version of Release Note {filename}")

	return contents, contents_row

def Create_this_version(obj, filename):
	# filename = f"{v['codename']}-0{v['ver_major']}0{v['ver_minor']}0{v['ver_main']}_Test.txt"
	try:
	    file = open(filename, 'r')
	    file.truncate(0) #clear the file
	    file.close()

	except IOError:
	    file = open(filename, 'w+')
	    file.close()
	    # logging.info(f"file has been created')

	with open(filename, 'w+') as file:
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
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{v['ver_major']}.{v['ver_minor']}.{v['ver_main']}"
			elif keywords == find_System:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{v['codename']} {v['subcodename_systemname']}" #!
			elif keywords == find_Release_Date:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{v['month']}/{v['day']}/{v['year']}"
			elif keywords == find_Release_By:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{v['name']}" #!
			elif keywords == find_SWB:
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{v['softwarebundle']}"
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
				obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{DebugMenuONOFF}" + ' in this version.'	

			elif keywords == find_CHANGES:
				obj.contents.insert(i+2, f"1. [ESGB-{v['esgb_number']}] Change {v['block']} BIOS version to 0{v['ver_major']}.0{v['ver_minor']}.0{v['ver_main']}")
				obj.contents.insert(i+3, f"2. Sync to 14G codebase to launch-1(Atlas) {v['ver_major']}.{v['ver_minor']}.{v['ver_main']}")
				obj.contents.insert(i+4, f"")
				obj.contents.insert(i+5, '*************************************************')
				obj.contents.insert(i+6, f"Sync to 14G codebase to launch-1(Atlas) {v['ver_major']}.{v['ver_minor']}.{v['ver_main']}")
				obj.contents.insert(i+7, '*************************************************')

				print(f"\n----------------------------------------------------------------------")
				print(f"Release Note '{This_ver_RN}' has been created. Please check it. \n")

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
			while j < i + 50:
				try:
					index = obj.contents[j].index(keywords)
					if keywords == find_Major_ver:
						print(f"\n----------------------------------------------------------------------")
						print(f"Code change in '{Last_ver_DellBiosVersion}'' : \n")
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['ver_major']}"
						print('    ' + obj.contents[j])
						break
					elif keywords == find_Minor_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['ver_minor']}"
						print('    ' + obj.contents[j])
						break
					elif keywords == find_Main_ver:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['ver_main']}"
						print('    ' + obj.contents[j])
						print('')
						break
					elif keywords == find_Build_Month:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['month']}"
						print('    ' + obj.contents[j])
						break
					elif keywords == find_Build_Day:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['day']}"
						print('    ' + obj.contents[j])
						break
					elif keywords == find_Build_Year:
						obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{v['year'][-2:]}"
						print('    ' + obj.contents[j])
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
						print(f"\n----------------------------------------------------------------------")
						print(f"Code change in '{Last_ver_PlatformConfig}'' : \n")
						if DebugMenuONOFF_input is 'Enabled':
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'TRUE'
							print('    ' + obj.contents[j])
							break
						elif DebugMenuONOFF_input is 'Disabled':
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'FALSE'
							print('    ' + obj.contents[j])
							break
				except ValueError:
					j += 1
			break
		else :
			i += 1
		if i == obj.row :
			print(f"Didn't find {keywords} in {Last_ver_PlatformConfig}")
	return obj.contents



# file path C:\BEA\14gmlk_junfy21\DellPkgs\DellPlatformPkgs\DellTaurusPkg
# path_LVRN = 
path_BV   = v['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{v['codename']}Pkg/Include/" + Last_ver_DellBiosVersion
path_PC   = v['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{v['codename']}Pkg/" + Last_ver_PlatformConfig

if os.path.isfile(path_BV):
	print(f"get {path_BV}")
else:
	print(f"did not get {path_BV}")

if os.path.isfile(path_PC):
	print(f"get {path_PC}")
else:
	print(f"did not get {path_PC}")








def create_RN(file, keywords):
	[get_contents, get_row] = Read_last_version_File(file)
	obj = File_Data(get_contents, get_row)

	for each_keywords in keywords :
		new_contents = find_keywords_n_edit_RN_info(obj, each_keywords, DebugMenuONOFF_input)

	outputfile = This_ver_RN
	Create_this_version(obj, outputfile)


def create_BV(file, keywords):
	[get_contents, get_row] = Read_last_version_File(file)
	obj = File_Data(get_contents, get_row)

	for each_keywords in keywords :
		new_contents = find_keywords_n_edit_BV(obj, each_keywords, keyword_Platform)

	Create_this_version(obj, file)

def create_DM(file, keywords):
	[get_contents, get_row] = Read_last_version_File(file)
	obj = File_Data(get_contents, get_row)

	new_contents = find_keywords_n_edit_DM(obj, keywords, keyword_Platform, DebugMenuONOFF_input)

	Create_this_version(obj, file)









#
# Build & Release & upload SVN & Rename EFI
#


def build_n_release():
	folder_path = 'C:/BEA/edk2/gemini_foxconn/DellPkgs/DellPlatformPkgs/DellTaurusPkg/'
	folder_path = v['repo_dell']

	print(folder_path + 'Makea_Arev_Release.bat')

	try:
		p1 = subprocess.check_call(['Makea_Arev_Release.bat'], shell=True, cwd=f'{folder_path}')
		print('ok')
	except subprocess.CalledProcessError:
		print('error')
		exit(0)


	try:
		p2 = subprocess.check_call(['release.bat', 'R440',  '020799', 'A'], shell=True, cwd=f'{folder_path}')
		print('R440 ok')
	except subprocess.CalledProcessError:
		print('error')



	try:
		p2 = subprocess.check_call(['release.bat', 'R740xd2',  '020799', 'A'], shell=True, cwd=f'{folder_path}')
		print('R740xd2 ok')
	except subprocess.CalledProcessError:
		print('error')


















#
# Create mail
#

def create_release_mail(Title, Content):
	Title = f"Release : BIOS, Dell Server BIOS {v['generation']}, {v['codename']} {v['subcodename']}, {v['revision']} {version} ({v['block']}), SWB#{v['softwarebundle']}" 
	print(Content)
	print('\n')
	print('\n')

	Content = f"Hi all,\n\
	\n\
	{v['generation']} {v['codename']} {v['subcodename_systemname']} BIOS version {version} {v['revision']} ({v['block']} block) is available on Agile.\n\
	SWB# : {v['softwarebundle']}\n\
	{DUP_text}\n\
	\n\
	Please check internal release note for the detail of BIOS changes.\n\
	Thanks.\n\
	\n\
	Best Regards,\n\
	{v['name']} "  #Convert first letter to Capital 
	print(Content)
	return Title, Content

# Release : BIOS, Dell Server BIOS Polaris, Taurus (Ice, Rosetta, Genesis) , X-Rev , 2.7.2 (JunFY21), SWB#MHV07 (X02-00)


#
# Generate a copy .txt file
#
def write_into_txt(Title, Content):
    try:
        file = open(f"Date_Mail_{v['codename']}_{version}.txt", 'a')
        file.truncate(0) #clear the file
        file.close()

    except IOError:
        file = open(f"Date_Mail_{v['codename']}_{version}.txt", 'w+')
        file.close()

    # Put the result from the list to the txt file
    with open(f"Date_Mail_{v['codename']}_{version}.txt", 'a') as mail_copy:
        mail_copy.writelines(f"To : {v['receivers']}")
        mail_copy.write('\n')
        mail_copy.writelines(f"Cc : {v['cc']}")
        mail_copy.write('\n')
        mail_copy.writelines(f"Title : {Title}")
        mail_copy.write('\n')
        mail_copy.writelines(Content)
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.write('----------------------------------------------------')
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.close()


#
# Python package to send
#


#
# Create rel branch
#
# [ESGB-2148][Taurus] Change JunFY21 BIOS version to 02.07.04.

def commit_block_branch():
	repo.git.checkout(f"{v['working_branch']}")
	repo.git.pull('origin', f"{v['working_branch']}")

	# Do Not commit Recovery .rom
	if repo.git.status().find('16MBRecoveryBios.rom') != 0 :
		repo.git.reset('DellPkgs/DellPlatformPkgs/DellTaurusPkg/BiosRecovery/Taurus_16MBRecoveryBios.rom')

	# repo.git.commit('-m', f"[ESGB-{v['esgb_number']}][{v['codename']}] Change {v['block']} BIOS version to 0{v['ver_major']}.0{v['ver_minor']}.0{v['ver_main']}.")


	# repo.git.push('origin', f"{git_working_branch}')

def create_rel_branch():
	repo.git.pull('origin', f"{v['working_branch']}")
	print(f"To create new rel branch {New_rel_branch}")
	try:
		b = repo.create_head(New_rel_branch)
	except git.exc.GitCommandError:
		print(f"branch {New_rel_branch} already exists")

	b.checkout()
	repo.git.push('origin', f"{New_rel_branch}")

 
def create_rel_tag():
	try:
		print(f"To create new tag {New_rel_tag}")
		repo.create_tag(New_rel_tag)
	except git.exc.GitCommandError:
		print(f"tag {New_rel_tag} already exists")

	repo.git.push('origin', f"{New_rel_tag}")


def update_INIdata():
	with open('readConfig_taurus.ini', 'w') as configfile:
		config.write(configfile)







#  == == == == ==  Execute  == == == == ==  #




#
# Create the file
#

# Prepare_for_repo()

# for RN
create_RN(Leading_V_RN_File_Name, RN_list_keywords)

# for DellBiosVersion.h
create_BV(path_BV, BV_list_keywords)

# for PlatformConfig_taurus.txt
create_DM(path_PC, DM_list_keywords)












# Mail_Title, Mail_Content = create_release_mail(Mail_Title, Mail_Content)
# write_into_txt(Mail_Title, Mail_Content)

# update_INIdata()
# commit_block_branch()
# create_rel_branch()
# create_rel_tag()

