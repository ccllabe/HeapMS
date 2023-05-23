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

def csvinfo(peak):
    all_file=[['name','start','end','transition']]
    #all_file=[['name','start','end','precursor','fragment','product']]
    with open(peak, newline='',encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        #skip 1st row of csv
        next(rows)
        for row in rows:
            name=row[0]
            peptide=row[1]
            start_time=row[2]
            end_time=row[3]
            precursor=row[4]
            fragment=row[5]
            isotope_type=row[7]
            
            all_file.append([name+"-..-"+peptide+"_"+isotope_type+".txt",start_time,end_time,precursor+"&"+fragment])    
    return all_file   
#######  main   ##############
import time

start=time.time()
print("code 3 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("3_rm_csv_notmatch.py",time.ctime(start)))
    f.close()

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    ##parameter
    peak=sys.argv[1]+"/"+sys.argv[2]+"/human.csv"     #人工匡選

    peak_skyline=sys.argv[1]+"/"+sys.argv[2]+"/skyline.csv"

    txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"


    ####以下不用參數不用修改

    allfile_human=csvinfo(peak)
    print(np.shape(allfile_human))
    name_human=np.array(allfile_human)[:,0]
    transition_human=np.array(allfile_human)[:,3]
    allfile_skyline=csvinfo(peak_skyline)
    print(np.shape(allfile_skyline))
    name_skyline=np.array(allfile_skyline)[:,0]
    transition_skyline=np.array(allfile_skyline)[:,3]

    mvlist=[]

    if not os.path.exists(txtfolder+"/notmatch_txt"):
        os.makedirs(txtfolder+"/notmatch_txt")
        os.chmod(txtfolder+"/notmatch_txt", 0o777)
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
            count=0
            for name in files:
                print(count)
                count+=1
                file=open(txtfolder+"/"+name,'r')
                list_all=file.readlines()
                #list_all[0/3/6]:ion ,list_all[1/4/7]:time ,list_all[2/5/8]:intensity
                #transition_r=np.array(list_all[0].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
                transition_r=list_all[0].split("\n")[0][:-2]
                transition_g=list_all[3].split("\n")[0][:-2]
                transition_b=list_all[6].split("\n")[0][:-2]
                #print(transition_r,transition_g,transition_b)
                file.close()
            
            
                find=0
                #找出每張色譜圖的檔名name與transition 確認色譜圖的3種transition 在human.csv中是否都有符合的一列
                find_name_idx=np.where(name_human==name)[0]
                find_transition=transition_human[find_name_idx]
                find_idx_r=np.where(find_transition==transition_r)[0]
                find_idx_g=np.where(find_transition==transition_g)[0]
                find_idx_b=np.where(find_transition==transition_b)[0]
                #find_idx_r=np.where(np.logical_and(name_human==name,transition_human==transition_r))[0]
                #find_idx_g=np.where(np.logical_and(name_human==name,transition_human==transition_g))[0]
                #find_idx_b=np.where(np.logical_and(name_human==name,transition_human==transition_b))[0]
                #if(len(np.where(name_human==name)[0])==3):
                if(len(find_idx_r)!=0 and len(find_idx_g)!=0 and len(find_idx_b)!=0):
                    find+=1
            
                #找出每張色譜圖的檔名name與transition 確認色譜圖的3種transition 在human.csv中是否都有符合的一列
                find_name_idx=np.where(name_skyline==name)[0]
                find_transition=transition_skyline[find_name_idx]
                find_idx_r=np.where(find_transition==transition_r)[0]
                find_idx_g=np.where(find_transition==transition_g)[0]
                find_idx_b=np.where(find_transition==transition_b)[0]
            
                #find_idx_r=np.where(np.logical_and(name_skyline==name,transition_skyline==transition_r))[0]
                #find_idx_g=np.where(np.logical_and(name_skyline==name,transition_skyline==transition_g))[0]
                #find_idx_b=np.where(np.logical_and(name_skyline==name,transition_skyline==transition_b))[0]
                #if(len(np.where(name_skyline==name)[0])==3):
                if(len(find_idx_r)!=0 and len(find_idx_g)!=0 and len(find_idx_b)!=0):
                    find+=1
                if(find!=2):  #skyline.csv human.csv 至少一個找不到符合name,peptide,light/heavy的欄位
                    print(name)
                    mvlist.append(name)
            
        else: 
            continue
    print(len(mvlist))

    for mvname in mvlist:
        shutil.move(txtfolder+'/'+mvname,txtfolder+'/notmatch_txt/'+mvname)
        shutil.move(txtfolder+'/'+mvname[:-10]+'_heavy.txt',txtfolder+'/notmatch_txt/'+mvname[:-10]+'_heavy.txt')
           
        
end=time.time()
print("3_rm_csv_notmatch.py use {} seconds.".format(end-start))
