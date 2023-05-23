#!/usr/bin/python
import xml.etree.cElementTree as ET
import math
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import time


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
           start_human=line.split("\t")[2]
           end_human=line.split("\t")[3]
           start_skyline=line.split("\t")[4]
           end_skyline=line.split("\t")[5]
           allfile.append([name,start_human,end_human,start_skyline,end_skyline])
           if 'str' in line:
              break
    return allfile

def getimage(all_file,txtfolder,savefolder):
    #skyline bad產生熱點圖heatmap
    if not os.path.exists(txtfolder+"/high_interference/"+savefolder):
        os.makedirs(txtfolder+"/high_interference/"+savefolder)
        os.chmod(txtfolder+"/high_interference/"+savefolder, 0o777)
    iteration=np.shape(np.array(all_file))[0]  ##避免圖片重複 只存peptide,precursor_charge,fragment_ion正確,且為light的資料
    #draw image
    #for i in range(1250,iteration):
    for i in range(iteration):
        imagename="%06d"%i
        print(imagename)
        if os.path.isfile(txtfolder+'/high_interference/txt/'+all_file[i][0]):
            ##get time 取得mass時間軸(資料加倍後)
            time=gettime(txtfolder+'/high_interference/txt/'+all_file[i][0])
            #建立result,result_mask
            num=len(time)
            arr_size=num*num
            result=getresult(txtfolder+'/high_interference/txt/'+all_file[i][0])
        
            ####draw image  0.png~xxx.png
            heatmap2d(result.astype(int),txtfolder+'/high_interference/'+savefolder+'/'+imagename,'nipy_spectral')
            os.chmod(txtfolder+'/high_interference/'+savefolder+'/'+imagename+'.png', 0o777)
            print('OK')
        else:
            print('not found')
def heatmap2d(arr: np.ndarray,path,color):
    plt.figure(figsize = (3.9,3.9))  ###set image size 300*300 ,default=(6.4,4.8)
    #plt.figure() ### image size 不限制
    plt.imshow(arr, cmap=color)
    plt.axis('off')
    plt.savefig(path,bbox_inches='tight',dpi=100,pad_inches=0)  ###調整解析度 預設dpi=100
    plt.show()
    plt.close()

def arr_extend(r,num):  ###增加資料量為num倍
    for j in range(num-1):
        tmp=[]
        tmp.append(r[0])
        for i in range(len(r)-1):
            tmp.append((r[i]+r[i+1])/2)
            tmp.append(r[i+1])
        r=tmp
    return r

def gettime(filename):  #取得mass時間軸(資料加倍後)
    file=open(filename,'r')
    list_all=file.readlines()
    #list_r=list_all[0].split("\t")
    #time=np.array(list_r[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    time=np.array(list_all[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    #time=arr_extend(time,3)
    return time
def getresult(filename): #取得轉換後heatmap(顏色為＃xxxxxx轉decimal後的數值大小)
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
    
    
    lr_max=np.amax(lr)
    lg_max=np.amax(lg)
    lb_max=np.amax(lb)
    hr_max=np.amax(hr)
    hg_max=np.amax(hg)
    hb_max=np.amax(hb)
    

    ###增加lr,lg,lb,hr,hg,hb資料量為3倍

    #num_extend=3
    #lr=arr_extend(lr,num_extend)
    #lg=arr_extend(lg,num_extend)
    #lb=arr_extend(lb,num_extend)
    #hr=arr_extend(hr,num_extend)
    #hg=arr_extend(hg,num_extend)
    #hb=arr_extend(hb,num_extend)
   
    num=len(lr)
    arr_size=num*num
    #result= np.arange(arr_size).reshape(num, num).astype(str)
    result_todecimal=np.arange(arr_size).reshape(num, num).astype(str)
    #set result value
    #import math
    for i in range(num):
        for j in range(num):

            #sol 2.原數據作圖 直接取數值 不轉換＃xxxxxx
            #val_r=(lr[i]/lr_max*1+hr[j]/hr_max*1)*10000
            #val_g=(lg[i]/lg_max*1+hg[j]/hg_max*1)*10000
            #val_b=(lb[i]/lb_max*1+hb[j]/hb_max*1)*10000
            #result_todecimal[i][j]=int(val_r+val_g+val_b)
            
            
            #val_rgb=[val_lr,val_lg,val_lb,val_hr,val_hg,val_hb] 初始設為0 避免計算時lr_max為0報錯 因為出現過強度全部為零的case＝＝
            #最終為val_rgb=[lr[i]/lr_max,lg[i]/lg_max,lb[i]/lb_max,hr[i]/hr_max,hg[i]/hg_max,hb[i]/hb_max]

            val_rgb=[0,0,0,0,0,0]
            if(lr_max!=0.0):
                val_rgb[0]=lr[i]/lr_max
            if(lg_max!=0.0):
                val_rgb[1]=lg[i]/lg_max
            if(lb_max!=0.0):
                val_rgb[2]=lb[i]/lb_max
            if(hr_max!=0.0):
                val_rgb[3]=hr[j]/hr_max
            if(hg_max!=0.0):
                val_rgb[4]=hg[j]/hg_max
            if(hb_max!=0.0):
                val_rgb[5]=hb[j]/hb_max
            #weight_rgb=[w_lr,w_lg,w_lb,w_hr,w_hg,w_hb]
            weight_rgb=[10000,10000,10000,10000,10000,10000]
            
            
            #result=inner product
            result_todecimal[i][j]=int(np.inner(val_rgb,weight_rgb))
    

    return result_todecimal


#######  main   ##############
import time

start=time.time()
print("code 9 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("9_img.py",time.ctime(start)))
    f.close()

##parameter
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

allfile=fileinfo(txtfolder)
getimage(allfile,txtfolder,"image_weight")
   

end=time.time()
print("9_img.py use {} seconds.".format(end-start))
