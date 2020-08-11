import os
import re

Target_Directory = '/Users/bomi.chen/Developer/Project_Name/'
Target_Extension = '.swift'
Target_Replaced_Syntax = 'R\.image\.(.+)\(\)'
Target_Syntax = 'Resource.image.named("%s")'


print('=== START PROCESS in derectory: %s ===' % Target_Directory)
for dirPath, dirs, files in os.walk(Target_Directory):

	# skip file
	if '/iOS_CaiLiFang/Pods/' in dirPath:
		continue

	print('File: %s', dirPath)
	for file in files:

		print(file)

		# if file == 'orange_devTests.swift' or file == 'FiveStarTest.swift':
			# continue

		if file.endswith(Target_Extension):

			fileName = os.path.join(dirPath, file)

			print(fileName)
			f = open(fileName, "r", encoding='UTF-8')
			lines = f.readlines()
			for index, line in enumerate(lines):
				# find image line
	    		# case: \? R\.image\.(.+)\(\)\?.tint\(color:.+\) \:
	    		# case: \? R\.image\.(.+)\(\)\?.tint
	    		# case: \? R\.image\.(.+)\(\)\! \:
	    		# case: \? R\.image\.(.+)\(\) \:
	    		# case: R\.image\.(.+)\(\),
	    		# case: R\.image\.(.+)\(\)

	    		# find name line
	    		# case: R\.image\.(.+)\.name,
	    		# case: R\.image\.(.+)\.name
				if 'R.image.' in line:

					match_0 = re.search('\? R\.image\.(.+)\(\)\?.tint\(color:.+\) \:', lines[index])
					if match_0:
						group_m = match_0.group(1)
						match_str = match_0.group()
						match_color = re.search('\? R\.image\.%s\(\)\?\.tint\(color:(.+)\) \:' % group_m, match_str)
						if match_color:
							lines[index] = lines[index].replace(match_str, '? %s?.tint(color:%s) :' % (Target_Syntax % group_m, match_color.group(1)))

					match_1 = re.search('\? R\.image\.(.+)\(\)\?.tint', lines[index])
					if match_1:
						group_m = match_1.group(1)
						lines[index] = lines[index].replace('? R.image.%s()?.tint' % group_m, '? %s?.tint' % (Target_Syntax % group_m))

					match_2 = re.search('\? R\.image\.(.+)\(\)\! \:', lines[index])
					if match_2:
						group_m = match_2.group(1)
						lines[index] = lines[index].replace('? R.image.%s()! :' % group_m, '? %s! :' % Target_Syntax % group_m)

					match_3 = re.search('\? R\.image\.(.+)\(\) \:', lines[index])
					if match_3:
						group_m = match_3.group(1)
						lines[index] = lines[index].replace('? R.image.%s() :' % group_m, '? %s :' % Target_Syntax % group_m)

					match_last = re.search('R\.image\.(.+)\(\)', lines[index])
					if match_last:
						group_m = match_last.group(1)
						# print('match line: %s' % lines[index])
						lines[index] = lines[index].replace('R.image.%s()' % group_m, '%s' % Target_Syntax % group_m)
						# print('change to: %s' % lines[index])

					match_name_first = re.search('R\.image\.(.+)\.name,', lines[index])
					if match_name_first:
						group_m = match_name_first.group(1)
						match_str = match_name_first.group()
						lines[index] = lines[index].replace(match_str, '"%s",' % group_m)

					match_name = re.search('R\.image\.(.+)\.name', lines[index])
					if match_name:
						group_m = match_name.group(1)
						match_str = match_name.group()
						lines[index] = lines[index].replace(match_str, '"%s"' % group_m)

					
			f_write = open(fileName, "w", encoding='UTF-8')
			f_write.writelines(lines)
			print('file complete: %s' % fileName)

print('=== COMPLETE PROCESS ===')

