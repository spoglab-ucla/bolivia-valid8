import random
import os
import sys

'''
    This script takes in 1 argument: the master folder which contains subdirectories for each child.
    It then processes it by making randomized lists of all the clips to be pulled.
'''

mainclipfolder = sys.argv[1]
subfolders = [f for f in os.listdir(mainclipfolder) if  os.path.isdir(os.path.join(mainclipfolder,f))]
random.seed(1)
path_to_jumbo = os.path.join(mainclipfolder, 'all_child_clips_randomized.txt')

for chopped_folder in subfolders:
    namesofclips = [f for f in os.listdir(os.path.join(mainclipfolder,chopped_folder))]
    random.shuffle(namesofclips)
    path_to_roster = os.path.join(mainclipfolder, chopped_folder, chopped_folder+'_clips_randomized.txt')
    with open(path_to_roster , 'w') as newfile , open(path_to_jumbo , "a+") as jumbo:
        for line in namesofclips:
            newfile.write(line + '\n')
            jumbo.write(line + '\n')



