#!/usr/bin/python
import xml.etree.cElementTree as ET
import math
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
import pylab as pl
from scipy.signal import savgol_filter
import shutil
import sys

def fileinfo(txtfolder):
    allfile=[]
    #allfile=[['name','start','end']]
    with open(txtfolder+"_info.txt") as f:
       for line in f:
           name=line.split("\t")[0].strip()       
           
           #skip 1st row
           if name=="ori_name":
               continue
           #start_human=float(line.split("\t")[2])
           #end_human=float(line.split("\t")[3])
           #start_skyline=float(line.split("\t")[4])
           #end_skyline=float(line.split("\t")[5])
           #allfile.append([name,start_human,end_human,start_skyline,end_skyline])
           
           #allfile.append(name)
           
           start_human=line.split("\t")[2]
           end_human=line.split("\t")[3]
           start_skyline=line.split("\t")[4]
           end_skyline=line.split("\t")[5]
           allfile.append([name,start_human,end_human,start_skyline,end_skyline])
           if 'str' in line:	
              break
    print(allfile)
    return allfile

def selefile(all_file,txtfolder,minpeakrate,peak_limit,rmse_limit,smooth_limit,tol):
    iteration=np.shape(np.array(all_file))[0] 
    #iteration=len(all_file) 
    for i in range(iteration):
        imagename="%06d"%i
        print(imagename)
        if os.path.isfile(txtfolder+'/'+all_file[i][0]):
        #if os.path.isfile(txtfolder+'/'+all_file[i]):
            ##get time 取得mass時間軸(資料加倍後)
            time=gettime(txtfolder+'/'+all_file[i][0])
            #time=gettime(txtfolder+'/'+all_file[i])
            
            #list_rgb[0]:light ,list_rgb[1]:heavy  
            #list_rgb[i][0]:R,list_rgb[i][0]:G,list_rgb[i][0]:B,
            list_rgb=getlist(txtfolder+'/'+all_file[i][0])
            #list_rgb=getlist(txtfolder+'/'+all_file[i])
            
            #找出minvalue_light/heavy用作小範圍平滑前的負值修正
            minvalue_light=np.amin([np.amin(list_rgb[0][0]),np.amin(list_rgb[0][1]),np.amin(list_rgb[0][2])]) 
            #print("minvalue_light {:.3f}".format(minvalue_light))
            minvalue_heavy=np.amin([np.amin(list_rgb[1][0]),np.amin(list_rgb[1][1]),np.amin(list_rgb[1][2])])
            #print("minvalue_heavy {:.3f}".format(minvalue_heavy))
          
            list_rgb_savgol=np.zeros(np.shape(list_rgb))
            #smooting Savitzky–Golay filter
            #big framelen smoothing 大範圍 取波形趨勢
            list_rgb_savgol[0][0]= savgol_filter(list_rgb[0][0], 15, 3)
            list_rgb_savgol[0][1]= savgol_filter(list_rgb[0][1], 15, 3)
            list_rgb_savgol[0][2]= savgol_filter(list_rgb[0][2], 15, 3)
            list_rgb_savgol[1][0]= savgol_filter(list_rgb[1][0], 15, 3)
            list_rgb_savgol[1][1]= savgol_filter(list_rgb[1][1], 15, 3)
            list_rgb_savgol[1][2]= savgol_filter(list_rgb[1][2], 15, 3)
            
            
            #合併list後取amax(最終採三個list分別取amax 在比較三個結果取最大值)
            minpeakvalue_light=np.max([np.amax(list_rgb_savgol[0][0]),np.amax(list_rgb_savgol[0][1]),np.amax(list_rgb_savgol[0][2])])*minpeakrate
            minpeakvalue_heavy=np.max([np.amax(list_rgb_savgol[1][0]),np.amax(list_rgb_savgol[1][1]),np.amax(list_rgb_savgol[1][2])])*minpeakrate
            
            #count peak
            cpeak=[[0,0,0],[0,0,0]]
            cpeak[0][0]=count_peak(list_rgb_savgol[0][0],time,minpeakvalue_light)
            cpeak[0][1]=count_peak(list_rgb_savgol[0][1],time,minpeakvalue_light)
            cpeak[0][2]=count_peak(list_rgb_savgol[0][2],time,minpeakvalue_light)
            cpeak[1][0]=count_peak(list_rgb_savgol[1][0],time,minpeakvalue_heavy)
            cpeak[1][1]=count_peak(list_rgb_savgol[1][1],time,minpeakvalue_heavy)
            cpeak[1][2]=count_peak(list_rgb_savgol[1][2],time,minpeakvalue_heavy)
            
            #small framelen smoothing 小範圍 去噪 先將強度平方(可能太多次會overflow)再平滑 最多平滑6次
            smooth_count=[1,1]
            minvalue=[minvalue_light,minvalue_heavy]
            #minvalue=[minpeakvalue_light,minpeakvalue_heavy]
            for j in range(2):
                framelen=5
                #平滑前把<0的部份設為原波形最小值minvalue[j] 
                list_rgb_savgol[j][0][list_rgb_savgol[j][0]<0]=minvalue[j]
                list_rgb_savgol[j][1][list_rgb_savgol[j][1]<0]=minvalue[j]
                list_rgb_savgol[j][2][list_rgb_savgol[j][2]<0]=minvalue[j]
                
                minpeakvalue=np.amax([np.amax(list_rgb_savgol[j][0]),np.amax(list_rgb_savgol[j][1]),np.amax(list_rgb_savgol[j][2])])*minpeakrate
                
                while cpeak[j][0]>3 or cpeak[j][1]>3 or cpeak[j][2]>3:   
                    #print("lr argmax:{:.3f}".format(np.amax(list_rgb_savgol[j][0])))
                    
                    if smooth_count[j]>=15:
                        break
                    smooth_count[j]+=1
                    
                    #print("smoothing framelen={}".format(framelen))     
                    #print(cpeak[j][0])     
                    #print(cpeak[j][1])     
                    #print(cpeak[j][2])      
                    list_rgb_savgol[j][0]= savgol_filter(list_rgb_savgol[j][0]*1.2,framelen,3)
                    list_rgb_savgol[j][1]= savgol_filter(list_rgb_savgol[j][1]*1.2,framelen,3)
                    list_rgb_savgol[j][2]= savgol_filter(list_rgb_savgol[j][2]*1.2,framelen,3)
                    
                    #20210305 reset minpeakvalue & conut peak after smooting
                    minpeakvalue=np.amax([np.amax(list_rgb_savgol[j][0]),np.amax(list_rgb_savgol[j][1]),np.amax(list_rgb_savgol[j][2])])*minpeakrate
                    
                    
                    #conut peak after smooting
                    cpeak[j][0]=count_peak(list_rgb_savgol[j][0],time,minpeakvalue)
                    cpeak[j][1]=count_peak(list_rgb_savgol[j][1],time,minpeakvalue)
                    cpeak[j][2]=count_peak(list_rgb_savgol[j][2],time,minpeakvalue)
                #print("smooth {:d} th".format(smooth_count[j]))    
                

            #找出多數peak的共同時間座標
            #mainpeak=find_mainpeak(list_rgb_savgol,time)
            
            peak_all=[]
            peak_lr=peaktime(list_rgb_savgol[0][0],time)
            peak_all+=peak_lr
            peak_lg=peaktime(list_rgb_savgol[0][1],time)
            peak_all+=peak_lg
            peak_lb=peaktime(list_rgb_savgol[0][2],time)
            peak_all+=peak_lb
            peak_hr=peaktime(list_rgb_savgol[1][0],time)
            peak_all+=peak_hr
            peak_hg=peaktime(list_rgb_savgol[1][1],time)
            peak_all+=peak_hg
            peak_hb=peaktime(list_rgb_savgol[1][2],time)
            peak_all+=peak_hb
            #print(peak_all)
           
            #uniwq:去除重複結果 inverse:各元素出現次數
            uniqw, inverse = np.unique(np.array(peak_all), return_inverse=True)
            #print(uniqw)
            #print(np.bincount(inverse))
            ind=np.argmax(np.bincount(inverse))
            peak_most=uniqw[ind]
            
            #判斷peak_XX中是否有任何一個peak（使用any()）很接近peak_most
            tol=0.3
            flag_lr=np.isclose(peak_lr,peak_most,atol=tol).any()
            flag_lg=np.isclose(peak_lg,peak_most,atol=tol).any()
            flag_lb=np.isclose(peak_lb,peak_most,atol=tol).any()
            flag_hr=np.isclose(peak_hr,peak_most,atol=tol).any()
            flag_hg=np.isclose(peak_hg,peak_most,atol=tol).any()
            flag_hb=np.isclose(peak_hb,peak_most,atol=tol).any()
            
        
        
        
        
            #### 波形相似度 rmse F1計算 OK ##################       
            ##calrmse
            rmse=[0,0,0]
            rmse[0]=np.sqrt(np.mean((list_rgb_savgol[0][0]/np.amax(list_rgb_savgol[0][0])-list_rgb_savgol[1][0]/np.amax(list_rgb_savgol[1][0]))**2))
            rmse[1]=np.sqrt(np.mean((list_rgb_savgol[0][1]/np.amax(list_rgb_savgol[0][1])-list_rgb_savgol[1][1]/np.amax(list_rgb_savgol[1][1]))**2))
            rmse[2]=np.sqrt(np.mean((list_rgb_savgol[0][2]/np.amax(list_rgb_savgol[0][2])-list_rgb_savgol[1][2]/np.amax(list_rgb_savgol[1][2]))**2))
            '''
            #skyline region
            hmin=all_file[i][1]
            hmax=all_file[i][2]
            smin=all_file[i][3]
            smax=all_file[i][4]
            
            #cal molecular
            s_sele_t=np.where(np.logical_and(time>=smin, time<=smax))[0]
            riemann_sum_l=0
            riemann_sum_h=0
            for t in s_sele_t:
                riemann_sum_l+=list_rgb[0][0][t]
                riemann_sum_h+=list_rgb[1][0][t]
            
            #print(riemann_sum_l)
            #print(riemann_sum_h)
            molecular_s=riemann_sum_l/riemann_sum_h
            
            h_sele_t=np.where(np.logical_and(time>=hmin, time<=hmax))[0]
            riemann_sum_l=0
            riemann_sum_h=0
            for t in h_sele_t:
                riemann_sum_l+=list_rgb[0][0][t]
                riemann_sum_h+=list_rgb[1][0][t]
            #print(riemann_sum_l)
            #print(riemann_sum_h)
            molecular_h=riemann_sum_l/riemann_sum_h
            
            #print("skyline {:.3f}".format(molecular_s))
            #print("human {:.3f}".format(molecular_h))
            #print("###")
                
            #cal f1
            F1_score=calf1(time,hmin,hmax,smin,smax)
            '''
            ##### 顯示文字資訊OK ###################   
            flag_peaknum=cpeak[0][0]<peak_limit and cpeak[0][1]<peak_limit and cpeak[0][2]<peak_limit and cpeak[1][0]<peak_limit and cpeak[1][1]<peak_limit and cpeak[1][2]<peak_limit    
            flag_mainpeak=flag_lr and flag_lg and flag_lb and flag_hr and flag_hg and flag_hb
            flag_rmse=rmse[0]<rmse_limit and rmse[1]<rmse_limit and rmse[2]<rmse_limit
            
            '''       
            ##add plt information
            fig,axs=plt.subplots(4,figsize=(12, 12))
            ###light ori.
            axs[0].plot(time,list_rgb[0][0], color='#ffb3b3')
            axs[0].plot(time,list_rgb[0][1], color='#b3ffb3')
            axs[0].plot(time,list_rgb[0][2], color='#b3b3ff')
            ###heavy ori.
            axs[2].plot(time,list_rgb[1][0], color='#ffb3b3')
            axs[2].plot(time,list_rgb[1][1], color='#b3ffb3')
            axs[2].plot(time,list_rgb[1][2], color='#b3b3ff')
            ###light smooting
            axs[1].plot(time,list_rgb_savgol[0][0], color='red')
            axs[1].plot(time,list_rgb_savgol[0][1], color='green')
            axs[1].plot(time,list_rgb_savgol[0][2], color='blue')
            ###heavy smooting
            axs[3].plot(time,list_rgb_savgol[1][0], color='red')
            axs[3].plot(time,list_rgb_savgol[1][1], color='green')
            axs[3].plot(time,list_rgb_savgol[1][2], color='blue')
            for k in range(4):
                axs[k].axvline(x=hmin,color="#ff99ff",alpha=0.5)
                axs[k].axvline(x=hmax,color="#ff99ff",alpha=0.5)
                axs[k].axvline(x=smin,color="#99ffff",alpha=0.5)
                axs[k].axvline(x=smax,color="#99ffff",alpha=0.5)
            axs[0].text(time[0], np.amax(list_rgb[0])*0.6,'main peak:{:.3f} flag_mainpeak:{} tol:{:.1f}\nrmse_r:{:.3f} rmse_g:{:.3f} rmse_b:{:.3f}\nflag_rmse:{}\nF1:{:.3f} \nlight: \nr_peak:{:d} g_peak:{:d} b_peak:{:d} \nlight_smooth {:d} th\nheavy: \nr_peak:{:d} g_peak:{:d} b_peak:{:d}\nheavy_smooth {:d} th\nflag_peak:{}'.format(peak_most,flag_mainpeak,tol,rmse[0],rmse[1],rmse[2],flag_rmse, F1_score,cpeak[0][0],cpeak[0][1],cpeak[0][2],smooth_count[0],cpeak[1][0],cpeak[1][1],cpeak[1][2],smooth_count[1],flag_peaknum),fontsize=8, color='black')
            '''                      
            #篩選條件 (1)rmse都小於0.3 因為完美波形的rmse約為0.25 (2)peak數都小於2 
            peak_limit=2
            if flag_rmse and flag_peaknum and flag_mainpeak:
                #完美波形的txt搬到 /low_interference(skyline good)
                #plt.savefig(txtfolder+'/low_interference/ori_image/'+imagename,bbox_inches='tight',dpi=100,pad_inches=0)
                shutil.move(txtfolder+'/'+all_file[i][0],txtfolder+'/low_interference/txt/'+all_file[i][0])
                #shutil.move(txtfolder+'/'+all_file[i],txtfolder+'/low_interference/txt/'+all_file[i])
                shutil.move(txtfolder+'/'+all_file[i][0][:-10]+'_heavy.txt',txtfolder+'/low_interference/txt/'+all_file[i][0][:-10]+'_heavy.txt')
                #shutil.move(txtfolder+'/'+all_file[i][:-10]+'_heavy.txt',txtfolder+'/low_interference/txt/'+all_file[i][:-10]+'_heavy.txt')
                
            else:
                #其他txt搬到 /high_interference(skyline bad)
                #plt.savefig(txtfolder+'/high_interference/ori_image/'+imagename,bbox_inches='tight',dpi=100,pad_inches=0) 
                shutil.move(txtfolder+'/'+all_file[i][0],txtfolder+'/high_interference/txt/'+all_file[i][0])
                #shutil.move(txtfolder+'/'+all_file[i],txtfolder+'/high_interference/txt/'+all_file[i])
                shutil.move(txtfolder+'/'+all_file[i][0][:-10]+'_heavy.txt',txtfolder+'/high_interference/txt/'+all_file[i][0][:-10]+'_heavy.txt')
                #shutil.move(txtfolder+'/'+all_file[i][:-10]+'_heavy.txt',txtfolder+'/high_interference/txt/'+all_file[i][:-10]+'_heavy.txt')
                
                #shutil.move(peptide+'/'+all_file[i][0]+'-..-'+peptide+'_light.txt',peptide+'/other_txt/'+all_file[i][0]+'-..-'+peptide+'_light.txt')
                #shutil.move(peptide+'/'+all_file[i][0]+'-..-'+peptide+'_heavy.txt',peptide+'/other_txt/'+all_file[i][0]+'-..-'+peptide+'_heavy.txt')           
            plt.close()    
        else:
            print('not found')
  
def count_peak(list_rgb,time,minvalue):
    num=len(time)
    pre_slope=1
    peak=0
    for k in range(num-1):
        slope=(list_rgb[k+1]-list_rgb[k])/(time[k+1]-time[k])
        #if list_rgb[k]>np.amax(list_rgb)/10 and pre_slope>0 and slope<0:
        if list_rgb[k]>minvalue and pre_slope>0 and slope<0:
            peak+=1
            #print(time[k])
        pre_slope=slope
    cpeak=peak

    return cpeak
    
def peaktime(list_rgb,time):
    num=len(time)
    pre_slope=1
    peaktime=[]
    for k in range(num-1):
        slope=(list_rgb[k+1]-list_rgb[k])/(time[k+1]-time[k])
        if list_rgb[k]>np.amax(list_rgb)/10 and pre_slope>0 and slope<0:
            peaktime.append(time[k])
        pre_slope=slope
        
    return peaktime   
         
def arr_extend(r,num):  ###增加資料量為num倍
    for j in range(num-1):
        tmp=[]
        tmp.append(r[0])
        for i in range(len(r)-1):
            tmp.append((r[i]+r[i+1])/2)
            tmp.append(r[i+1])
        r=tmp
    return r
'''
def calf1(time,hmin,hmax,smin,smax):
    TP=0
    TN=0
    FP=0
    FN=0
    ###note:此處的f1只計算小數點2位 有誤差
    frange=np.arange(round(time[0],2),round(time[-1],2),0.01)
    for t in frange:
        #print(t)
        if (t >= smin and t <=smax) and (t >= hmin and t <=hmax):
            #print("TP+=1")
            TP+=1         
        elif (t >= smin and t <=smax) and not(t >= hmin and t <=hmax):
            #print("FP+=1")
            FP+=1         
        elif not(t >= smin and t <=smax) and (t >= hmin and t <=hmax):
            #print("FN+=1")
            FN+=1         
        else:
            #print("TN+=1")
            TN+=1         

    F1_score=(2*TP)/(2*TP+FP+FN)
    return F1_score
'''    
    
def gettime(filename):  #取得mass時間軸(資料加倍後)
    file=open(filename,'r')
    list_all=file.readlines()
    #list_r=list_all[0].split("\t")
    #time=np.array(list_r[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    time=np.array(list_all[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    #time=arr_extend(time,3)
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
    
    #lr=arr_extend(lr,3)
    #lg=arr_extend(lg,3)
    #lb=arr_extend(lb,3)
    #hr=arr_extend(hr,3)
    #hg=arr_extend(hg,3)
    #hb=arr_extend(hb,3)
    
    list_rgb=[[lr,lg,lb],[hr,hg,hb]]
    return list_rgb

#######  main   ##############
#parameter
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

import time
start=time.time()
print("code 7 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("7_sele_perfect_txt.py",time.ctime(start)))
    f.close()

minpeakrate=0.2
peak_limit=2
rmse_limit=0.25
smooth_limit=5
tol=0.15
#print("tol:{:.3f} minpeakrate:{:.3f} rmse_limit:{:.3f} peak_limit:{:d} smooth_limit:{:d}".format(tol,minpeakrate,rmse_limit,peak_limit,smooth_limit))

if not os.path.exists(txtfolder+"/low_interference/txt"):
    os.makedirs(txtfolder+"/low_interference/txt")
    os.chmod(txtfolder+"/low_interference", 0o777)
    os.chmod(txtfolder+"/low_interference/txt", 0o777)
if not os.path.exists(txtfolder+"/high_interference/txt"):
    os.makedirs(txtfolder+"/high_interference/txt")
    os.chmod(txtfolder+"/high_interference", 0o777)
    os.chmod(txtfolder+"/high_interference/txt", 0o777)
'''
if not os.path.exists(txtfolder+"/low_interference/ori_image"):
    os.makedirs(txtfolder+"/low_interference/ori_image")
    os.chmod(txtfolder+"/low_interference/ori_image", 0o777)
if not os.path.exists(txtfolder+"/high_interference/ori_image"):
    os.makedirs(txtfolder+"/high_interference/ori_image")
    os.chmod(txtfolder+"/high_interference/ori_image", 0o777)
'''
all_file=fileinfo(txtfolder)
print(np.shape(all_file))
selefile(all_file,txtfolder,minpeakrate,peak_limit,rmse_limit,smooth_limit,tol)

end=time.time()
print("7_sele_perfect_txt.py use {} seconds.".format(end-start))
