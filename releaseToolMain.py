import os, sys
import git
import configparser
from datetime import date
import subprocess
import time
import pysvn
import win32com.client as win32
import inspect
# import const

#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  Initialize   === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #

config = configparser.ConfigParser() #-
config.read('readConfig_all.ini') #-
print("[O] Read configuartion from 'readConfig_all.ini'\n")
print("    Please check configuration info is correct.\n")

PLATFORM       = ['Taurus', 'Spitzer'] #INPUT

P = []
for i in PLATFORM:
	P.append(dict(config.items(i)))

version        = f"0{P[0]['ver_major']}.0{P[0]['ver_minor']}.0{P[0]['ver_main']}"
version_svn    = f"{P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}"
DUP_Checkbox   = True #INPUT
DebugMenu_Enable_checkbox = True #INPUT
if DebugMenu_Enable_checkbox == True : 
	DebugMenuONOFF_input = 'Enabled'   # X rev
	C = ''
	t_drive_folder = f"T:/Projects/14G.TDC.projects/{P[0]['codename']}/Release/{version}{C}/"
elif DebugMenu_Enable_checkbox == False :
	DebugMenuONOFF_input = 'Disabled'  # A-Can
	C = '-C'
	t_drive_folder = f"T:/Projects/14G.TDC.projects/{P[0]['codename']}/Release/{version}{C}/{P[0]['systemname']}/"


DUP_Available_string    = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'
DUP_text = ''
if DUP_Checkbox is True:
	DUP_text = DUP_Available_string
else:
	DUP_text = DUP_NOT_Avaiable_string


# if os.path.isdir(P[0]['repo_dell']):
# 	repo = git.Repo(P[0]['repo_dell'])
# 	# r = repo.remotes.origin
# 	print(f"[O] Find repo : {repo}")
# else:
# 	print('[X] Did not find repo')

#
# Files needed to be modified
#
Leading_V_RN_File_Name   = f"{P[0]['leading_v']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}.txt"
This_ver_RN              = f"{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}_test.txt"
Last_ver_DellBiosVersion = 'DellBiosVersion.h'
Last_ver_PlatformConfig  = 'PlatformConfig.txt'

#
# Const
#

# [RN]
find_Version        = 'Version:      '
find_System         = 'System:       '
find_Release_Date   = 'Release Date: '
find_Release_By     = 'Released By:  '
find_SWB            = 'SWB#:         '
find_AEP_Driver     = 'AEP Driver'
find_Important_Note = 'Important Note:'
find_Known_Issues   = 'Known Issues:'
find_DebugMenu      = 'Debug Menu is '
find_CHANGES        = 'CHANGES:'
find_ABP            = 'All Points Bulletin (APB)'

# [DellBiosVersion.h]
keyword_Platform    = f" {P[0]['codename']} version" # hashtag
find_Major_ver      = '#define DELL_BIOS_MAJOR_VERSION       '
find_Minor_ver      = '#define DELL_BIOS_MINOR_VERSION       '
find_Main_ver       = '#define DELL_BIOS_MAIN_VERSION        '
find_Build_Month    = '#define DELL_BIOS_BUILD_MONTH         '
find_Build_Day      = '#define DELL_BIOS_BUILD_DAY           '
find_Build_Year     = '#define DELL_BIOS_BUILD_YEAR          '

# [PlatformConfig.txt]
find_DebugMenu_PC   = 'DEFINE DEBUG_MENU_ENABLE                     = '

# Keywords for get/set code change
RN_list_keywords = [find_Version, find_System, find_Release_Date, find_Release_By, find_SWB, find_AEP_Driver, find_Important_Note, find_Known_Issues, find_DebugMenu, find_CHANGES, find_ABP]
BV_list_keywords = [find_Major_ver, find_Minor_ver, find_Main_ver, find_Build_Month, find_Build_Day, find_Build_Year]
DM_list_keywords = find_DebugMenu_PC



#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===   Functions   === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #

class File_Data():
	def __init__(self, contents, row):
		self.contents = contents
		self.row = row

class Functions:
	def Prepare_for_repo(self):
		if os.path.isdir(P[0]['repo_dell']):
			repo = git.Repo(P[0]['repo_dell'])
			# r = repo.remotes.origin
			print(f"[O] Find repo : {repo}")
		else:
			print('[X] Did not find repo')

		repo.git.checkout(f"{P[0]['working_branch']}")
		repo.git.pull('origin', f"{P[0]['working_branch']}")

	def Read_last_version_File(self, filename):
		contents = []
		contents_row = 0
		try:
			RN_last_ver = open(filename, "r")
			contents = RN_last_ver.read().splitlines()

			# RN_last_ver = open(filename, "rt", encoding="utf-16")		
			# contents = RN_last_ver.read()
			# contents = contents.rstrip("\n")
			# contents = contents.split("\r\n")

			contents_row = len(contents)
			print(contents_row)
			RN_last_ver.close()

		except IOError:
			print(f"Can not find last version of Release Note {filename}")

		return contents, contents_row

	def Create_this_version(self, obj, filename):
		# filename = f"{P[0]['codename']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}_Test.txt"
		try:
			print(f"Create_this_version : open {filename}")
			file = open(filename, 'r')
			file.truncate(0) #clear the file
			file.close()
			print("try")

		except IOError:
		    file = open(filename, 'w+')
		    file.truncate(0)
		    file.close()
		    print("except")
		    # logging.info(f"file has been created')

		with open(filename, 'w+') as file:
			for line in obj.contents:
				file.write("%s\n" % line)
			file.close()

	def read_existing_RN(self, filename):
		contents = []
		contents_row = 0
		try:
			RN_last_ver = open(filename, "r", encoding="ISO-8859-1")		
			contents = RN_last_ver.read().splitlines()
			contents_row = len(contents)
			print("contents_row : ")
			print(contents_row)
			RN_last_ver.close()

		except IOError:
			print(f"Can not find last version of Release Note {filename}")

		obj = File_Data(contents, contents_row)
		return obj

	#
	#
	#
	def find_keywords_n_edit_RN_info(self, obj, keywords, DebugMenuONOFF):
		index = 0
		i = 0
		while i < obj.row - 1 :
			try:
				index = obj.contents[i].index(keywords)
				if keywords == find_Version:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}"
				elif keywords == find_System:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{P[0]['codename']} {P[0]['subcodename_systemname']}"
				elif keywords == find_Release_Date:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{P[0]['month']}/{P[0]['day']}/{P[0]['year']}"
				elif keywords == find_Release_By:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{P[0]['name']}"
				elif keywords == find_SWB:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{P[0]['swb']}"
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
					obj.contents.insert(i+2, f"1. [ESGB-{P[0]['esgb_number']}] Change {P[0]['block']} BIOS version to 0{P[0]['ver_major']}.0{P[0]['ver_minor']}.0{P[0]['ver_main']}")
					obj.contents.insert(i+3, f"2. Sync to 14G codebase to launch-1(Atlas) {P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}")
					obj.contents.insert(i+4, f"")
					obj.contents.insert(i+5, '*************************************************')
					obj.contents.insert(i+6, f"Sync to 14G codebase to launch-1(Atlas) {P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}")
					obj.contents.insert(i+7, '*************************************************')

					print(f"\n----------------------------------------------------------------------")
					print(f"Release Note '{This_ver_RN}' has been created. Please check it. \n")

				elif keywords == find_ABP:
					obj.contents[i].replace("#22", "#02") #*

				break

			except ValueError:
				i += 1

		return obj.contents


	def find_keywords_n_edit_BV(self, obj, keywords, Platform):
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
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_major']}"
							print('    ' + obj.contents[j])
							break
						elif keywords == find_Minor_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_minor']}"
							print('    ' + obj.contents[j])
							break
						elif keywords == find_Main_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_main']}"
							print('    ' + obj.contents[j])
							print('')
							break
						elif keywords == find_Build_Month:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['month']}"
							print('    ' + obj.contents[j])
							break
						elif keywords == find_Build_Day:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['day']}"
							print('    ' + obj.contents[j])
							break
						elif keywords == find_Build_Year:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['year'][-2:]}"
							print('    ' + obj.contents[j])
							break
					except ValueError:
						j += 1
				break
			else :
				i += 1
			if i == obj.row :
				print(f"[X] Didn't find {keywords} in {Last_ver_DellBiosVersion}")
		return obj.contents


	def find_keywords_n_edit_DM(self, obj, keywords, Platform, DebugMenuONOFF):
		index = 0
		i = 0
		while i < obj.row:
			if obj.contents[i].find(f'{Platform}') != -1:
				print(f"Found hashtag at #{i}")
				j = i
				while j < i + 5:
					try:				
						index = obj.contents[j].index(keywords)
						if keywords is find_DebugMenu_PC:
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
				print(f"[X] Didn't find {keywords} in {Last_ver_PlatformConfig}")
		return obj.contents

	def create_RN(self, file, keywords):
		[get_contents, get_row] = self.Read_last_version_File(file)
		obj = File_Data(get_contents, get_row)

		for each_keywords in keywords :
			new_contents = self.find_keywords_n_edit_RN_info(obj, each_keywords, DebugMenuONOFF_input)

		outputfile = This_ver_RN
		self.Create_this_version(obj, outputfile)

		return obj


	def edit_BV(self, keywords):
		path_BV   = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/Include/" + Last_ver_DellBiosVersion

		if os.path.isfile(path_BV):
			print(f"\n[O] Find the file : {path_BV}")
		else:
			print(f"[X] Did not find : {path_BV}")

		[get_contents, get_row] = self.Read_last_version_File(path_BV)
		obj = File_Data(get_contents, get_row)

		# print(obj.row)

		for each_keywords in keywords :
			new_contents = self.find_keywords_n_edit_BV(obj, each_keywords, keyword_Platform)

		self.Create_this_version(obj, path_BV)

	def edit_PC(self, keywords):
		path_PC   = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/" + Last_ver_PlatformConfig

		if os.path.isfile(path_PC):
			print(f"\n[O] Find the file : {path_PC}")
		else:
			print(f"[X] Did not find : {path_PC}")

		[get_contents, get_row] = self.Read_last_version_File(path_PC)
		obj = File_Data(get_contents, get_row)

		new_contents = self.find_keywords_n_edit_DM(obj, keywords, keyword_Platform, DebugMenuONOFF_input)

		self.Create_this_version(obj, path_PC)

	def scan_CPI(self):
		index = 0
		list_commits = list(repo.iter_commits(P[0]['working_branch'], max_count = 70))
		for commit in list_commits:
			if commit.message.find("version change") != -1:
				if commit.message.find(f"{P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}") == -1:
					# print(commit.message)
					index = list_commits.index(commit)
					# print(index)
					break
				# if commit.find("")
		list_commits = list(repo.iter_commits(P[0]['working_branch'], max_count = index))

		for commit in list_commits:
			for file in commit.stats.files:
				if file.find("DellPkgs/DellPlatformPkgs/DellAtlasPkg") != -1:
					if file.find("DellPkgs/DellPlatformPkgs/DellAtlasPkg/Include/DellBiosVersion.h") == -1:
						print(f"\n---------------------------------------------")
						print(f"Got CPI : " + f"{file}")
						print(f"    Path : " + f"{file}")
						print(f"    Author : {commit.author}")
						print(f"    Date and time : {commit.authored_datetime}")
						print(f"    SHA number : {commit}")
						print(f"---------------------------------------------")
						# print(inspect.getmembers(commit))
						print(f"    Please check whether it's neccessary CPI or not.\n")
						print(f"    If yes, please get the CPI to your platform MAUALLY.\n")





# list_commits_this_ver


	#
	# Build & Release & upload SVN & Rename EFI
	#


	def build_n_release(self):
		# folder_path = 'C:/BEA/edk2/gemini_foxconn/DellPkgs/DellPlatformPkgs/DellTaurusPkg/'
		# version     = f"0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}"
		folder_path = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/"
		# print(folder_path + 'Makea_Arev_Release.bat')
		

		# try:
			# if DebugMenu_Enable_checkbox == True :    # X rev
			# 	bat_file = 'Makea_Release.bat'
			# elif DebugMenu_Enable_checkbox == False : # A-Can
			# 	bat_file = 'Makea_Arev_Release.bat'
		# 	subprocess.check_call(f"{bat_file}", shell=True, cwd=f'{folder_path}')
		# 	print('ok')
		# except subprocess.CalledProcessError:
		# 	print('error')
		# 	exit(0)

		for p in P: # !Cautious : Spitzer only!?
			try:
				if DebugMenu_Enable_checkbox == True :    # X rev
					rel_cmd = 'release.bat' + f" {p['systemname']}" + f" {version}"
				elif DebugMenu_Enable_checkbox == False : # A-Can
					rel_cmd = 'release.bat' + f" {p['systemname']}" + f" {version}" + ' A'
				print(f"Run cmd : {rel_cmd}")
				subprocess.check_call(f"{rel_cmd}", shell=True, cwd=f'{folder_path}')
				print(f"[OK] release.bat for {p['systemname']}")
			except subprocess.CalledProcessError:
				print('error')

	def upload_to_svn(self):
		client = pysvn.Client()
		file_name = f"{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}.efi"
		file_path = t_drive_folder + file_name

		# ODM SVN (Foxconn)
		svn_url = f"https://f2dsvn.{P[0]['odm']}.com/svn/14G_misc/{P[0]['codename']}/Release/BIOS/MLK/{version_svn}/{file_name}"
		print(f"Get SVN path : {svn_url}")

		client.import_(path = file_path,
		               url = f'{svn_url}',
		               log_message = 'Hi Webb, EFI file was uploaded. Please help perform POT. Thanks!')
		print("[OK] Upload to svn. Please check it.")


	def rename_EFI_withSWB(self):
		for p in P:
			os.chdir(t_drive_folder)
			new_name  = f"BIOS_{p['swb']}_EFI_{p['ver_major']}.{p['ver_minor']}.{p['ver_main']}.efi"
			for file in os.listdir(t_drive_folder):
			    if file.endswith(".efi"):
			    	print(f"Found an EFI file : '{file}'")
			    	os.rename(file, new_name)
			    	print(f"EFI has been renamed as '{new_name}'")

	#
	#
	# Create mail
	#
	#

	def read_RN(self, file):
		[get_contents, get_row] = self.Read_last_version_File(file)
		obj = File_Data(get_contents, get_row)

		return obj


	def create_release_mail(self, obj):
		for p in P :
			i = P.index(p)
			version = p['ver_major'] + '.' + p['ver_minor'] + '.' + p['ver_main']

			Title = f"Release : BIOS, Dell Server BIOS {p['generation']}, {p['codename']} {p['subcodename']}, {p['revision']} {version} ({p['block']}), SWB#{p['swb']}" 
			Content = f"Hi all,\n\
			\n\
			{p['generation']} {p['codename']} {p['subcodename_systemname']} BIOS version {version} {p['revision']} ({p['block']} block) is available on Agile.\n\
			SWB# : {p['swb']}\n\
			{DUP_text}\n\
			\n\
			\n" 
			# print(Content)
			# Add Release note
			if bool(obj) is not False:
				if obj[i] is not None:
					for line in obj[i].contents:
						Content += f"{line}\n"
				# print(Content)

			olook = win32.Dispatch("outlook.application")
			mail = olook.CreateItem(0)
			mail.To = p['receivers']
			mail.CC = p['cc']
			mail.Subject = Title
			mail.Body = Content
			mail.Display(True)



	#
	# Create rel branch
	#
	def commit_block_branch(self):
		path_BV = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/Include/" + Last_ver_DellBiosVersion
		path_PC = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/"         + Last_ver_PlatformConfig
		version = f"0{P[0]['ver_major']}.0{P[0]['ver_minor']}.0{P[0]['ver_main']}"

		repo.git.checkout(f"{P[0]['working_branch']}")
		repo.git.pull('origin', f"{P[0]['working_branch']}")

		# Do Not commit Recovery .rom
		# if repo.git.status().find('16MBRecoveryBios.rom') != 0 :
		# 	repo.git.reset('DellPkgs/DellPlatformPkgs/DellTaurusPkg/BiosRecovery/Taurus_16MBRecoveryBios.rom')

		for item in repo.index.diff(None):
			# print(item.a_path)
			if  item.a_path in path_BV:
				repo.git.add(f"{path_BV}")
				print(f"add {path_BV} to commit")

			if  item.a_path in path_PC:
				repo.git.add(f"{path_PC}")
				print(f"add {path_PC} to commit")

		repo.git.commit('-m', f"[ESGB-{P[0]['esgb_number']}][{P[0]['codename']}] Change {P[0]['block']} BIOS version to {version}.")
		repo.git.push('origin', f"{P[0]['working_branch']}")


	def create_rel_branch(self):
		if repo.active_branch.name != P[0]['working_branch']:
			repo.git.checkout(f"{P[0]['working_branch']}")
			
		Codename_lower = P[0]['codename'].lower()
		New_rel_branch = f"rel/{Codename_lower}/{Codename_lower}_{P[0]['ver_major']}_{P[0]['ver_minor']}_{P[0]['ver_main']}"

		repo.git.pull('origin', f"{P[0]['working_branch']}")
		print(f"To create new rel branch {New_rel_branch}")
		try:
			b = repo.create_head(New_rel_branch)
		except git.exc.GitCommandError:
			print(f"branch {New_rel_branch} already exists")

		b.checkout()
		repo.git.push('origin', f"{P[0]['working_branch']}")
		repo.git.push('origin', f"{New_rel_branch}")

	 
	def create_rel_tag(self):
		# print(repo.active_branch.name)
		New_rel_tag = f"{P[0]['codename']}/{P[0]['ver_major']}_{P[0]['ver_minor']}_{P[0]['ver_main']}"

		try:
			print(f"To create new tag {New_rel_tag}")
			repo.create_tag(New_rel_tag)
		except git.exc.GitCommandError:
			print(f"tag {New_rel_tag} already exists")

		repo.git.push('origin', f"{New_rel_tag}")


	def update_INIdata(self):
		with open('readConfig_taurus.ini', 'w') as configfile:
			config.write(configfile)



	#  === === === === ===  == == == ==  === === === === ===  #
	#  === === === === ===  == == == ==  === === === === ===  #
	#  === === === === ===  == == == ==  === === === === ===  #
	#  === === === === ===    Execute    === === === === ===  #
	#  === === === === ===  == == == ==  === === === === ===  #
	#  === === === === ===  == == == ==  === === === === ===  #
	#  === === === === ===  == == == ==  === === === === ===  #

	if os.path.isdir(P[0]['repo_dell']):
		repo = git.Repo(P[0]['repo_dell'])
		# r = repo.remotes.origin
		print(f"[O] Find repo : {repo}")
	else:
		print('[X] Did not find repo')


	def func1(self):
		print("1 working")

	def func2(self):
		print("2 working")

	def func3(self):
		print("3 working")


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#
# Step 1 : Fetch RN, git repo, and create code change
#

f = Functions()



if os.path.isdir(P[0]['repo_dell']):
	repo = git.Repo(P[0]['repo_dell'])
	# r = repo.remotes.origin
	print(f"[O] Find repo : {repo}")
	print(f"Working on branch {P[0]['working_branch']}")
else:
	print('[X] Did not find repo')
f.Prepare_for_repo()
# RN_obj = f.create_RN(Leading_V_RN_File_Name, RN_list_keywords)
# f.edit_BV(BV_list_keywords)
# f.edit_PC(DM_list_keywords)
# time.sleep(10)


read_RN_path_T = f"C:/BEA/releaseTool/{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}_read.txt"
read_RN_path_S = f"C:/BEA/releaseTool/{P[1]['systemname']}-0{P[1]['ver_major']}0{P[1]['ver_minor']}0{P[1]['ver_main']}_read.txt"
# print(read_RN_path_T)
# print(read_RN_path_S)
RN_obj_T = f.read_RN(read_RN_path_T) # Test for Taurus  RN
RN_obj_S = f.read_RN(read_RN_path_S) # Test for Spitzer RN
# RN_obj_T = f.read_existing_RN(read_RN_path_T)
# RN_obj_S = f.read_existing_RN(read_RN_path_S)
RN_Read = [RN_obj_T, RN_obj_S]

# f.scan_CPI()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#
# Step 2 : Fetch RN, git repo, and create code change
#

# f.build_n_release()
# f.upload_to_svn()
# f.rename_EFI_withSWB()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#
# Step 3 : Release mail, create branch & tag
#


# f.create_release_mail(RN_Read)

# f.commit_block_branch()
# f.create_rel_branch()
# f.create_rel_tag()

# update_INIdata() # from GUI INPUT

# sys.exit(1)
