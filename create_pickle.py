# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 08:58:27 2022

@author: srira
"""
""" This is to create pickle files to for train,test and val splits """


import pickle 
files=['44856031_0d82c2c7d1',
'47870024_73a4481f7d',
'47871819_db55ac4699']
athletes_file = open('filename.pickle', 'wb')

pickle.dump(files, athletes_file)
athletes_file.close()

# Read pickle file
athletes_file = open(r"C:\Users\srira\Desktop\Final testing\Data_for_SAS\test\filenames.pickle", "rb")
athletes = pickle.load(athletes_file)
cnt = 0
for item in athletes:
    print('The data ', cnt, ' is : ', item)
    cnt += 1
    
athletes_file.close()
# =============================================================================
# 
# =============================================================================
import glob
path=r"C:\Users\srira\Desktop\temppp\500\test\*"
filenames = glob.glob(path)
text="C:\\Users\\srira\\Desktop\\temppp\\500\\test\\"
files=[i.replace(text,'') for i in filenames]
files=[i.replace(".npy",'') for i in files]
athletes_file = open('filenames.pickle', 'wb')
pickle.dump(files, athletes_file)
athletes_file.close()