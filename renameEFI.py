import os, sys


#
#
# Rename .efi
platform = 'R440'
codename = 'Taurus'
version = '02.07.01'

path = 'T:/Projects/14G.TDC.projects/' + f'{codename}' + '/Release/' + f'{version}'
os.chdir(path)

oldname = f'{platform}' + '-' + '020701.efi'
os.rename(oldname, 'BIOS_MHV07_EFI_2.7.1.efi')
