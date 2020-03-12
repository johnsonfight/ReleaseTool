import os
import git
import configparser #-

config = configparser.ConfigParser() #-
config.read('readConfig.ini') #-

s_repoPath = config.get('git', 'repo_dell') 



print(s_repoPath)

if os.path.isdir(s_path):
	repo = git.Repo(s_repoPath)
# else:
# 	print(s_repoPath)

print(repo)
exit(1)

list_branch_from = 'remotes/origin/stg/14gmlk' ### Add checking branch exits or not
list_commits = list(repo.iter_commits(f'{list_branch_from}', max_count = 50)) ### Need to modify to Start-End


#
# Find CPI by folder path
#
for each_commit in list_commits :
	for each_file in each_commit.stats.files :
		if each_file.find('DellPkgs/DellPlatformPkgs/DellAtlasPkg') != -1 :
			# if each_file.find('DellBiosVersion.h') == -1 :
			if each_file.find('.c', -2) != -1 :  ### Need to make sure whether all CPI are .c file 
				print(each_commit)
				print(each_file)
				print(each_commit.message)
				print('\n')
				break

#
# Pull and Cherry pick
#
		
exit(1)
	# each_commit.stats.files


#
# Find CPI with #CPI
#
# for each_commit in list_commits :
# 	if each_commit.message.find('CPI') != -1 :
# 		print(each_commit)
# 		print(each_commit.stats.files)
# 		print(each_commit.message.find('CPI'))
# 		print(each_commit.message)




#
# Find SPS_version changed
#
# for each_commit in list_commits :
# 	if each_commit.message.find('Update SPS to SPS') != -1 :
# 		print(each_commit)
# 		print(each_commit.stats.files)
# 		print(each_commit.message.find('Update SPS to SPS'))
# 		print(each_commit.message)

# exit(1)