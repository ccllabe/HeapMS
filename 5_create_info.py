#!/usr/bin/python
from os import listdir
from os.path import isfile, isdir, join
from os import walk

import os
import shutil
import csv
import numpy as np
import sys
import time

def csvinfo(peak,txtfolder):
    all_file=[]
    with open(peak, newline='',encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        #skip 1st row of csv
        next(rows)
        for row in rows:
            name=row[0]
            peptide=row[1]
            isotope_type=row[7]
            start_time=row[2]
            end_time=row[3]
            all_file.append([name+"-..-"+peptide+"_"+isotope_type+".txt",start_time,end_time])  
    return all_file

#######  main   ##############
import time

start=time.time()
print("code 5 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("5_create_info.py",time.ctime(start)))
    f.close()

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    peak=sys.argv[1]+"/"+sys.argv[2]+"/human.csv"     #人工匡選
else:
    peak=sys.argv[1]+"/"+sys.argv[2]+"/skyline.csv"

peak_skyline=sys.argv[1]+"/"+sys.argv[2]+"/skyline.csv"

txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"


####以下不用參數不用修改

allfile_human=csvinfo(peak,txtfolder)
print(np.shape(allfile_human))
name_human=np.array(allfile_human)[:,0]

allfile_skyline=csvinfo(peak_skyline,txtfolder)
print(np.shape(allfile_skyline))
name_skyline=np.array(allfile_skyline)[:,0]

uniques_skyline = np.unique(name_skyline)



png_num=0  #png_name init
file_num=0 #num of png
no_RQ=0

'''
if not os.path.exists(txtfolder+"/notinskyline_txt"):
    os.makedirs(txtfolder+"/notinskyline_txt")
    os.chmod(txtfolder+"/notinskyline_txt", 0o777)
if not os.path.exists(txtfolder+"/NA_notinskyline_txt"):
    os.makedirs(txtfolder+"/NA_notinskyline_txt")
    os.chmod(txtfolder+"/NA_notinskyline_txt", 0o777)    
'''
if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    # 列出目錄txtfolder的所有檔案
    for root, dirs, files in walk(txtfolder):
        print(root)
        #把比對不上的資料（在human.csv卻沒有在skyline.csv中的txt）移到/notinskyline   &&  移除對不上的資料後 把可用的資訊加入info.txt
        if root==txtfolder:
            files.sort()
            ### explain:some_list[start:stop:step]
            files=files[1::2]
            file_num=len(files)
            files=np.array(files)
            ###create info.txt
            fo = open(txtfolder+"_info.txt", "w")
            os.chmod(txtfolder+"_info.txt", 0o777)
            fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format("ori_name","png_name","h_ini","h_end","s_ini","s_end"))
            for name in files:
                png_name="%06d"%png_num+".png"
                #print(png_name)
                index_human=np.where(name_human==name)[0][0]
                human_start=allfile_human[index_human][1]
                human_end=allfile_human[index_human][2]
            
                index_skyline=np.where(name_skyline==name)[0][0]
                skyline_start=allfile_skyline[index_skyline][1]
                skyline_end=allfile_skyline[index_skyline][2]
                                   
                png_num+=1
                fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format(name,png_name,str(human_start),str(human_end),str(skyline_start),str(skyline_end)))

elif not os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    # 列出目錄txtfolder的所有檔案
    for root, dirs, files in walk(txtfolder):
        print(root)
        #把比對不上的資料（在human.csv卻沒有在skyline.csv中的txt）移到/notinskyline   &&  移除對不上的資料後 把可用的資訊加入info.txt
        if root==txtfolder:
            files.sort()
            ### explain:some_list[start:stop:step]
            files=files[1::2]
            file_num=len(files)
            files=np.array(files)
            ###create info.txt
            fo = open(txtfolder+"_info.txt", "w")
            os.chmod(txtfolder+"_info.txt", 0o777)
            fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format("ori_name","png_name","s_ini","s_end","s_ini","s_end"))

            for name in files:
                for i in range(len(uniques_skyline)):
                    if name==uniques_skyline[i]:
                        png_name="%06d"%png_num+".png"
                        
                        index_skyline=np.where(name_skyline==uniques_skyline[i])[0][0]
                        skyline_start=allfile_skyline[index_skyline][1]
                        skyline_end=allfile_skyline[index_skyline][2]
                        
                        png_num+=1
                        fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format(name,png_name,str(skyline_start),str(skyline_end),str(skyline_start),str(skyline_end)))      

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    txtfolder_remove=txtfolder+"_remove_NA"
    for root, dirs, files in walk(txtfolder_remove):
        if root==txtfolder_remove:
            print(root)
            files.sort()
            files=files[1::2]
            files=np.array(files)
            for name in files:
                png_name="%06d"%png_num+".png"
                index_human=np.where(name_human==name)[0][0]
                human_start=allfile_human[index_human][1]
                human_end=allfile_human[index_human][2]
            
                index_skyline=np.where(name_skyline==name)[0][0]
                skyline_start=allfile_skyline[index_skyline][1]
                skyline_end=allfile_skyline[index_skyline][2]
                png_num+=1
                if(skyline_start=="#N/A"):
                    fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format(name,png_name,"NA","NA","NA","NA"))
                else:
                    fo.writelines("{}\t{}\t{}\t{}\t{}\t{}\n".format(name,png_name,"NA","NA",str(skyline_start),str(skyline_end)))

txtfolder_skyline_remove=txtfolder+"_skyline_remove_NA"
for root, dirs, files in walk(txtfolder_skyline_remove):
    if root==txtfolder_skyline_remove:
        print(root)
        files.sort()
        files=files[1::2]
        files=np.array(files)
        for name in files:
            no_RQ+=1        
        fo.close()
print("skyline NA so can not calculate RQ:{}".format(no_RQ))
end=time.time()
print("5_create_info.py use {} seconds.".format(end-start))

