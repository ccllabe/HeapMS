#!/usr/bin/python
import os
from os import walk
import glob
from shutil import copyfile
import time

def fileinfo(txt_name):
    allfile=[]
    with open(txt_name) as f:
       for line in f:
           node=line.split("\t")[0].strip()       
           
           #skip 1st row
           if node=="node_id":
               continue          
           time=line.split("\t")[1]
           
           allfile.append([node,time])
    return allfile

#######  main   ##############
start=time.time()
#print(start)

txtfolder="upload"
count=0
for root, dirs, files in walk(txtfolder):
    if root==txtfolder:
        dirs.sort()
        for dir_name in dirs:
            folder=root+"/"+dir_name
            if os.path.isfile(folder+"/finished.txt"):
                print(dir_name+" finished!")
                continue
            if os.path.isfile(folder+"/running.txt"):
                allfile=fileinfo(folder+"/running.txt")
                print(dir_name+" run now! node_id: "+allfile[0][0])
                if allfile[0][0]=='1':
                    break
                else:
                    continue
            if not os.path.isfile(folder+"/running.txt"):
                count+=1
                if count==1:
                    print(dir_name+" get job! node_id: 2")
                    fo = open(folder+"/running.txt", "w")
                    fo.writelines("{}\t{}\n".format("node_id","get_job_time"))
                    fo.writelines("{}\t{}\n".format("2",time.ctime(time.time())))
                    os.chmod(folder+"/running.txt", 0o777)
                    fo.close()
                    
                    code = open(folder+"/log.txt", "w")
                    os.chmod(folder+"/log.txt", 0o777)
                    code.writelines("{}\t{}\n".format("code","start_time"))
                    code.close()
                    
                    
                    os.system('python 1_rmTQN_format_trans.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 2_checkline.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 3_rm_csv_notmatch.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 4_remove_NA.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 5_create_info.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 6_remove_cannot_calRQ.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 7_sele_perfect_txt.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 8_xmlcreate.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 9_img.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 10_coatnet_classify.py '+txtfolder+' '+dir_name)
                         
                    os.system('python 11_exec_predict_boundary.py '+txtfolder+' '+dir_name)
                           
                    os.system('python 12_export_skylinecsv.py '+txtfolder+' '+dir_name)
                    
                    os.system('python 13_createtsv.py '+txtfolder+' '+dir_name)
                    
                    final = open(folder+"/finished.txt", "w")
                    final.writelines("{}\n".format("time"))
                    final.writelines("{}\n".format(time.ctime(time.time())))
                    os.chmod(folder+"/finished.txt", 0o777)                    
                    final.close()
                    


