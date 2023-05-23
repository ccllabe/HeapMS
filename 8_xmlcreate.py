#!/usr/bin/python
import xml.etree.cElementTree as ET
import math
import os
import numpy as np
import csv
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
           start_human=line.split("\t")[2]
           end_human=line.split("\t")[3]
           start_skyline=line.split("\t")[4]
           end_skyline=line.split("\t")[5]
           allfile.append([name,start_human,end_human,start_skyline,end_skyline])
           if 'str' in line:
              break
    return allfile
    
def getxml(all_file,txtfolder,savefolder):
    #folder=savefolder
    #PATH="./"+peptide
    
    #skyline bad產生xml
    if not os.path.exists(txtfolder+"/high_interference/"+savefolder):
        os.makedirs(txtfolder+"/high_interference/"+savefolder)
        os.chmod(txtfolder+"/high_interference/"+savefolder, 0o777)
    iteration=np.shape(np.array(all_file))[0] 
    #print(iteration)
    for i in range(iteration):
        #只要info.txt中有任一個欄位為NA 就不產生xml
        if(all_file[i][1]=="NA" or all_file[i][2]=="NA" or all_file[i][3]=="NA" or all_file[i][4]=="NA"):
            continue        
        if os.path.isfile(txtfolder+'/high_interference/txt/'+all_file[i][0]):
            ##get time 取得mass時間軸(資料加倍後)
            time=gettime(txtfolder+'/high_interference/txt/'+all_file[i][0])
            time=arr_extend(time,3)
            
            time_init=time[0]
            time_final=time[-1]
            if(savefolder=="human_xml"):
                start_time=float(all_file[i][1])
                end_time=float(all_file[i][2])
            elif(savefolder=="skyline_xml"):
                start_time=float(all_file[i][3])
                end_time=float(all_file[i][4])
            near_start=find_nearest(time,start_time)   ###start_time不存在time中 取最近的值
            near_end=find_nearest(time,end_time)
            index_start= np.where(np.isclose(time,near_start))[0]  #float比較時不一定完全相等 比較相等時用isclose()代替
            index_end= np.where(np.isclose(time,near_end))[0] 


            total=time_final-time_init
            region=near_end-near_start
            pixelmin=int((near_start-time_init)/total*300)
            pixelmax=int((near_end-time_init)/total*300)
     
            filename="%06d"%i
            print(filename)
            path='/docker_mount/Faster-RCNN-TensorFlow-Python3/data/VOCdevkit2007/VOC2007/JPEGImages/'+filename
            #savexml(filename,path,str(pixelmax),str(pixelmin),str(pixelmax),str(pixelmin),peptide+'/'+"xml")
            #savexml(filename,path,str(pixelmax),str(pixelmin),str(pixelmax),str(pixelmin),peptide+'/high_interference/'+savefolder)
            savexml(filename,path,str(pixelmax),str(pixelmin),str(pixelmax),str(pixelmin),txtfolder+'/high_interference/'+savefolder)

def savexml(filename,path,xmax,xmin,ymax,ymin,savefolder):
	
	annotation = ET.Element("annotation")
	ET.SubElement(annotation, "folder").text = "VOC2007"
	ET.SubElement(annotation, "filename").text = filename+".png"
	#ET.SubElement(annotation, "path").text = path+".png"

	source = ET.SubElement(annotation, "source")
	ET.SubElement(source, "database").text = "Unknown"

	size = ET.SubElement(annotation, "size")
	ET.SubElement(size, "width").text = "300"
	ET.SubElement(size, "height").text = "300"
	ET.SubElement(size, "depth").text = "3"


	ET.SubElement(annotation, "segmented").text = "0"

	Object = ET.SubElement(annotation, "object")
	ET.SubElement(Object, "name").text = 'target'
	#ET.SubElement(Object, "pose").text = 'Unspecified'
	ET.SubElement(Object, "truncated").text = '1'
	ET.SubElement(Object, "difficult").text = '0'

	bndbox = ET.SubElement(Object, "bndbox")
	ET.SubElement(bndbox, "xmin").text = xmin
	ET.SubElement(bndbox, "ymin").text = ymin
	ET.SubElement(bndbox, "xmax").text = xmax
	ET.SubElement(bndbox, "ymax").text = ymax

	tree = ET.ElementTree(annotation)
	tree.write(savefolder+"/"+filename+".xml")
	os.chmod(savefolder+"/"+filename+".xml", 0o777)
	#tree.write("xml/"+filename+".xml")
	return
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

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

            
#######  main   ##############
import time

start=time.time()
print("code 8 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("8_xmlcreate.py",time.ctime(start)))
    f.close()

##parameter

txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

allfile=fileinfo(txtfolder)
if os.path.isfile(sys.argv[1]+"/"+sys.argv[2]+"/human.csv"):
    getxml(allfile,txtfolder,"human_xml")
    
getxml(allfile,txtfolder,"skyline_xml")


end=time.time()
print("8_xmlcreate.py use {} seconds.".format(end-start))
