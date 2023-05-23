#!/usr/bin/python
import cv2
import os
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import sys
import shutil
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def fileinfo(txtfolder):
    allfile=[]
    #allfile=[['name','start','end']]
    with open(txtfolder+"_info.txt") as f:
       for line in f:
           name=line.split("\t")[0].strip()
           #skip 1st row
           if name=="ori_name":
               continue   
           #allfile多讀取newname
           #allfile.append([name,start_human,end_human,start_skyline,end_skyline])
           newname=line.split("\t")[1].strip()

           start_human=line.split("\t")[2]
           end_human=line.split("\t")[3]
           start_skyline=line.split("\t")[4]
           end_skyline=line.split("\t")[5].split("\n")[0]    #因為info.txt每一列結尾的\n須消除
           allfile.append([name,start_human,end_human,start_skyline,end_skyline,newname])
           if 'str' in line:
              break
    return allfile
def get_transition(path):  #取得mass時間軸(資料加倍後)
    file=open(path,'r')
    list_all=file.readlines()
    transition_1=list_all[0][:-1]
    transition_2=list_all[3][:-1]
    transition_3=list_all[6][:-1]
    transition_all=[transition_1,transition_2,transition_3]
    file.close()
    return transition_all
def get_transition_heavy(path):
    file=open(path[:-10]+'_heavy.txt','r')
    list_all=file.readlines()
    transition_1=list_all[0][:-1]
    transition_2=list_all[3][:-1]
    transition_3=list_all[6][:-1]
    transition_all=[transition_1,transition_2,transition_3]
    file.close()
    return transition_all
def gettime(path):  #取得mass時間軸(資料加倍後)
    file=open(path,'r')
    list_all=file.readlines()
    time=np.array(list_all[1].split(",")[:-1]).astype('float64') #[:-1]去除最後的\n
    file.close()
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
    
def plt_image(txtfolder,time,list_rgb,human_start,human_end,skyline_start,skyline_end,model_start,model_end,interference,imagename,model_aq,skyline_aq):
    if not os.path.exists(txtfolder+"/low_interference/error_image"):
        os.makedirs(txtfolder+"/low_interference/error_image")
        os.chmod(txtfolder+"/low_interference/error_image", 0o777)
    if not os.path.exists(txtfolder+"/high_interference/error_image"):
        os.makedirs(txtfolder+"/high_interference/error_image")
        os.chmod(txtfolder+"/high_interference/error_image", 0o777)
    fig,axs=plt.subplots(2,figsize=(12, 12))
    ###light ori.
    axs[0].set_title('light',fontsize=16)
    axs[0].set_xlabel('Time',fontsize=14)
    axs[0].set_ylabel('Intensity',fontsize=14)
    axs[0].plot(time,list_rgb[0][0], color='#ffb3b3')
    axs[0].plot(time,list_rgb[0][1], color='#b3ffb3')
    axs[0].plot(time,list_rgb[0][2], color='#b3b3ff')
    ###heavy ori.
    axs[1].set_title('heavy',fontsize=16)
    axs[1].set_xlabel('Time',fontsize=14)
    axs[1].set_ylabel('Intensity',fontsize=14)
    axs[1].plot(time,list_rgb[1][0], color='#ffb3b3')
    axs[1].plot(time,list_rgb[1][1], color='#b3ffb3')
    axs[1].plot(time,list_rgb[1][2], color='#b3b3ff')
    for k in range(2):
        axs[k].yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,}'.format(int(y))))
        axs[k].tick_params(axis='x', labelsize=14)
        axs[k].tick_params(axis='y', labelsize=14)
        axs[k].axvline(x=float(human_start),color='red',alpha=0.5)
        axs[k].axvline(x=float(human_end),color='red',alpha=0.5)
        axs[k].axvline(x=float(skyline_start),color='blue',alpha=0.5)
        axs[k].axvline(x=float(skyline_end),color='blue',alpha=0.5)
        axs[k].axvline(x=float(model_start),color='#00A600',alpha=0.5)
        axs[k].axvline(x=float(model_end),color='#00A600',alpha=0.5)
    axs[0].text(time[0],np.amax(list_rgb[0])*0.6,'model_AQscore:{}\nskyline_AQscore:{}\n'.format(round(model_aq,2),round(skyline_aq,2)),fontsize=10, color='black')
    if interference=='low':
        plt.savefig(txtfolder+'/low_interference/error_image/'+imagename,bbox_inches='tight',dpi=100,pad_inches=0)
        plt.close()
    elif interference=='high':
        plt.savefig(txtfolder+'/high_interference/error_image/'+imagename,bbox_inches='tight',dpi=100,pad_inches=0)
        plt.close()
        
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
        
def createLabels(data):                   
    for item in data:
        height = item.get_height()
        plt.text(item.get_x()+item.get_width()/2., height*1.05, '%1.1f' % float(height), ha = "center", va = "bottom")
       
def exportcsv(all_file,txtfolder,test_folder,human_csv):
    PATH=txtfolder+"/high_interference/"+test_folder+"/"       
    HM_file = sorted(os.listdir(PATH+"classify_result/image_weight_acce_HM"))  
    #print(HM_file[:5])
    #print(len(HM_file))
         
    AI_file = []  
    human_file = []  
    
    bbox=[]
    with open(PATH+"predict_result/bbox.txt") as f:
       for line in f:
           name=line.split("\t")[0]
           if line.split("\t")[0]=="image_name":
               continue
           elif line.split("\t")[1]=="{:<20}".format(-1):
               human_file.append(name)
               continue
           elif line.split("\t")[1]=="{:<20}".format(-2):
               human_file.append(name)
               continue
           mmin=int((float(line.split("\t")[1])+float(line.split("\t")[2]))/2)
           mmax=int((float(line.split("\t")[3])+float(line.split("\t")[4]))/2)
           AI_file.append(name)
           bbox.append([name,mmin,mmax])
           if 'str' in line:
              break
    bbox=np.array(bbox)
    bbox=bbox[bbox[:,0].argsort()]
    #print(bbox[:5])
    
    #print(AI_file[:5])
    #print(len(AI_file))
    
    #print(human_file[:5])
    #print(len(human_file))
    

    #列出NA品質過低刪除 AI修正 human人工校正的檔案有哪些
    NA_file = sorted(os.listdir(PATH+"classify_result/image_weight_acce_NA"))
    
    #NA_file=NA_file[NA_file.argsort()]
    
    #print(NA_file[:5])
    #print(len(NA_file))
    
    RQ_csv=[]
    all_list=[]
    
    csv_NA=[]
    csv_AI=[]
    csv_human=[]
    
    tsv_NA=[]
    tsv_AI=[]
    tsv_human=[]
    
    score=np.zeros(17, dtype=int)
    score_skyline=np.zeros(17, dtype=int)
    bar_model_correct=0
    bar_model_error=0
    bar_skyline_correct=0
    bar_skyline_error=0
    
    model_correct=0
    model_remove=0
    model_error=0
    model_multi_frame=0
    
    na_detect_correct=0
    na_detect_fail=0
    model_detect_fail=0 
    
    low_correct=0
    low_error=0
    low_na=0
       
    #[name,peptide,PrecursorCharge,ProductMz,FragmentIon,ProductCharge,IsotopeLabelType,TotalArea,Times,Intensities]
    ##cal model&human overlap
    csvcol=["File Name","Peptide Modified Sequence","Min Start Time","Max End Time","Precursor Charge","Fragment Ion","Product Charge","Isotope Label Type","PrecursorIsDecoy"]
    csvrqcol=["File Name","Model_RQscore","Skyline_RQscore"]
    csvall_list=["File Name","Peptide Modified Sequence","type"]
    iteration=np.shape(np.array(all_file))[0]  
    #for i in range(10):
    for i in range(iteration):
        ######[name,start_human,end_human,start_skyline,end_skyline,newname]
        imagename=all_file[i][5]
        filename=all_file[i][0].split("-..-")[0]
        peptide=all_file[i][0].split("-..-")[1].split("_")[0]
        skyline_start=all_file[i][3]
        skyline_end=all_file[i][4]
        
        if imagename in NA_file:
            if os.path.isfile(txtfolder+"/high_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/high_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/high_interference/txt/"+all_file[i][0])
            elif os.path.isfile(txtfolder+"/low_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/low_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/low_interference/txt/"+all_file[i][0])
            elif os.path.isfile(txtfolder+"/notmatch_txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/notmatch_txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/low_interference/txt/"+all_file[i][0])
            #print(transition[0])
            #print(transition[1])
            #print(transition[2])
            
            if all_file[i][1]!='NA':
                all_list.append([filename,peptide,'False_deletion'])
                na_detect_fail+=1
            else:
                all_list.append([filename,peptide,'True_deletion'])
                na_detect_correct+=1
            
            for t in transition:
                precursor=t.split("&")[0]
                fragment=t.split("&")[1]
                product=t.split("&")[2]
                csv_NA.append([filename,peptide,"#N/A","#N/A",precursor,fragment,product,"light","FALSE"])
            for t_heavy in transition_heavy:
                precursor_heavy=t_heavy.split("&")[0]
                fragment_heavy=t_heavy.split("&")[1]
                product_heavy=t_heavy.split("&")[2]
                csv_NA.append([filename,peptide,"#N/A","#N/A",precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
        
        elif imagename in human_file:
            if os.path.isfile(txtfolder+"/high_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/high_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/high_interference/txt/"+all_file[i][0])
            elif os.path.isfile(txtfolder+"/low_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/low_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/low_interference/txt/"+all_file[i][0])
            elif os.path.isfile(txtfolder+"/notmatch_txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/notmatch_txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/notmatch_txt/"+all_file[i][0])
            #print(transition[0])
            #print(transition[1])
            #print(transition[2])
            
            all_list.append([filename,peptide,'uncertain'])
            model_detect_fail+=1
                
            for t in transition:
                precursor=t.split("&")[0]
                fragment=t.split("&")[1]
                product=t.split("&")[2]
                csv_human.append([filename,peptide,skyline_start,skyline_end,precursor,fragment,product,"light","FALSE"])
            for t_heavy in transition_heavy:
                precursor_heavy=t_heavy.split("&")[0]
                fragment_heavy=t_heavy.split("&")[1]
                product_heavy=t_heavy.split("&")[2]
                csv_human.append([filename,peptide,skyline_start,skyline_end,precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])            
        
        elif imagename in AI_file:
            if os.path.isfile(txtfolder+"/high_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/high_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/high_interference/txt/"+all_file[i][0])
                time=gettime(txtfolder+'/high_interference/txt/'+all_file[i][0])
                intensity=getlist(txtfolder+'/high_interference/txt/'+all_file[i][0])
            '''
            elif os.path.isfile(txtfolder+"/low_interference/txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/low_interference/txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/low_interference/txt/"+all_file[i][0])
                time=gettime(txtfolder+'/low_interference/txt/'+all_file[i][0])
                intensity=getlist(txtfolder+'/low_interference/txt/'+all_file[i][0])
            elif os.path.isfile(txtfolder+"/notmatch_txt/"+all_file[i][0]):
                transition=get_transition(txtfolder+"/notmatch_txt/"+all_file[i][0])
                transition_heavy=get_transition_heavy(txtfolder+"/notmatch_txt/"+all_file[i][0])
                time=gettime(txtfolder+'/notmatch_txt/'+all_file[i][0])
                intensity=getlist(txtfolder+'/notmatch_txt/'+all_file[i][0])
            '''
            #print(transition[0])
            #print(transition[1])
            #print(transition[2])
            
            
            #print(imagename)
            b_iter=np.shape(np.array(bbox))[0]  
            for j in range(b_iter):
                #print(bbox[j][0])
                if bbox[j][0]==all_file[i][5]:
                    ###heatmap座標軸轉回滯留時間軸(可能有誤？)
                    if human_csv==1:
                        if all_file[i][1]=='NA':
                            all_list.append([filename,peptide,'miss_deletion'])
                            model_multi_frame+=1
                            for t in transition:
                                precursor=t.split("&")[0]
                                fragment=t.split("&")[1]
                                product=t.split("&")[2]
                                csv_AI.append([filename,peptide,skyline_start,skyline_end,precursor,fragment,product,"light","FALSE"])
                            for t_heavy in transition_heavy:
                                precursor_heavy=t_heavy.split("&")[0]
                                fragment_heavy=t_heavy.split("&")[1]
                                product_heavy=t_heavy.split("&")[2]
                                csv_AI.append([filename,peptide,skyline_start,skyline_end,precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
                        hmin_pixel=0
                        hmax_pixel=0
                        if os.path.isfile(txtfolder+"/high_interference/human_xml/"+all_file[i][5][0:-4]+".xml"):                       
                            with open(txtfolder+"/high_interference/human_xml/"+all_file[i][5][0:-4]+".xml",'r') as data:
                                xml = BeautifulSoup(data.read(), "lxml")
                                hmin_pixel = int(xml.find("xmin").get_text())
                                hmax_pixel = int(xml.find("xmax").get_text())
                        elif not os.path.isfile(txtfolder+"/high_interference/human_xml/"+all_file[i][5][0:-4]+".xml"):
                            continue
                    
                    smin_pixel=0
                    smax_pixel=0
                    if os.path.isfile(txtfolder+"/high_interference/skyline_xml/"+all_file[i][5][0:-4]+".xml"):
                        with open(txtfolder+"/high_interference/skyline_xml/"+all_file[i][5][0:-4]+".xml",'r') as data:
                            xml = BeautifulSoup(data.read(), "lxml")
                            smin_pixel = int(xml.find("xmin").get_text())
                            smax_pixel = int(xml.find("xmax").get_text())
                    elif not os.path.isfile(txtfolder+"/high_interference/skyline_xml/"+all_file[i][5][0:-4]+".xml"):
                        continue
                    #print(smin_pixel,smax_pixel)    
                    step_len=time[1]-time[0]
                    smin=float(all_file[i][3])
                    smax=float(all_file[i][4])
                    
                    mmin_pixel=int(bbox[j][1].split(".")[0])
                    mmax_pixel=int(bbox[j][2].split(".")[0])
                    
                    if human_csv==1:
                        refpoint=np.array(np.sort([time[0],float(all_file[i][1]),float(all_file[i][2]),smin,smax,time[-1]]))
                        refpoint_pixel=np.array(np.sort([0,hmin_pixel,hmax_pixel,smin_pixel,smax_pixel,300]))
                    elif human_csv==0:
                        refpoint=np.array(np.sort([time[0],smin,smax,time[-1]]))
                        refpoint_pixel=np.array(np.sort([0,smin_pixel,smax_pixel,300]))
                   
                    mmin=0
                    dist_pixel=mmin_pixel-refpoint_pixel
                    #print(dist_pixel)
                    dist_min=np.amin(np.absolute(dist_pixel))
                    idx_ref=np.where(np.logical_or(dist_pixel==dist_min,dist_pixel==dist_min*-1))[0][0]
                    #print(idx_ref)
                    val_ref=refpoint_pixel[idx_ref]
                    #print(val_ref)
                    if(mmin_pixel==val_ref):
                        mmin=refpoint[idx_ref]
                    else:
                        mmin=refpoint[idx_ref]+dist_pixel[idx_ref]*step_len*len(time)/300
                    
                    mmax=0
                    dist_pixel=mmax_pixel-refpoint_pixel
                    #print(dist_pixel)
                    dist_min=np.amin(np.absolute(dist_pixel))
                    idx_ref=np.where(np.logical_or(dist_pixel==dist_min,dist_pixel==dist_min*-1))[0][0]
                    #print(idx_ref)
                    val_ref=refpoint_pixel[idx_ref]
                    #print(val_ref)
                    if(mmax_pixel==val_ref):
                        mmax=refpoint[idx_ref]
                    else:
                        mmax=refpoint[idx_ref]+dist_pixel[idx_ref]*step_len*len(time)/300
                    #print(mmax)
                    # 以上 heatmap座標軸轉回滯留時間軸(可能有誤？)
                    '''
                    time=gettime(txtfolder+'/high_interference/txt/'+all_file[i][0])        
                    intensity=getlist(txtfolder+'/high_interference/txt/'+all_file[i][0])
                    '''
                    RQ_score=cal_RQscore(time,intensity,float(all_file[i][1]),float(all_file[i][2]),round(mmin, 2),round(mmax, 2))
                    RQ_score_skyline=cal_RQscore(time,intensity,float(all_file[i][1]),float(all_file[i][2]),smin,smax)
                    
                    if human_csv==1:
                        if all_file[i][1]!='NA':
                            if(RQ_score>=0.8 and RQ_score<=1.2):
                                RQ_csv.append([filename,RQ_score,RQ_score_skyline])
                                all_list.append([filename,peptide,'correct'])
                                model_correct+=1
                                
                                R_Position=RQ_frequency(RQ_score)
                                score[R_Position]+=1
                                R_Position_skyline=RQ_frequency(RQ_score_skyline)
                                score_skyline[R_Position_skyline]+=1
                                
                                for t in transition:
                                    precursor=t.split("&")[0]
                                    fragment=t.split("&")[1]
                                    product=t.split("&")[2]
                                    csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor,fragment,product,"light","FALSE"])
                                for t_heavy in transition_heavy:
                                    precursor_heavy=t_heavy.split("&")[0]
                                    fragment_heavy=t_heavy.split("&")[1]
                                    product_heavy=t_heavy.split("&")[2]
                                    csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
                            elif(RQ_score==-1 or RQ_score==-2):
                                all_list.append([filename,peptide,'uncertain'])
                                model_remove+=1                               
                                print("image_name:{},filename:{},RQ_score:{}".format(imagename,all_file[i][0],RQ_score))
                                print("#######################################")                         
                                for t in transition:
                                    precursor=t.split("&")[0]
                                    fragment=t.split("&")[1]
                                    product=t.split("&")[2]
                                    csv_human.append([filename,peptide,skyline_start,skyline_end,precursor,fragment,product,"light","FALSE"])
                                for t_heavy in transition_heavy:
                                    precursor_heavy=t_heavy.split("&")[0]
                                    fragment_heavy=t_heavy.split("&")[1]
                                    product_heavy=t_heavy.split("&")[2]
                                    csv_human.append([filename,peptide,skyline_start,skyline_end,precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
                            else:
                                RQ_csv.append([filename,RQ_score,RQ_score_skyline])
                                all_list.append([filename,peptide,'error'])
                                plt_image(txtfolder,time,intensity,all_file[i][1],all_file[i][2],all_file[i][3],all_file[i][4],round(mmin, 2),round(mmax, 2),'high',imagename,RQ_score,RQ_score_skyline)
                                model_error+=1
                                
                                R_Position=RQ_frequency(RQ_score)
                                score[R_Position]+=1
                                R_Position_skyline=RQ_frequency(RQ_score_skyline)
                                score_skyline[R_Position_skyline]+=1
                                
                                for t in transition:
                                    precursor=t.split("&")[0]
                                    fragment=t.split("&")[1]
                                    product=t.split("&")[2]      
                                    csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor,fragment,product,"light","FALSE"])
                                for t_heavy in transition_heavy:
                                    precursor_heavy=t_heavy.split("&")[0]
                                    fragment_heavy=t_heavy.split("&")[1]
                                    product_heavy=t_heavy.split("&")[2]
                                    csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])      
                    elif human_csv==0:
                        for t in transition:
                            precursor=t.split("&")[0]
                            fragment=t.split("&")[1]
                            product=t.split("&")[2]
                            csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor,fragment,product,"light","FALSE"])
                        for t_heavy in transition_heavy:
                            precursor_heavy=t_heavy.split("&")[0]
                            fragment_heavy=t_heavy.split("&")[1]
                            product_heavy=t_heavy.split("&")[2]
                            csv_AI.append([filename,peptide,round(mmin, 2),round(mmax, 2),precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
                                            
        else:
            if not os.path.isfile(txtfolder+"/low_interference/txt/"+all_file[i][0]):
                continue
            if human_csv==1:
                if all_file[i][1]!='NA':
                    hmin=float(all_file[i][1])
                    hmax=float(all_file[i][2])
                    smin=float(all_file[i][3])
                    smax=float(all_file[i][4]) 
                         
                    time=gettime(txtfolder+'/low_interference/txt/'+all_file[i][0])        
                    intensity=getlist(txtfolder+'/low_interference/txt/'+all_file[i][0])
                    RQ_score=cal_RQscore(time,intensity,hmin,hmax,smin,smax)
                
                    R_Position=RQ_frequency(RQ_score)
                    score[R_Position]+=1
                    R_Position_skyline=RQ_frequency(RQ_score)
                    score_skyline[R_Position_skyline]+=1
                    
                    RQ_csv.append([all_file[i][0],RQ_score,RQ_score])
                    if(RQ_score>=0.8 and RQ_score<=1.2):
                        all_list.append([filename,peptide,'correct'])
                        low_correct+=1
                    elif(RQ_score!=-1 and RQ_score!=-2):
                        all_list.append([filename,peptide,'error'])
                        plt_image(txtfolder,time,intensity,all_file[i][1],all_file[i][2],all_file[i][3],all_file[i][4],all_file[i][3],all_file[i][4],'low',imagename,RQ_score,RQ_score)
                        low_error+=1
                elif all_file[i][1]=='NA':
                    all_list.append([filename,peptide,'miss_deletion'])
                    low_na+=1
                     
            transition=get_transition(txtfolder+"/low_interference/txt/"+all_file[i][0])
            transition_heavy=get_transition_heavy(txtfolder+"/low_interference/txt/"+all_file[i][0])
            for t in transition:
                precursor=t.split("&")[0]
                fragment=t.split("&")[1]
                product=t.split("&")[2]
                csv_AI.append([filename,peptide,skyline_start,skyline_end,precursor,fragment,product,"light","FALSE"])
            for t_heavy in transition_heavy:
                precursor_heavy=t_heavy.split("&")[0]
                fragment_heavy=t_heavy.split("&")[1]
                product_heavy=t_heavy.split("&")[2]
                csv_AI.append([filename,peptide,skyline_start,skyline_end,precursor_heavy,fragment_heavy,product_heavy,"heavy","FALSE"])
    
    df_rq = pd.DataFrame(RQ_csv,columns=csvrqcol) 
    df_rq.to_csv(txtfolder+'_compare_RQ.csv',index = False)
    os.chmod(txtfolder+'_compare_RQ.csv', 0o777)
    
    df_all_list = pd.DataFrame(all_list,columns=csvall_list)
    df_all_list.to_csv(txtfolder+"/list.csv",index = False)
    os.chmod(txtfolder+"/list.csv", 0o777)
                      
    df_NA = pd.DataFrame(csv_NA,columns=csvcol)
    df_NA = df_NA.sort_values(["Peptide Modified Sequence","File Name","Isotope Label Type"], ascending = (False,False,False))
    #print(df_NA)        
    df_NA.to_csv(txtfolder+"/NA.csv",index=False)
    os.chmod(txtfolder+"/NA.csv", 0o777)
    #print(df_NA["File Name"])        
    
    df_human = pd.DataFrame(csv_human,columns=csvcol)
    df_human = df_human.sort_values(["Peptide Modified Sequence","File Name","Isotope Label Type"], ascending = (False,False,False))
    #print(df_human)        
    df_human.to_csv(txtfolder+"/human.csv",index=False)
    os.chmod(txtfolder+"/human.csv", 0o777)
    
    df_AI = pd.DataFrame(csv_AI,columns=csvcol)
    df_AI = df_AI.sort_values(["Peptide Modified Sequence","File Name","Isotope Label Type"], ascending = (False,False,False))
    #print(df_AI)        
    df_AI.to_csv(txtfolder+"/AI.csv",index=False)
    os.chmod(txtfolder+"/AI.csv", 0o777)   
    
    if human_csv==1:
        print("RQ_score>=0.8 and RQ_score<=1.2:{} RQ_score_remove:{} RQ_score_error:{}".format(model_correct,model_remove,model_error))
        
        #AI_model
        plt.figure(1)
        labels='correct','error','miss deletion','uncertain','True deletion','False deletion'
        size=[(model_correct+low_correct),(low_error+model_error),(low_na+model_multi_frame),(model_detect_fail+model_remove),na_detect_correct,na_detect_fail]
        print(model_correct,low_correct,low_error,model_error,low_na,model_multi_frame,model_detect_fail,model_remove,na_detect_correct,na_detect_fail)
        print(model_correct+low_correct,low_error+model_error,low_na+model_multi_frame,model_detect_fail+model_remove,na_detect_correct,na_detect_fail)
        colors=['#46A3FF','#FF7575','#8E8E8E','#00DB00','#BE77FF','#AE57A4']
        plt.title('AI_model',fontsize=16)
        patches,l_text,p_text=plt.pie(size,labels=labels,colors=colors,autopct='%1.1f%%',startangle=90)#Set302
        #patches,l_text,p_text=plt.pie(size,labels=labels,colors=colors,autopct='%1.1f%%',startangle=90,pctdistance=0.6,explode=(0,0,0.1,0.2,0,0))#Set451
        for t in p_text:
            t.set_size(10) 
        for t in l_text:
            t.set_size(14)
        plt.axis('equal')
        plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/model_pie.png')
        os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/model_pie.png', 0o777)
        #AI_csv
        plt.figure(2)
        AI_csv_labels='correct','error','miss deletion'
        AI_csv_size=[(model_correct+low_correct),(low_error+model_error),(low_na+model_multi_frame)]
        print(model_correct+low_correct,low_error+model_error,low_na+model_multi_frame)
        AI_csv_colors=['#46A3FF','#FF7575','#8E8E8E']
        plt.title('AI_csv',fontsize=16)
        #patches,l_text,p_text=plt.pie(AI_csv_size,labels=AI_csv_labels,colors=AI_csv_colors,autopct='%1.1f%%',startangle=90)
        patches,l_text,p_text=plt.pie(AI_csv_size,labels=AI_csv_labels,colors=AI_csv_colors,autopct='%1.1f%%',startangle=90,pctdistance=0.6,explode=(0,0,0.1))
        for t in p_text:
            t.set_size(10) 
        for t in l_text:
            t.set_size(14)
        plt.axis('equal')
        plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/AI_csv_pie.png')
        os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/AI_csv_pie.png', 0o777)
        #NA_csv
        plt.figure(3)
        NA_csv_labels='True deletion','False deletion'
        NA_csv_size=[na_detect_correct,na_detect_fail]
        print(na_detect_correct,na_detect_fail)
        NA_csv_colors=['#BE77FF','#AE57A4']
        plt.title('deletion',fontsize=16)
        patches,l_text,p_text=plt.pie(NA_csv_size,labels=NA_csv_labels,colors=NA_csv_colors,autopct='%1.1f%%',startangle=90)
        for t in p_text:
            t.set_size(10) 
        for t in l_text:
            t.set_size(14)
        plt.axis('equal')
        plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/NA_csv_pie.png')
        os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/NA_csv_pie.png', 0o777)
        #bar
        plt.figure(4,figsize=(15, 10), dpi=150)
        ratio=[]
        ratio_skyline=[]
        for s in range(len(score)):
            if s>=8 and s<=12:
                bar_model_correct+=score[s]
                bar_skyline_correct+=score_skyline[s]
            else:
                bar_model_error+=score[s]
                bar_skyline_error+=score_skyline[s]
            ratio.append(float((score[s]/(model_correct+model_error+low_correct+low_error))*100))
            ratio_skyline.append(float((score_skyline[s]/(model_correct+model_error+low_correct+low_error))*100))
            #ratio.append(round(float((score[s]/(model_correct+model_error+low_correct+low_error))*100),1))
            #ratio_skyline.append(round(float((score_skyline[s]/(model_correct+model_error+low_correct+low_error))*100),1))
        print("bar_model_correct:{} bar_model_error:{} bar_skyline_correct:{} bar_skyline_error:{}".format(bar_model_correct,bar_model_error,bar_skyline_correct,bar_skyline_error))
        name=['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1','1.1','1.2','1.3','1.4','1.5','>1.5']
        x = np.arange(len(name))
        width = 0.5
        A=plt.bar(x-width/2, ratio, width, color='red',label='Model')
        B=plt.bar(x+width/2, ratio_skyline, width, color='blue',label='Skyline')
        plt.xticks(x + width / 100, name)
        plt.ylim(0,100)
        plt.xlabel('AQscore')
        plt.ylabel('%')
        plt.title('Model vs. Skyline')
        createLabels(A)
        createLabels(B)
        plt.legend(["Model", "Skyline"],loc='upper right')
        plt.text(0.1,np.amax(ratio)*0.95,'data num:{}'.format(model_correct+model_error+low_correct+low_error),fontsize=10, color='black')
        plt.axvline(7.5,color="#000000",alpha=0.5,ls='dotted')
        plt.axvline(12.5,color="#000000",alpha=0.5,ls='dotted')
        plt.savefig(sys.argv[1]+'/'+sys.argv[2]+'/bar.png')
        os.chmod(sys.argv[1]+'/'+sys.argv[2]+'/bar.png', 0o777)
        
#######  main   ##############
import time
start=time.time()
print("code 12 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("12_export_skylinecsv.py",time.ctime(start)))
    f.close()

##parameter
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"
tsv_path=sys.argv[1]+"/"+sys.argv[2]+"/time_intensity.tsv"
test_folder="auto_test"
allfile=fileinfo(txtfolder)
#RQ_score=0

if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    exportcsv(allfile,txtfolder,test_folder,1)
else:
    exportcsv(allfile,txtfolder,test_folder,0)

end=time.time()
print("12_export_skylinecsv.py use {} seconds.".format(end-start))

