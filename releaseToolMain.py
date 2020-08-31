from datetime import date
import time
import os, sys, shutil, subprocess
import win32com.client as win32
import git, pysvn
import configparser
from colorama import init, Fore, Back, Style
init()
# import const

#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  Initialize   === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #

config = configparser.ConfigParser()
config_file = 'readConfig_Sep.ini' # _INPUT_
config.read(config_file)           # _INPUT_
PLATFORM = ['Taurus', 'Spitzer']   # _INPUT_
DUP_Checkbox   = False             # _INPUT_
num_platform = len(PLATFORM)
print(Fore.GREEN + f"[O] Read configuartion from '{config_file}'. Please double check configuration is correct." + Style.RESET_ALL)

P = []
for i in PLATFORM:
	P.append(dict(config.items(i)))

version        = f"0{P[0]['ver_major']}.0{P[0]['ver_minor']}.0{P[0]['ver_main']}"
version_cmd    = f"0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}"
version_svn    = f"{P[0]['ver_major']}.{P[0]['ver_minor']}.{P[0]['ver_main']}"
Codename_lower = P[0]['codename'].lower()
New_rel_branch = f"rel/{Codename_lower}/{Codename_lower}_{P[0]['ver_major']}_{P[0]['ver_minor']}_{P[0]['ver_main']}"
New_rel_tag    = f"{P[0]['codename']}/{P[0]['ver_major']}_{P[0]['ver_minor']}_{P[0]['ver_main']}"
repo           = None
DebugMenu_Enable_checkbox = None
t_drive_folder = [''] * num_platform
read_RN        = [''] * num_platform

if P[0]['revision'] == 'X rev':
	print(Fore.YELLOW + '[!] This is X rev' + Style.RESET_ALL)
	DebugMenu_Enable_checkbox = True 

elif P[0]['revision'] == 'A-can':
	print(Fore.YELLOW + '[!] This is A-can' + Style.RESET_ALL)
	DebugMenu_Enable_checkbox = False 

if DebugMenu_Enable_checkbox == True : # X rev
	DebugMenuONOFF = 'Enabled'
	C = ''
	for i in range(num_platform):
		t_drive_folder[i] = f"T:/Projects/14G.TDC.projects/{P[i]['codename']}/Release/{version}{C}/"

elif DebugMenu_Enable_checkbox == False : # A-Can
	DebugMenuONOFF = 'Disabled'
	C = '-C'
	for i in range(num_platform):
		t_drive_folder[i] = f"T:/Projects/14G.TDC.projects/{P[i]['codename']}/Release/{version}{C}/{P[i]['systemname']}/"

for i in range(num_platform):
	read_RN[i] = f"{P[i]['systemname']}-0{P[i]['ver_major']}0{P[i]['ver_minor']}0{P[i]['ver_main']}.txt"


DUP_Available_string    = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'
DUP_text = ''
if DUP_Checkbox is True:
	DUP_text = DUP_Available_string
else:
	DUP_text = DUP_NOT_Avaiable_string


#
# Files needed to be modified
#
Leading_V_RN_File_Name   = f"{P[0]['leading_v']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}.txt"
This_ver_RN              = f"{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}_test.txt"
RN_file_name   = f"{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}.txt"
RN_file_name_2 = f"{P[1]['systemname']}-0{P[1]['ver_major']}0{P[1]['ver_minor']}0{P[1]['ver_main']}.txt"
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
#  === === === === ===   Functions   === === === === ===  #
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
			print(Fore.GREEN + f"[O] Find repo : {repo}" + Style.RESET_ALL)
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
			# print(f"[O] Read file, total row : '{contents_row}'")
			RN_last_ver.close()

		except IOError:
			print(f"Can not find last version of Release Note {filename}")

		return contents, contents_row

	def Create_this_version(self, obj, filename):
		# filename = f"{P[0]['codename']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}_Test.txt"
		try:
			print(Fore.GREEN + f"\n[O] Successfully Create_this_version : {filename}" + Style.RESET_ALL)
			file = open(filename, 'r')
			file.truncate(0) #clear the file
			file.close()

		except IOError:
		    file = open(filename, 'w+')
		    file.truncate(0)
		    file.close()
		    # logging.info(f"file has been created')

		with open(filename, 'w+') as file:
			for line in obj.contents:
				file.write("%s\n" % line)
			file.close()

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
							print('----' + f"Code change in '{Last_ver_DellBiosVersion}' : \n")
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_major']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Minor_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_minor']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Main_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['ver_main']}"
							print('        ' + obj.contents[j])
							print('')
							break
						elif keywords == find_Build_Month:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['month']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Build_Day:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['day']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Build_Year:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{P[0]['year'][-2:]}"
							print('        ' + obj.contents[j])
							break
					except ValueError:
						j += 1
				break
			else :
				i += 1
			if i == obj.row :
				print(Fore.RED + f"[X] Didn't find {keywords} in {Last_ver_DellBiosVersion}" + Style.RESET_ALL)
		return obj.contents


	def find_keywords_n_edit_DM(self, obj, keywords, Platform, DebugMenuONOFF):
		index = 0
		i = 0
		while i < obj.row:
			if obj.contents[i].find(f'{Platform}') != -1:
				# print(f"Found hashtag at #{i}")
				j = i
				while j < i + 5:
					try:				
						index = obj.contents[j].index(keywords)
						if keywords is find_DebugMenu_PC:
							print('----' + f"Code change in '{Last_ver_PlatformConfig}'' : \n")
							if DebugMenuONOFF is 'Enabled':
								obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'TRUE'
								print('        ' + obj.contents[j])
								break
							elif DebugMenuONOFF is 'Disabled':
								obj.contents[j] = obj.contents[j][:(index + len(keywords))] + 'FALSE'
								print('        ' + obj.contents[j])
								break
					except ValueError:
						j += 1
				break
			else :
				i += 1
			if i == obj.row :
				print(Fore.RED + f"[X] Didn't find {keywords} in {Last_ver_PlatformConfig}" + Style.RESET_ALL)
		return obj.contents

	# def create_RN(self, file, keywords):
	# 	[get_contents, get_row] = self.Read_last_version_File(file)
	# 	obj = File_Data(get_contents, get_row)

	# 	for each_keywords in keywords :
	# 		new_contents = self.find_keywords_n_edit_RN_info(obj, each_keywords, DebugMenuONOFF)

	# 	outputfile = This_ver_RN
	# 	self.Create_this_version(obj, outputfile)

	# 	return obj


	def edit_BV(self, keywords):
		print(Back.CYAN + f"\n")
		print(f"----------------------------")
		print(f"-- Edit DellBiosVersion.h --")
		print(f"----------------------------")
		print(Style.RESET_ALL)
		path_BV   = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/Include/" + Last_ver_DellBiosVersion

		if os.path.isfile(path_BV):
			print(f"[O] Find the file : {path_BV}")
		else:
			print(Fore.RED + f"[X] Did not find : {path_BV}" + Style.RESET_ALL)

		[get_contents, get_row] = self.Read_last_version_File(path_BV)
		obj = File_Data(get_contents, get_row)
		# print(obj.row)

		for each_keywords in keywords :
			new_contents = self.find_keywords_n_edit_BV(obj, each_keywords, keyword_Platform)

		self.Create_this_version(obj, path_BV)

	def edit_PC(self, keywords):
		print(Back.CYAN + f"\n")
		print(f"-----------------------------")
		print(f"-- Edit PlatformConfig.txt --")
		print(f"-----------------------------")
		print(Style.RESET_ALL)
		path_PC   = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/" + Last_ver_PlatformConfig

		if os.path.isfile(path_PC):
			print(f"[O] Find the file : {path_PC}")
		else:
			print(Fore.RED + f"[X] Did not find : {path_PC}" + Style.RESET_ALL)

		[get_contents, get_row] = self.Read_last_version_File(path_PC)
		obj = File_Data(get_contents, get_row)

		new_contents = self.find_keywords_n_edit_DM(obj, keywords, keyword_Platform, DebugMenuONOFF)

		self.Create_this_version(obj, path_PC)

	def scan_CPI(self):
		print(Back.CYAN)
		print(f"--------------")
		print(f"-- Scan CPI --")
		print(f"--------------")
		print(Style.RESET_ALL)
		index = 0
		cpi_num = 0
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
						print(f"    Please check whether it's neccessary CPI or not.\n")
						print(f"    If yes, please get the CPI to your platform MAUALLY.\n")
						cpi_num += 1

		if cpi_num is 0:
			print("[O] Found no CPI.\n")
		else :
			print(f"[O] Found {cpi_num} CPI.\n")


		#
		# Check status before build code
		#
		print(Back.YELLOW)
		print(f"------------------------")
		print(f"-- Show changed files --")
		print(f"------------------------")
		print('\n' + Style.RESET_ALL)
		print(Fore.YELLOW + f'[!] Check these before you go to "Step 2 : Bulid EFI to POT"')
		print(Style.RESET_ALL)
		for item in repo.index.diff(None):
			print(item)
			print('\n')
		print(f"\n")


	#
	# Build & Release & upload SVN & Rename EFI
	#
	def build_n_release(self):
		folder_path = P[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[0]['codename']}Pkg/"
		# print(folder_path + 'Makea_Arev_Release.bat')
		
		try:
			if DebugMenu_Enable_checkbox == True :    # X rev
				bat_file = 'Makea_Release.bat'
			elif DebugMenu_Enable_checkbox == False : # A-Can
				bat_file = 'Makea_Arev_Release.bat'
			subprocess.check_call(f"{bat_file}", shell=True, cwd=f'{folder_path}')
			print('ok')
		except subprocess.CalledProcessError:
			print('error')
			exit(0)

		# Check T drive folder (for rebuild)
		if os.path.isdir(t_drive_folder[0]):
			shutil.rmtree(t_drive_folder[0])

		for index in range(num_platform): # !Cautious : Spitzer only!?
			try:
				if DebugMenu_Enable_checkbox == True :    # X rev
					rel_cmd = 'release.bat' + f" {P[index]['systemname']}" + f" {version_cmd}"
				elif DebugMenu_Enable_checkbox == False : # A-Can
					rel_cmd = 'release.bat' + f" {P[index]['systemname']}" + f" {version_cmd}" + ' A'
				print(f"Run cmd : {rel_cmd}")
				subprocess.check_call(f"{rel_cmd}", shell=True, cwd=f'{folder_path}')
				print(f"[O] release.bat for {P[index]['systemname']}")
			except subprocess.CalledProcessError:
				print('error')

	def upload_to_svn(self):
		client = pysvn.Client()
		file_name = f"{P[0]['systemname']}-0{P[0]['ver_major']}0{P[0]['ver_minor']}0{P[0]['ver_main']}.efi"
		file_path = t_drive_folder[0] + file_name

		# ODM SVN (Foxconn) _input_
		svn_url = f"https://f2dsvn.{P[0]['odm']}.com/svn/14G_misc/{P[0]['codename']}/Release/BIOS/MLK/{version_svn}/{file_name}"
		print(f"[O] Get SVN path : {svn_url}")

		client.import_(path = file_path,
		               url = f'{svn_url}',
		               log_message = 'Hi Webb, EFI file was uploaded. Please help perform POT. Thanks!')
		print(Fore.GREEN + "[O] Successfully upload to svn. Please check it." + Style.RESET_ALL)


	def rename_EFI_withSWB(self):
		for index in range(num_platform):
			os.chdir(t_drive_folder[0])
			new_name  = f"BIOS_{P[index]['swb']}_EFI_{P[index]['ver_major']}.{P[index]['ver_minor']}.{P[index]['ver_main']}.efi"
			for file in os.listdir(t_drive_folder[0]):
			    if file.endswith(".efi"):
			    	# print(f"Found an EFI file : '{file}'")
			    	os.rename(file, new_name)
			    	print(Fore.GREEN + f"[O] EFI has been renamed as '{new_name}'" + Style.RESET_ALL)

	def read_existing_RN(self, filename, index):
		#
		# First, download RN from ODM SVN
		#
		svn_url   = f"https://f2dsvn.{P[index]['odm']}.com/svn/14G_misc/{P[index]['codename']}/Release/BIOS/MLK/{version_svn}/{filename}"
		dest_path = t_drive_folder[index] + filename
		client = pysvn.Client()

		if os.path.isfile(dest_path) != True:
			try:
				client.export(src_url_or_path = svn_url,
								dest_path = dest_path)
				print(Fore.GREEN + f"[O] Download Release Note to {dest_path}" + Style.RESET_ALL)			
			except:
				print(Fore.YELLOW + f"[!] Cannot get Release Note from {svn_url}" + Style.RESET_ALL)
		else:
			print(f"{filename} already exists in T-drive.")
			pass
		
		#
		# Load RN
		#
		contents = []
		contents_row = 0
		try:
			RN_last_ver = open(dest_path, "r", encoding="UTF-8")
			contents = RN_last_ver.read().splitlines()
			for line in contents:
				contents_row += 1
				if line.find(find_Version) != -1:
					if line[line.find(find_Version) + len(find_Version) : line.find(find_Version) + len(find_Version) + len(version_svn)] != version_svn :
						contents = contents[0:contents_row-2]
			contents_row = len(contents)

			print(f"[O] Get RN, total row : '{contents_row}'" + Style.RESET_ALL)
			RN_last_ver.close()

		except IOError:
			print(Fore.RED + f"[X] Can not find Release Note {dest_path}" + Style.RESET_ALL)
			pass

		obj = File_Data(contents, contents_row)
		return obj


	def create_release_mail(self, obj, index):
		version = P[index]['ver_major'] + '.' + P[index]['ver_minor'] + '.' + P[index]['ver_main']
		Title   = f"Release : BIOS, Dell Server BIOS {P[index]['generation']}, {P[index]['codename']} {P[index]['subcodename']}, {P[index]['revision']} {version} ({P[index]['block']}), SWB#{P[index]['swb']}" 
		Content = f"Hi all,\n\
		\n\
		{P[index]['generation']} {P[index]['codename']} {P[index]['subcodename_systemname']} BIOS version {version} {P[index]['revision']} ({P[index]['block']} block) is available on Agile.\n\
		SWB# : {P[index]['swb']}\n\
		{DUP_text}\n\
		\n\
		\n" 

		#
		# Add Release note
		#
		if bool(obj) is not False:
			if obj is not None:
				for line in obj.contents:
					Content += f"{line}\n"

		olook = win32.Dispatch("outlook.application")
		mail = olook.CreateItem(0)
		mail.To = P[index]['receivers']
		mail.CC = P[index]['cc']
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
				print(Fore.YELLOW + f"add {path_BV} to commit" + Style.RESET_ALL)

			if  item.a_path in path_PC:
				repo.git.add(f"{path_PC}")
				print(Fore.YELLOW + f"add {path_PC} to commit" + Style.RESET_ALL)

		repo.git.commit('-m', f"[ESGB-{P[0]['esgb_number']}][{P[0]['codename']}] Change {P[0]['block']} BIOS version to {version}.")
		# repo.git.push('origin', f"{P[0]['working_branch']}")


	def create_rel_branch(self):
		if repo.active_branch.name != P[0]['working_branch']:
			repo.git.checkout(f"{P[0]['working_branch']}")

		repo.git.pull('origin', f"{P[0]['working_branch']}")
		try:
			b = repo.create_head(New_rel_branch)
		except git.exc.GitCommandError:
			print(Fore.GREEN + f"branch {New_rel_branch} already exists")

		b.checkout()
		print(Fore.GREEN + f"[O] Successfully create new rel branch {New_rel_branch}" + Style.RESET_ALL)

	 
	def create_rel_tag(self):
		try:
			print(f"To create new tag {New_rel_tag}")
			repo.create_tag(New_rel_tag)
		except git.exc.GitCommandError:
			print(Fore.GREEN + f"tag {New_rel_tag} already exists" + Style.RESET_ALL)

		print(f"[O] Successfully create new tag {New_rel_tag}")

	def push_branch_tag(self):
		repo.git.push('origin', f"{P[0]['working_branch']}")
		repo.git.push('origin', f"{New_rel_branch}")
		repo.git.push('origin', f"{New_rel_tag}")
		print(Fore.GREEN + f"[O] Successfully push {P[0]['working_branch']}, {New_rel_branch}, {New_rel_tag}" + Style.RESET_ALL)



	def update_INIdata(self):
		with open('readConfig_taurus.ini', 'w') as configfile:
			config.write(configfile)


	def func1(self):
		print("1 working")

	def func2(self):
		print("2 working")

	def func3(self):
		print("3 working")



#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===    Execute    === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #



# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#
# Step 1 : Fetch RN, git repo, and create code change
#

f = Functions()
f.Prepare_for_repo()
repo = git.Repo(P[0]['repo_dell'])
# RN_obj = f.create_RN(Leading_V_RN_File_Name, RN_list_keywords)
# f.edit_BV(BV_list_keywords)
# f.edit_PC(DM_list_keywords)
# time.sleep(10)


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
