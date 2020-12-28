from datetime import date
import time
import os, sys, shutil, subprocess
import win32com.client as win32
import git, pysvn
import configparser
from colorama import init, Fore, Back, Style
init()
os.system('cls')

#
# Non-fixed Const
#
IGNORE_LIST  = ['Spitzer']
CONVERT_DICT = {"Pathfinder":"Skyline", "Sojourner":"Skyline"}

#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  Initialize   === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #
#  === === === === ===  == == == ==  === === === === ===  #


config = configparser.ConfigParser()
config_file = f'{sys.argv[1]}'
# print(os.getcwd() + "\\" + config_file)
if os.path.isfile(f'./{config_file}'):
	config.read(config_file)
else:
	print(f"{config_file} file is not exist.")
	exit(1)

print(Fore.GREEN + f"[O] Read configuartion from '{config_file}'. Please double check configuration is correct." + Style.RESET_ALL)

INI = []
for i in config.sections():
	INI.append(dict(config.items(i)))

P  = {} 
PlatformQueue = []
for i in config.sections():
	if i == "CommonData":
		pass
	else:
		PlatformQueue.append(i) # Init build queue
		P.update({i:dict(config.items(i))})
num_platform = len(P)


version        = 'ver_major.ver_minor.ver_main'
version_cmd    = 'ver_majorver_minorver_main'
version_svn    = 'ver_major.ver_minor.ver_main'

f     = lambda target, i, number : target.replace(i, '0'+number) if (int(number) < 10) else target.replace(i, number)
f_svn = lambda target, i, number : target.replace(i, number) if (int(number) < 10) else target.replace(i, number)

for i in ['ver_major', 'ver_minor', 'ver_main']:
	version     = f(version, i, INI[0][i])
	version_cmd = f(version_cmd, i, INI[0][i])
	version_svn = f_svn(version_svn, i, INI[0][i])

repo           = None
DebugMenu_Enable_checkbox = None
t_drive_folder = {}
read_RN        = {}


if INI[0]['revision'] == 'X-rev':
	print(Fore.YELLOW + '[!] This is X-rev' + Style.RESET_ALL)
	DebugMenu_Enable_checkbox = True 

elif INI[0]['revision'] == 'A-can':
	print(Fore.YELLOW + '[!] This is A-can' + Style.RESET_ALL)
	DebugMenu_Enable_checkbox = False 

if DebugMenu_Enable_checkbox == True : # X-rev
	DebugMenuONOFF = 'Enabled'
	C = ''
	for i in PlatformQueue:
		t_drive_folder.update({i:f"T:/Projects/14G.TDC.projects/{P[i]['codename']}/Release/{version}{C}/"})

elif DebugMenu_Enable_checkbox == False : # A-Can
	DebugMenuONOFF = 'Disabled'
	C = '-C'
	for i in PlatformQueue:
		t_drive_folder.update({i:f"T:/Projects/14G.TDC.projects/{P[i]['codename']}/Release/{version}{C}/{P[i]['systemname']}/"})

for i in PlatformQueue:
	read_RN.update({i:f"{P[i]['systemname']}-{version_cmd}.txt"})

DUP_Available_string    = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'
DUP_text = ''


#
# Files needed to be modified
#
# Leading_V_RN_File_Name   = f"{INI[0]['leading_v']}-0{INI[0]['ver_major']}0{INI[0]['ver_minor']}0{INI[0]['ver_main']}.txt"
# This_ver_RN              = f"{INI[0]['systemname']}-0{INI[0]['ver_major']}0{INI[0]['ver_minor']}0{INI[0]['ver_main']}_test.txt"
# RN_file_name   = f"{INI[0]['systemname']}-0{INI[0]['ver_major']}0{INI[0]['ver_minor']}0{INI[0]['ver_main']}.txt"
# RN_file_name_2 = f"{P[1]['systemname']}-0{P[1]['ver_major']}0{P[1]['ver_minor']}0{P[1]['ver_main']}.txt"
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
		if os.path.isdir(INI[0]['repo_dell']):
			repo = git.Repo(INI[0]['repo_dell'])
			# r = repo.remotes.origin
			print(Fore.GREEN + f"[O] Find repo : {repo}" + Style.RESET_ALL)
		else:
			print('[X] Did not find repo')

		print(Fore.YELLOW + f"[!] Check out {INI[0]['working_branch']}" + Style.RESET_ALL)
		repo.git.checkout(f"{INI[0]['working_branch']}")
		repo.git.pull('origin', f"{INI[0]['working_branch']}")

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
		# filename = f"{INI[0]['codename']}-0{INI[0]['ver_major']}0{INI[0]['ver_minor']}0{INI[0]['ver_main']}_Test.txt"
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
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{INI[0]['ver_major']}.{INI[0]['ver_minor']}.{INI[0]['ver_main']}"
				elif keywords == find_System:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{INI[0]['codename']} {INI[0]['subcodename_systemname']}"
				elif keywords == find_Release_Date:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{INI[0]['month']}/{INI[0]['day']}/{INI[0]['year']}"
				elif keywords == find_Release_By:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{INI[0]['name']}"
				elif keywords == find_SWB:
					obj.contents[i] = obj.contents[i][:(index + len(keywords))] + f"{INI[0]['swb']}"
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
					obj.contents.insert(i+2, f"1. [ESGB-{INI[0]['esgb_number']}] Change {INI[0]['block']} BIOS version to 0{INI[0]['ver_major']}.0{INI[0]['ver_minor']}.0{INI[0]['ver_main']}")
					obj.contents.insert(i+3, f"2. Sync to 14G codebase to launch-1(Atlas) {INI[0]['ver_major']}.{INI[0]['ver_minor']}.{INI[0]['ver_main']}")
					obj.contents.insert(i+4, f"")
					obj.contents.insert(i+5, '*************************************************')
					obj.contents.insert(i+6, f"Sync to 14G codebase to launch-1(Atlas) {INI[0]['ver_major']}.{INI[0]['ver_minor']}.{INI[0]['ver_main']}")
					obj.contents.insert(i+7, '*************************************************')

					print(f"\n----------------------------------------------------------------------")
					print(f"Release Note '{This_ver_RN}' has been created. Please check it. \n")

				elif keywords == find_ABP:
					obj.contents[i].replace("#22", "#02") #*

				break

			except ValueError:
				i += 1

		return obj.contents


	def find_keywords_n_edit_BV(self, obj, keywords, hashtag):
		index = 0
		i = 0
		while i < obj.row:			
			if obj.contents[i].find(f'{hashtag} start') != -1:
				j = i
				while j < i + 70:
					if obj.contents[i].find(f'{hashtag} end') != -1:
						break
					try:
						index = obj.contents[j].index(keywords)
						if keywords == find_Major_ver:
							print('----' + f"Code change in '{Last_ver_DellBiosVersion}' : \n")
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['ver_major']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Minor_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['ver_minor']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Main_ver:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['ver_main']}"
							print('        ' + obj.contents[j])
							print('')
							break
						elif keywords == find_Build_Month:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['month']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Build_Day:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['day']}"
							print('        ' + obj.contents[j])
							break
						elif keywords == find_Build_Year:
							obj.contents[j] = obj.contents[j][:(index + len(keywords))] + f"{INI[0]['year'][-2:]}"
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


	def find_keywords_n_edit_DM(self, obj, keywords, hashtag, DebugMenuONOFF):
		index = 0
		i = 0
		while i < obj.row:
			if obj.contents[i].find(f'{hashtag} start') != -1:
				j = i
				while j < i + 10:
					if obj.contents[i].find(f'{hashtag} end') != -1:
						break
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


	def edit_BV(self, platform, keywords):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			platform_hashtag = f"_{P[platform]['codename']}_" # hashtag
			print(Back.CYAN + f"\n")
			print(f"----------------------------")
			print(f"-- Edit DellBiosVersion.h --")
			print(f"----------------------------")
			print(Style.RESET_ALL)
			path_BV   = INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{platform}Pkg/Include/" + Last_ver_DellBiosVersion

			if os.path.isfile(path_BV):
				print(f"[O] Find the file : {path_BV}")
			else:
				print(Fore.RED + f"[X] Did not find : {path_BV}" + Style.RESET_ALL)

			[get_contents, get_row] = self.Read_last_version_File(path_BV)
			obj = File_Data(get_contents, get_row)
			# print(obj.row)

			for each_keywords in keywords :
				new_contents = self.find_keywords_n_edit_BV(obj, each_keywords, platform_hashtag)

			self.Create_this_version(obj, path_BV)

	def edit_PC(self, platform, keywords):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			platform_hashtag = f"_{P[platform]['codename']}_" # hashtag
			print(Back.CYAN + f"\n")
			print(f"-----------------------------")
			print(f"-- Edit PlatformConfig.txt --")
			print(f"-----------------------------")
			print(Style.RESET_ALL)
			path_PC   = INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{platform}Pkg/" + Last_ver_PlatformConfig

			if os.path.isfile(path_PC):
				print(f"[O] Find the file : {path_PC}")
			else:
				print(Fore.RED + f"[X] Did not find : {path_PC}" + Style.RESET_ALL)

			[get_contents, get_row] = self.Read_last_version_File(path_PC)
			obj = File_Data(get_contents, get_row)

			new_contents = self.find_keywords_n_edit_DM(obj, keywords, platform_hashtag, DebugMenuONOFF)

			self.Create_this_version(obj, path_PC)

	def scan_CPI(self, platform):
		print(platform)
		# if platform in IGNORE_LIST :
		# 	pass
		# else:
		# 	print(Back.CYAN)
		# 	print(f"--------------")
		# 	print(f"-- Scan CPI --")
		# 	print(f"--------------")
		# 	print(Style.RESET_ALL)
		# 	index = 0
		# 	cpi_num = 0
		# 	list_commits = list(repo.iter_commits(INI[0]['working_branch'], max_count = 70))
		# 	for commit in list_commits:
		# 		if commit.message.find("version change") != -1:
		# 			if commit.message.find(f"{INI[0]['ver_major']}.{INI[0]['ver_minor']}.{INI[0]['ver_main']}") == -1:
		# 				# print(commit.message)
		# 				index = list_commits.index(commit)
		# 				# print(index)
		# 				break
		# 			# if commit.find("")
		# 	list_commits = list(repo.iter_commits(INI[0]['working_branch'], max_count = index))

		# 	for commit in list_commits:
		# 		for file in commit.stats.files:
		# 			if file.find("DellPkgs/DellPlatformPkgs/DellAtlasPkg") != -1:
		# 				if file.find("DellPkgs/DellPlatformPkgs/DellAtlasPkg/Include/DellBiosVersion.h") == -1:
		# 					print(f"\n---------------------------------------------")
		# 					print(f"    Path : " + f"{file}")
		# 					print(f"    Author : {commit.author}")
		# 					print(f"    Date and time : {commit.authored_datetime}")
		# 					print(f"    SHA number : {commit}")
		# 					print(f"---------------------------------------------")
		# 					cpi_num += 1

		# 	if cpi_num is 0:
		# 		print("[O] Found no CPI.\n")
		# 	else :
		# 		print(f"[O] Found {cpi_num} suspicious CPI.\n")
		# 		print(f"    Please check whether these are neccessary CPI or not.\n")
		# 		print(f"    If yes, please get the CPI to your platform MAUALLY.\n")

	def check_before_POT(self):
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
			print(item.a_path)
			# print(dir(item))
			# print('\n')


	#
	# Build & Release & upload SVN & Rename EFI
	#
	def build_n_release(self, platform):
		if platform in IGNORE_LIST :
			pass
		else:
			# print(INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[platform]['codename']}Pkg/")
			# time.sleep(2)
			folder_path = INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{P[platform]['codename']}Pkg/"

			# print(folder_path + 'Makea_Arev_Release.bat')
			
			try:
				if DebugMenu_Enable_checkbox == True :    # X-rev
					bat_file = 'Makea_Release.bat'
				elif DebugMenu_Enable_checkbox == False : # A-Can
					bat_file = 'Makea_Arev_Release.bat'
				subprocess.check_call(f"{bat_file}", shell=True, cwd=f'{folder_path}')
				print('ok')
			except subprocess.CalledProcessError:
				print('error')
				exit(0)

		# Check T drive folder (for rebuild)
		if os.path.isdir(t_drive_folder[platform]):
			shutil.rmtree(t_drive_folder[platform])

		try:
			if DebugMenu_Enable_checkbox == True :    # X-rev
				rel_cmd = 'release.bat' + f" {P[platform]['systemname']}" + f" {version_cmd}"
			elif DebugMenu_Enable_checkbox == False : # A-Can
				rel_cmd = 'release.bat' + f" {P[platform]['systemname']}" + f" {version_cmd}" + ' A'
			print(f"Run cmd : {rel_cmd}")
			subprocess.check_call(f"{rel_cmd}", shell=True, cwd=f'{folder_path}')
			print(f"[O] release.bat for {P[platform]['systemname']}")
		except:
				print('Exception')

	def upload_to_svn(self, platform):
		if platform in IGNORE_LIST :
			pass
		else:
			client = pysvn.Client()
			file_name = f"{P[platform]['systemname']}-0{INI[0]['ver_major']}0{INI[0]['ver_minor']}0{INI[0]['ver_main']}.efi"
			file_path = t_drive_folder[platform] + file_name

			# ODM SVN (Foxconn) _input_
			svn_url = f"https://f2dsvn.{P[platform]['odm']}.com/svn/14G_misc/{P[platform]['codename']}/Release/BIOS/MLK/{version_svn}/{file_name}"
			print(f"[O] Get SVN path : {svn_url}")

			client.import_(path = file_path,
			               url = f'{svn_url}',
			               log_message = 'Hi Webb, EFI file was uploaded. Please help perform POT. Thanks!')
			print(Fore.GREEN + "[O] Successfully upload to svn. Please check it." + Style.RESET_ALL)


	def rename_EFI_withSWB(self):
		for index in range(num_platform):
			os.chdir(t_drive_folder[platform])
			new_name  = f"BIOS_{P[index]['swb']}_EFI_{P[index]['ver_major']}.{P[index]['ver_minor']}.{P[index]['ver_main']}.efi"
			for file in os.listdir(t_drive_folder[platform]):
			    if file.endswith(".efi"):
			    	# print(f"Found an EFI file : '{file}'")
			    	os.rename(file, new_name)
			    	print(Fore.GREEN + f"[O] EFI has been renamed as '{new_name}'" + Style.RESET_ALL)

	def read_existing_RN(self, filename, platform):
		#
		# First, download RN from ODM SVN
		#
		svn_url   = f"https://f2dsvn.{P[platform]['odm']}.com/svn/14G_misc/{P[platform]['codename']}/Release/BIOS/MLK/{version_svn}/{filename}"
		dest_path = t_drive_folder[platform] + filename
		client = pysvn.Client()

		print(dest_path)

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
			RN = open(dest_path, "r", encoding="UTF-8")
			contents = RN.read().splitlines()
			for line in contents:
				contents_row += 1
				if line.find(find_Version) != -1:
					if line[line.find(find_Version) + len(find_Version) : line.find(find_Version) + len(find_Version) + len(version_svn)] != version_svn :
						contents = contents[0:contents_row-2]
			contents_row = len(contents)

			print(f"[O] Get RN, total row : '{contents_row}'" + Style.RESET_ALL)
			RN.close()

		except IOError:
			obj = File_Data(contents, contents_row)
			return obj

		obj = File_Data(contents, contents_row)
		return obj


	def create_release_mail(self, obj, platform, DUP_Checkbox):
		if DUP_Checkbox is True:
			DUP_text = DUP_Available_string
		else:
			DUP_text = DUP_NOT_Avaiable_string
		print(DUP_text)
		version = INI[0]['ver_major'] + '.' + INI[0]['ver_minor'] + '.' + INI[0]['ver_main']
		Title   = f"Release : BIOS, Dell Server BIOS {P[platform]['generation']}, {P[platform]['codename']} {P[platform]['subcodename']}, {INI[0]['revision']} {version} ({INI[0]['block']}), SWB#{P[platform]['swb']}" 
		Content = f"Hi all,\n\
		\n\
		{P[platform]['generation']} {P[platform]['codename']} {P[platform]['subcodename_systemname']} BIOS version {version} {INI[0]['revision']} ({INI[0]['block']} block) is available on Agile.\n\
		SWB# : {P[platform]['swb']}\n\
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
		mail.To = P[platform]['receivers']
		mail.CC = P[platform]['cc']
		mail.Subject = Title
		mail.Body = Content
		mail.Display(True)


	def commit_block_branch(self, platform):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			path_BV = INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{platform}Pkg/Include/" + Last_ver_DellBiosVersion
			path_PC = INI[0]['repo_dell'] + 'DellPkgs/DellPlatformPkgs/' + f"Dell{platform}Pkg/"         + Last_ver_PlatformConfig
			version = f"0{INI[0]['ver_major']}.0{INI[0]['ver_minor']}.0{INI[0]['ver_main']}"

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

			repo.git.commit('-m', f"[ESGB-{P[platform]['esgb_number']}][{P[platform]['codename']}] Change {INI[0]['block']} BIOS version to {version}.")
			# repo.git.push('origin', f"{INI[0]['working_branch']}")


	def create_rel_branch(self, platform):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			Codename_lower = P[platform]['codename'].lower()
			New_rel_branch = f"rel/{Codename_lower}/{Codename_lower}_{INI[0]['ver_major']}_{INI[0]['ver_minor']}_{INI[0]['ver_main']}"
			
			if repo.active_branch.name != INI[0]['working_branch']:
				repo.git.checkout(f"{INI[0]['working_branch']}")

			repo.git.pull('origin', f"{INI[0]['working_branch']}")
			try:
				b = repo.create_head(New_rel_branch)
			except git.exc.GitCommandError:
				print(Fore.GREEN + f"branch {New_rel_branch} already exists")

			b.checkout()
			print(Fore.GREEN + f"[O] Successfully create new rel branch {New_rel_branch}" + Style.RESET_ALL)

	 
	def create_rel_tag(self, platform):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			New_rel_tag = f"{P[platform]['codename']}/{INI[0]['ver_major']}_{INI[0]['ver_minor']}_{INI[0]['ver_main']}"
			try:
				# print(f"To create new tag {New_rel_tag}")
				repo.create_tag(New_rel_tag)
			except git.exc.GitCommandError:
				print(Fore.GREEN + f"tag {New_rel_tag} already exists" + Style.RESET_ALL)

			print(Fore.GREEN + f"[O] Successfully create new tag {New_rel_tag}" + Style.RESET_ALL)

	def push_branch_tag(self, platform):
		if platform in CONVERT_DICT :
			platform = CONVERT_DICT[platform]
		if platform in IGNORE_LIST :
			pass
		else:
			Codename_lower = P[platform]['codename'].lower()
			New_rel_branch = f"rel/{Codename_lower}/{Codename_lower}_{INI[0]['ver_major']}_{INI[0]['ver_minor']}_{INI[0]['ver_main']}"
			New_rel_tag    = f"{P[platform]['codename']}/{INI[0]['ver_major']}_{INI[0]['ver_minor']}_{INI[0]['ver_main']}"

			repo.git.push('origin', f"{INI[0]['working_branch']}")
			repo.git.push('origin', f"{New_rel_branch}")
			repo.git.push('origin', f"{New_rel_tag}")
			print(Fore.GREEN + f"[O] Successfully push {INI[0]['working_branch']}, {New_rel_branch}, {New_rel_tag}" + Style.RESET_ALL)


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
repo = git.Repo(INI[0]['repo_dell'])
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
