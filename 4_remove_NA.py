#!/usr/bin/python
import os
import time
import csv
import shutil
import sys

start=time.time()
print("code 4 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("4_remove_NA.py",time.ctime(start)))
    f.close()


txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    folder= txtfolder+"_remove_NA"
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chmod(folder, 0o777)
    with open(sys.argv[1]+"/"+sys.argv[2]+"/human.csv", newline='',encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)
        for row in rows:
            if row[2]=='#N/A' or row[3]=='#N/A':
                file_light = row[0]+'-..-'+row[1]+'_light.txt'
                file_heavy = row[0]+'-..-'+row[1]+'_heavy.txt'
                if os.path.isfile(txtfolder+"/"+file_light):
                    shutil.move(txtfolder+"/"+file_light,folder+"/"+file_light)
                if os.path.isfile(txtfolder+"/"+file_heavy):
                    shutil.move(txtfolder+"/"+file_heavy,folder+"/"+file_heavy)

folder_skyline= txtfolder+"_skyline_remove_NA"
if not os.path.exists(folder_skyline):
    os.makedirs(folder_skyline)
    os.chmod(folder_skyline, 0o777)       
with open(sys.argv[1]+"/"+sys.argv[2]+"/skyline.csv", newline='',encoding='utf8') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    for row in rows:
        if row[2]=='#N/A' or row[3]=='#N/A':
            file_light = row[0]+'-..-'+row[1]+'_light.txt'
            file_heavy = row[0]+'-..-'+row[1]+'_heavy.txt'
            if os.path.isfile(txtfolder+"/"+file_light):
                shutil.move(txtfolder+"/"+file_light,folder_skyline+"/"+file_light)
            if os.path.isfile(txtfolder+"/"+file_heavy):
                shutil.move(txtfolder+"/"+file_heavy,folder_skyline+"/"+file_heavy)
                               
end=time.time()
print("4_remove_NA.py use {} seconds.".format(end-start))

