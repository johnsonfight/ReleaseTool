import os, sys
import time, datetime
import shutil
import configparser

config = configparser.ConfigParser() 
config.read('readConfig_taurus.ini') 



platform = 'R440'
codename = 'Taurus'
version = '02.07.01'

platform_systemName = config.get('platform', 'systemName') 
platform_codeName = config.get('platform', 'codeName') 
platform_ver_major = config.get('platform', 'version_major')
platform_ver_minor = config.get('platform', 'version_minor')
platform_ver_main = config.get('platform', 'version_main')
# versio_full = f'0{platform_ver_major}0{platform_ver_minor}0{platform_ver_main}'
schedule_softwareBundle = config.get('schedule', 'softwareBundle')


#
# Rename .efi for SWB
#
path = 'T:/Projects/14G.TDC.projects/' + f'{platform_codeName}' + '/Release/' + f'0{platform_ver_major}.0{platform_ver_minor}.0{platform_ver_main}'
os.chdir(path)

oldname = f'{platform}' + '-' + f'0{platform_ver_major}0{platform_ver_minor}0{platform_ver_main}.efi'
os.rename(oldname, f'BIOS_{schedule_softwareBundle}_EFI_{platform_ver_major}.{platform_ver_minor}.{platform_ver_main}.efi')

