#release mail template 
import os
import git
import configparser #-
from datetime import date

DUP_text = ''
DUP_Availablity = 1
# DUP_Availablity = 0


config = configparser.ConfigParser() #-
config.read('readConfig_taurus.ini') #-

today = date.today()
config.set('date', 'day', f'{today.day}')
config.set('date', 'month', f'{today.month}')
config.set('date', 'year', f'{today.year}')

user_first_name = config.get('user', 'first_name')
user_last_name = config.get('user', 'last_name')

platform_generation = config.get('platform', 'generation')
platform_codeName = config.get('platform', 'codeName') 
platform_subCodeName = config.get('platform', 'subCodeName')
platform_systemName = config.get('platform', 'systemName') 
platform_subCodeName_systemName = config.get('platform', 'subCodeName_systemName')
platform_ver_major = config.get('platform', 'version_major')
platform_ver_minor = config.get('platform', 'version_minor')
platform_ver_main = config.get('platform', 'version_main')

schedule_block = config.get('schedule', 'block')
schedule_revision = config.get('schedule', 'revision')
schedule_softwareBundle = config.get('schedule', 'softwareBundle')
schedule_ESGB_number = config.get('schedule', 'ESGB_number')

git_repo_dell = config.get('git', 'repo_dell') 
git_working_branch = config.get('git', 'working_branch')

email_receivers = config.get('email', 'receivers') 
email_cc = config.get('email', 'cc') 

platform_codeName_lower = platform_codeName.lower()
new_rel_branch = f'rel/{platform_codeName_lower}/{platform_codeName_lower}_{platform_ver_major}_{platform_ver_minor}_{platform_ver_main}'
new_rel_tag = f'{platform_codeName}/{platform_ver_major}_{platform_ver_minor}_{platform_ver_main}'

if os.path.isdir(git_repo_dell):
	repo = git.Repo(git_repo_dell)
	# r = repo.remotes.origin
	print(repo)
else:
	print('did not get repo')



DUP_Available_string = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'

if DUP_Availablity is 1:
	DUP_text = DUP_Available_string
else:
	DUP_text = DUP_NOT_Avaiable_string

# print ("read_account = ", user_account )

# print ()
# print ("s_password = ", s_password )
# print ("s_codeName = ", s_codeName )
# print ("s_systemName = ", s_systemName )
# print ("s_version = ", s_version )
# print ("s_repoPath = ", s_repoPath )


platform_version = f'{platform_ver_major}.{platform_ver_minor}.{platform_ver_main}'
Mail_Title = ''
Mail_Content = ''
#
# Create mail
#

def create_release_mail(Title, Content):
	Title = f'Release : BIOS, Dell Server BIOS {platform_generation}, {platform_codeName} {platform_subCodeName}, {schedule_revision} {platform_version} ({schedule_block}), SWB#{schedule_softwareBundle}' 
	print(Content)
	print('\n')
	print('\n')

	Content = f'Hi all,\n\
	\n\
	{platform_generation} {platform_codeName} {platform_subCodeName_systemName} BIOS version {platform_version} {schedule_revision} ({schedule_block} block) is available on Agile.\n\
	SWB# : {schedule_softwareBundle}\n\
	{DUP_text}\n\
	\n\
	Please check internal release note for the detail of BIOS changes.\n\
	Thanks.\n\
	\n\
	Best Regards,\n\
	{user_first_name} {user_last_name}'  #Convert first letter to Capital 
	print(Content)
	return Title, Content

# Release : BIOS, Dell Server BIOS Polaris, Taurus (Ice, Rosetta, Genesis) , X-Rev , 2.7.2 (JunFY21), SWB#MHV07 (X02-00)


#
# Generate a copy .txt file
#
def write_into_txt(Title, Content):
    try:
        file = open(f'Date_Mail_{platform_codeName}_{platform_version}.txt', 'a')
        file.truncate(0) #clear the file
        file.close()

    except IOError:
        file = open(f'Date_Mail_{platform_codeName}_{platform_version}.txt', 'w+')
        file.close()

    # Put the result from the list to the txt file
    with open(f'Date_Mail_{platform_codeName}_{platform_version}.txt', 'a') as mail_copy:
        mail_copy.writelines(f'To : {email_receivers}')
        mail_copy.write('\n')
        mail_copy.writelines(f'Cc : {email_cc}')
        mail_copy.write('\n')
        mail_copy.writelines(f'Title : {Title}')
        mail_copy.write('\n')
        mail_copy.writelines(Content)
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.write('----------------------------------------------------')
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.close()
# write_into_txt()


#
# Python package to send
#


#
# Create rel branch
#
# [ESGB-2148][Taurus] Change JunFY21 BIOS version to 02.07.04.

def commit_block_branch():
	repo.git.checkout(f'{git_working_branch}')
	repo.git.pull('origin', f'{git_working_branch}')

	# Do Not commit Recovery .rom
	if repo.git.status().find('16MBRecoveryBios.rom') != 0 :
		repo.git.reset('DellPkgs/DellPlatformPkgs/DellTaurusPkg/BiosRecovery/Taurus_16MBRecoveryBios.rom')

	repo.git.commit('-m', f'[ESGB-{schedule_ESGB_number}][{platform_codeName}] Change {schedule_block} BIOS version to 0{platform_ver_major}.0{platform_ver_minor}.0{platform_ver_main}.')


	# repo.git.push('origin', f'{git_working_branch}')

def create_rel_branch():
	try:
		b = repo.create_head(new_rel_branch)
	except git.exc.GitCommandError:
		print(f'branch {new_rel_branch} already exists')

	b.checkout()
	repo.git.push('origin', f'{git_working_branch}')


 
def create_rel_tag():
	try:
		repo.create_tag(new_rel_tag)
	except git.exc.GitCommandError:
		print(f'tag {new_rel_tag} already exists')

	repo.git.push('origin', f'{new_rel_tag}')


def test_print():
	print('test test')

def update_INIdata():
	with open('readConfig_taurus.ini', 'w') as configfile:
		config.write(configfile)

# update_INIdata()
# commit_block_branch()
# create_rel_branch()
# create_rel_tag()
Mail_Title, Mail_Content = create_release_mail(Mail_Title, Mail_Content)
write_into_txt(Mail_Title, Mail_Content)