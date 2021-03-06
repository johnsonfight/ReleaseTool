#
# Non-fixed Const
#
IGNORE_LIST  = ['Spitzer']
CONVERT_DICT = {"Pathfinder":"Skyline", "Sojourner":"Skyline", "Shoemaker":"Ulysses"}

INI = []

P  = {} 
PlatformQueue = []

version        = 'ver_major.ver_minor.ver_main' # e.g.:01.22.00
version_cmd    = 'ver_majorver_minorver_main'   # e.g.:012200
version_svn    = 'ver_major.ver_minor.ver_main' # e.g.:1.22.0

repo           = None
t_drive_folder = {}
read_RN        = {}


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

#
# [DellBiosVersion.h]
#
Str_DellBiosVersion = 'DellBiosVersion.h'
find_Major_ver      = '#define DELL_BIOS_MAJOR_VERSION       '
find_Minor_ver      = '#define DELL_BIOS_MINOR_VERSION       '
find_Main_ver       = '#define DELL_BIOS_MAIN_VERSION        '
find_Build_Month    = '#define DELL_BIOS_BUILD_MONTH         '
find_Build_Day      = '#define DELL_BIOS_BUILD_DAY           '
find_Build_Year     = '#define DELL_BIOS_BUILD_YEAR          '

#
# [PlatformConfig.txt]
#
Str_PlatformConfig  = 'PlatformConfig.txt'
find_DebugMenu_PC   = 'DEFINE DEBUG_MENU_ENABLE                     = '
DebugMenuONOFF = ''

#
# Keywords for get/set code change
#
RN_list_keywords = [find_Version, find_System, find_Release_Date, find_Release_By, find_SWB, find_AEP_Driver, find_Important_Note, find_Known_Issues, find_DebugMenu, find_CHANGES, find_ABP]
BV_list_keywords = [find_Major_ver, find_Minor_ver, find_Main_ver, find_Build_Month, find_Build_Day, find_Build_Year]
DM_list_keywords = find_DebugMenu_PC

#
# [mail]
#
DUP_Available_string    = 'DUPs are available on Agile.'
DUP_NOT_Avaiable_string = 'DUPs are NOT available on Agile.'
DUP_text = ''

#
#
#
ini_file = ""