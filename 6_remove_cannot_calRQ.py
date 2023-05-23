#!/usr/bin/python
import os
import numpy as np
import pandas as pd
import shutil
from os import walk
import time
import csv
import sys
import matplotlib.pyplot as plt

def fileinfo(txtfolder):
    allfile=[]
    with open(txtfolder+"_info.txt") as f:
        for line in f:
           name=line.split("\t")[0].strip()                 
           #skip 1st row
           if name=="ori_name":
               continue
           start_human=line.split("\t")[2]
           end_human=line.split("\t")[3]
           start_skyline=line.split("\t")[4]
           end_skyline=line.split("\t")[5].split("\n")[0]
           allfile.append([name,start_human,end_human,start_skyline,end_skyline])     
    return allfile
    
def checker_result(all_file,txtfolder):
    total=0
    
    na=0
    hm=0
    skyline_ok=0
    
    RQ_correct=0
    RQ_error=0
    RQ_denomin_zero=0
        
    iteration=np.shape(np.array(all_file))[0]  ##避免圖片重複 只存peptide,precursor_charge,fragment_ion正確,且為light的資料
    csvcol=["File Name","RQscore"]
    RQ_csv=[]
    score=np.zeros(17, dtype=int)
    folder=txtfolder+'/RQ_cannot_cal'
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chmod(folder, 0o777)
    for i in range(iteration):
        if os.path.isfile(txtfolder+'/'+all_file[i][0]):
            total+=1
            if all_file[i][1]=="NA":
                na+=1
                continue
            hmin=float(all_file[i][1])
            hmax=float(all_file[i][2])
            smin=float(all_file[i][3])
            smax=float(all_file[i][4])
            ##get time 取得mass時間軸(資料加倍後)
            time=gettime(txtfolder+'/'+all_file[i][0])        
            intensity=getlist(txtfolder+'/'+all_file[i][0])
            RQ_score=cal_RQscore(time,intensity,hmin,hmax,smin,smax)
            if(RQ_score==-1 or RQ_score==-2):
                print("filename:{},RQ_score:{}".format(all_file[i][0],RQ_score))
                print("#######################################")
                RQ_denomin_zero+=1
                shutil.move(txtfolder+'/'+all_file[i][0],folder+'/'+all_file[i][0])
                shutil.move(txtfolder+'/'+all_file[i][0][:-10]+'_heavy.txt',folder+'/'+all_file[i][0][:-10]+'_heavy.txt')
                continue
            R_Position=RQ_frequency(RQ_score)
            score[R_Position]+=1
            if(RQ_score>=0.8 and RQ_score<=1.2):
                RQ_correct+=1
            else:                
                RQ_error+=1
            if hmin==smin and hmax==smax:
                skyline_ok+=1
            else:
                hm+=1
                RQ_csv.append([all_file[i][0],RQ_score])
        else:
            print('not found')
    print("total:{},RQ_correct:{},RQ_error:{},csv_RQ_total:{},RQ_denomin_zero:{},HM:{},NA:{},Skyline OK:{}".format(total,RQ_correct,RQ_error,RQ_correct+RQ_error,RQ_denomin_zero,hm-RQ_denomin_zero,na,skyline_ok))
    df_human = pd.DataFrame(RQ_csv,columns=csvcol)
    #df_human = df_human.sort_values(["File Name"], ascending = (False))   
    df_human.to_csv(txtfolder+'_RQ.csv',index = False)
    os.chmod(txtfolder+'_RQ.csv', 0o777)
    
    labels='correct','error','miss deletion'
    size=[RQ_correct,RQ_error,na]
    colors=['#46A3FF','#FF7575','#8E8E8E']
    plt.title('Skyline',fontsize=16)
    patches,l_text,p_text=plt.pie(size,labels=labels,colors=colors,autopct='%1.1f%%',startangle=90)
    for t in p_text:
        t.set_size(10) 
    for t in l_text:
        t.set_size(14)
    plt.axis('equal')
    plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/skyline_pie.png')
    os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/skyline_pie.png', 0o777)
    '''
    ratio=[]
    for s in range(len(score)):
        ratio.append((float(score[s]/(RQ_correct+RQ_error)))*100)
        
    name=['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1','1.1','1.2','1.3','1.4','1.5','>1.5']
    x = np.arange(len(name))
    plt.bar(x, ratio, color='blue')
    plt.xticks(x, name)
    plt.xlabel('AQ')
    plt.ylabel('%')
    plt.title('Skyline')
    plt.text(0.1,np.amax(ratio)*0.9,'Total:{}'.format(RQ_correct+RQ_error),fontsize=8, color='black')
    plt.axvline(7.5,color="#000000",alpha=0.5,ls='dotted')
    plt.axvline(12.5,color="#000000",alpha=0.5,ls='dotted')
    plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/skyline_bar.png')
    os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/skyline_bar.png', 0o777)
    '''
def gettime(filename):  #取得mass時間軸(資料加倍後)
    file=open(filename,'r')
    list_all=file.readlines()
    list_r=list_all[0].split("\t")
    #time=np.array(list_r[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    time=np.array(list_all[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    return time

def getlist(filename): 
    #read light.txt &set time,lr ,lg ,lb value(ion time&intensity)
    file=open(filename,'r')
    list_all=file.readlines()
    #list_all[0/3/6]:ion ,list_all[1/4/7]:time ,list_all[2/5/8]:intensity
    lr=np.array(list_all[2].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    lg=np.array(list_all[5].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    lb=np.array(list_all[8].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    
    file.close()
   
    #read heavy.txt &set lr ,lg ,lb value(ion intensity)
    file=open(filename[:-10]+'_heavy.txt','r')
    list_all=file.readlines()
    
    hr=np.array(list_all[2].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    hg=np.array(list_all[5].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    hb=np.array(list_all[8].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    file.close()
    
    list_rgb=[[lr,lg,lb],[hr,hg,hb]]
    return list_rgb

def cal_RQscore(time,intensity,hmin,hmax,smin,smax):
    #skyline ratio
    s_sele_t=np.where(np.logical_and(time>=smin, time<=smax))[0]
    s_riemann_sum_l=0
    s_riemann_sum_h=0
    for t in s_sele_t:
        s_riemann_sum_l+=intensity[0][0][t]
        s_riemann_sum_h+=intensity[1][0][t]
        #print(intensity[0][0][t])
        #print(intensity[1][0][t])
        #print("---")
    #print(s_riemann_sum_l,s_riemann_sum_h)
    #human ratio
    h_sele_t=np.where(np.logical_and(time>=hmin, time<=hmax))[0]
    h_riemann_sum_l=0
    h_riemann_sum_h=0
    for t in h_sele_t:
        h_riemann_sum_l+=intensity[0][0][t]
        h_riemann_sum_h+=intensity[1][0][t]
        #print(intensity[0][0][t])
        #print(intensity[1][0][t])
        #print("---")
    #print(h_riemann_sum_l,h_riemann_sum_h)
    
    
    if(s_riemann_sum_h==0 or h_riemann_sum_h==0):
        if s_riemann_sum_h==0:
            print("s_riemann_sum_h")
        else:
            print("h_riemann_sum_h")
        print("heavy: ratio denominator is 0!")
        RQ_score=-1
        return RQ_score
    else:
        skyline_ratio=s_riemann_sum_l/s_riemann_sum_h
        human_ratio=h_riemann_sum_l/h_riemann_sum_h
        if(human_ratio==0):
            print("light: RQ_score denominator is 0!")
            RQ_score=-2
            return RQ_score
        else:
            RQ_score=abs(skyline_ratio/human_ratio)
            return RQ_score  
            
def RQ_frequency(RQ_score):
    real_num=float((int(RQ_score*10))/10)
    for i in range(16):
        if real_num==(float(i/10)):
           return i
    if real_num>1.5:
        return 16 
#######  main   ##############
#parameter
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

start=time.time()
print("code 6 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("6_remove_cannot_calRQ.py",time.ctime(start)))
    f.close()

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    txtfolder_remove=txtfolder+"_remove_NA"
    for root, dirs, files in walk(txtfolder_remove):
        if root==txtfolder_remove:
            files=np.array(files)
            for name in files:
                shutil.move(txtfolder_remove+'/'+name,txtfolder+'/'+name)
    shutil.rmtree(txtfolder_remove+'/')

    allfile=fileinfo(txtfolder)
    checker_result(allfile,txtfolder)


end=time.time()
print("6_remove_cannot_calRQ.py use {} seconds.".format(end-start))
