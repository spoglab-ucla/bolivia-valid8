''' 
    ==========================================
    SPOG Lab, UCLA
    Version 04, published on May 10, 2024
    Authors: Arjun Pawar and Dr. Meg Cychosz
    ==========================================
'''
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from functools import partial
import os
import subprocess
import random
import datetime
import sys

link_to_chopped_clips_folder = sys.argv[1]
annotator_name = sys.argv[2]

# DEFINING FILEPATH CONSTANTS

# folder with all clips
clipfolder = link_to_chopped_clips_folder

# text file with clip names in order
all_clips_in_order = os.path.join(link_to_chopped_clips_folder, 'filemapping.txt') 

outdir = link_to_chopped_clips_folder #folder with responses.csv

#number of minute-audio-clips in folder; index of row in df
idx = 0
USER_INP = ''
df = None
row = None
resp_df = None
allfilenames = []
actualnames = []
NUM_VALUES = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','>30','Unclear']
LANG_VALUES = ["Spanish", "Quechua", "Mixed", "Unsure", "Only researcher speech","Too short to tell", "No speech"]   
SPEAKER_VALUES = [ "Adult male", "Adult female", "Other child & adult male", "Other child & adult female","Other child","Target child","Adult male & target child", "Adult female & target child", "Target child with other child", "Adult male & female both", "Electronic media/noise", "Unsure"]

#helper function
def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list

# clear category and media selection   
def clear():
    mediacat.set(0)
    langcategory.set("Categorize language")
    scategory.set("Categorize speaker")
    wcategory.set("Choose a number") 
    sylcategory.set("Choose a number")
    phcategory.set("Choose a number")


# need to give multiple commands to button below
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

# this function loads the randomized list of clips (if available) or creates a new list (if not made)
def createRandomizationOrder():
    global allfilenames
    clips_to_play = os.path.join(clipfolder, USER_INP, USER_INP+"_xxxx_randomized.txt")
    file1 = open(clips_to_play, 'r')
    lines = file1.readlines()
    for eachline in lines:
        #pair = eachline.strip()
        #comma = pair.find(",")
        #oldname = (pair[0:comma]).strip()
        #newname = (pair[comma+1:]).strip()
        allfilenames.append(eachline.strip())
        actualnames.append(eachline.strip())

# set up initial pieces
def annotatorinfo():
    global df
    global outdir
    global content
    global resp_df
    global allfilenames
    global idx     
    global USER_INP
    
    wrong = True
    while (wrong):
        USER_INP = tk.simpledialog.askstring(title="CHILD ID",prompt="Out of the below child IDs which one do you want to annotate? 1065, 1050, 1094, 1071, 1090, 1062, 1034, 1083, 1039, 1054, 1042, 1029")
        if USER_INP in ['1065', '1050', '1094', '1071', '1090', '1062', '1034', '1083', '1039', '1054', '1042', '1029']:
            wrong = False

    try: # if available, open the response df so we can append new work to it

        resp_df = pd.read_csv(os.path.join(outdir, annotator_name+"_"+USER_INP+"_responses.csv")) 
        idx = len(resp_df)

    except: # if not, create one (this happens the first time)
        empty = pd.DataFrame().assign(Language=None, Speaker=None, Word_count = None,Syllable_count = None,Phoneme_count = None, annotate_date_YYYYMMDD=None, Clip = None,ActualClip=None ) 
        empty.to_csv(os.path.join(outdir, annotator_name+"_"+USER_INP+"_responses.csv"), index=False) 
        resp_df = pd.read_csv(os.path.join(outdir, annotator_name+"_"+USER_INP+"_responses.csv")) 

    createRandomizationOrder()


def close_window(annotate):
    annotate.destroy()

    tk.Label(annotate, text="What is your name?").grid(row=0)
    name = tk.Entry(annotate)
    def return_name():
        global content
        content = name.get()
    name.grid(row=0, column=1)


    tk.Button(annotate, text="Enter", command=combine_funcs(return_name, partial(close_window, annotate))).grid(row=7,column=1,columnspan=2)


    #index and play audio file aloud
def play_audio():
    global row
    global audiofile
    global file_name

    file_name = allfilenames[idx]
    lastunderscore = file_name.rfind('_')
    file_name = file_name[0:4] + "_xxxx_" +file_name[lastunderscore+1:]

    #idfolder = file_name[0:4]
    audiofile = os.path.join(clipfolder, USER_INP, file_name)
    subprocess.check_call(['open', '-a', 'Quicktime Player', audiofile])

#go to the next audio file 
def next_audio():
    global row
    global resp_df
    global idx

    language = langcategory.get() # get the language classification
    speaker = scategory.get() # get the speaker classification
    word_count = wcategory.get() 
    syll_count = sylcategory.get()
    phon_count = phcategory.get()

    annotate_date_YYYYMMDD = datetime.datetime.now() # get current annotation time

    allcols = pd.DataFrame([row]).assign(Language=language, Speaker=speaker, Word_count = word_count,Syllable_count = syll_count,Phoneme_count = phon_count, annotate_date_YYYYMMDD=annotate_date_YYYYMMDD, Clip = file_name, ActualClip = actualnames[idx]) 
    resp_df = pd.concat([resp_df, allcols]) # append new records in old csv
    resp_df.to_csv(os.path.join(outdir, annotator_name+"_"+USER_INP+"_responses.csv"), index=False)  # overwrite responses.csv each time  

    idx += 1 # update the global idx

    if idx>=len(allfilenames):
        tk.messagebox.showinfo(title='Alert', message='All clips have been annotated. Please close the app now! Restart to start with a new CHILD ID')
    else:
        play_audio()


def repeat():
    subprocess.check_call(['open', '-a', 'Quicktime Player', audiofile])

def main():
    global langcategory
    global scategory
    global mediacat
    global wcategory
    global phcategory
    global sylcategory

    root = tk.Tk() # refers to annotation window 

    root.update()

    root.title("Bolivia Data - ALICE Performance Testing")

    frame = tk.Frame(root, bg="white")
    frame.grid(row=8, column=8)

    langcategory = tk.StringVar() 
    scategory = tk.StringVar()
    phcategory = tk.StringVar()
    sylcategory = tk.StringVar()
    wcategory = tk.StringVar()
   

    langcategory.set("Categorize language")
    scategory.set("Categorize speaker")
    phcategory.set("Count no of phonemes")
    sylcategory.set("Count no of syllables")
    wcategory.set("Count no of words")


    popupMenu = tk.OptionMenu(frame, langcategory, *LANG_VALUES)
    popupMenu2 = tk.OptionMenu(frame, scategory, *SPEAKER_VALUES)
    popupMenu3 = tk.OptionMenu(frame, phcategory, *NUM_VALUES)
    popupMenu4 = tk.OptionMenu(frame, sylcategory, *NUM_VALUES)
    popupMenu5 = tk.OptionMenu(frame, wcategory, *NUM_VALUES)

    popupMenu.grid(row=4, column=1)
    popupMenu2.grid(row=5, column=1)
    popupMenu3.grid(row=6, column=1)
    popupMenu4.grid(row=7, column=1)
    popupMenu5.grid(row=8, column=1)

    tk.Label(frame, text="Language: ").grid(row = 4, column = 0)
    tk.Label(frame, text="Speaker: ").grid(row = 5, column = 0)
    tk.Label(frame, text="No. of phonemes: ").grid(row = 6, column = 0)
    tk.Label(frame, text="No. of syllables: ").grid(row = 7, column = 0)
    tk.Label(frame, text="No. of words: ").grid(row = 8, column = 0)

    mediacat = tk.IntVar()
 
    tk.Button(frame, text="   Play   ", command=combine_funcs(play_audio, clear), bg="gray").grid(row=1, column=0) 

    tk.Button(frame, text="  Save and next   ", command=combine_funcs(next_audio, clear), bg="gray").grid(row=1, column=2) 

    tk.Button(frame, background="gray", text="   Repeat   ", command=repeat).grid(row=1, column=1)

    annotatorinfo()
    
    root.mainloop()  

if __name__ == "__main__":
    main()