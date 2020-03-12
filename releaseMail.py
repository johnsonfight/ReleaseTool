#release mail template 
import os
import configparser #-

DUP_text = ''
DUP_Availablity = 1
# DUP_Availablity = 0


config = configparser.ConfigParser() #-
config.read('readConfig.ini') #-


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



#
# Create mail
#
Mail_Title = f'Release : BIOS, Dell Server BIOS {platform_generation}, {platform_codeName} {platform_subCodeName}, {schedule_revision} ({schedule_block}), SWB#{schedule_softwareBundle}' 
print(Mail_Title)
print('\n')
print('\n')

Mail_Content = f'Hi all,\n\
\n\
{platform_generation} {platform_codeName} {platform_systemName} BIOS version {platform_version} {schedule_revision} ({schedule_block} block) is avaiable on Agile.\n\
SWB# : {schedule_softwareBundle}\n\
{DUP_text}\n\
\n\
Please check internal release note for the detail of BIOS changes.\n\
Thanks.\n\
\n\
Best Regards,\n\
{user_account}'  #Convert first letter to Capital 
print(Mail_Content)

# Release : BIOS, Dell Server BIOS Polaris, Taurus (Ice, Rosetta, Genesis) , X-Rev , 2.7.2 (JunFY21), SWB#MHV07 (X02-00)


#
#Generate a copy .txt file
#
def write_into_txt():
    # Put the result from the list to the txt file
    with open(f'Date_Mail_{platform_codeName}_{platform_version}.txt', 'a') as mail_copy:
        mail_copy.writelines(Mail_Content)
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.write('----------------------------------------------------')
        mail_copy.write('\n')
        mail_copy.write('\n')
        mail_copy.close()
write_into_txt()


#
# Python package to send
#

