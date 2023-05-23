#!/usr/bin/python
import os 
import time
import glob
import sys
  
from shutil import copyfile 
from shutil import copytree        
#######  main   ##############

start=time.time()
print("code 11 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("11_exec_predict_boundary.py",time.ctime(start)))
    f.close()
##parameter

txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"
testfolder="auto_test"
rawdata_path="/docker_mount/web/"
FasterRCNN_path="/docker_mount/Faster-RCNN-TensorFlow-Python3/"
predict_model_path="/docker_mount/3object(tar_na_hm)_model/451_all_sele_integral_range/"
#predict_model_path="/docker_mount/3object(tar_na_hm)_model/CKD_OSCC_302_all_sele_integral_range/"


files = glob.glob("./"+txtfolder+"/high_interference/"+testfolder+"/classify_result/image_weight_acce_HM/*")
#print(len(files))
if len(files) !=0:
    PATH="./"+txtfolder+"/high_interference/"+testfolder+"/predict_result/"
    if not os.path.exists(PATH):
        os.makedirs(PATH)
        os.chmod(PATH, 0o777)
    #remove old testing data(heatmap) & object detect result 
    files = glob.glob(FasterRCNN_path+"data/demo/*")
    #print(len(files))
    for f in files:
        #print("rm",f)
        os.remove(f) 
    files = glob.glob(FasterRCNN_path+"data/testfigs/*")
    #print(len(files))
    for f in files:
        #print("rm",f)
        os.remove(f)  
    files = glob.glob(FasterRCNN_path+"output/vgg16/voc_2007_trainval+voc_2012_trainval/default/*")
    #print(len(files))
    for f in files:
        #print("rm",f)
        os.remove(f)    
        
    #copy new testing data
    files = glob.glob("./"+txtfolder+"/high_interference/"+testfolder+"/classify_result/image_weight_acce_HM/*")
    #print(len(files))
    for f in files:
        fname=f.split("/")[-1]
        #print("cp",f,"\tto\t",FasterRCNN_path+"data/demo/"+fname)
        copyfile(f,FasterRCNN_path+"data/demo/"+fname)
    
    
    #copy classify ai model
    files = glob.glob(predict_model_path+"vgg16*")
    #print(len(files))
    for f in files:
        fname=f.split("/")[-1]
        print("cp",f,"\tto\t",FasterRCNN_path+"output/vgg16/voc_2007_trainval+voc_2012_trainval/default/"+fname)
        copyfile(f,FasterRCNN_path+"output/vgg16/voc_2007_trainval+voc_2012_trainval/default/"+fname)
    
    #exec ai predict chromatogram boundary
    os.chdir(FasterRCNN_path)
    os.system('python demo.py')
    #os.system('python demo451.py')

    ####回原路徑 20210226_OSCC2_sele_test
    os.chdir(rawdata_path)
    files = glob.glob("/docker_mount/Faster-RCNN-TensorFlow-Python3/data/testfigs/")
    for f in files:
        print("cp",f,"\tto\t",PATH)
        copytree(FasterRCNN_path+"data/testfigs/",PATH+"testfigs")  
    copyfile(FasterRCNN_path+"data/bbox.txt",PATH+"bbox.txt")
    os.chmod(PATH, 0o777)  
    #copyfile(FasterRCNN_path+"data/classification.txt",PATH+"classification.txt") 
     
end=time.time()
print("11_exec_predict_boundary.py use {} seconds.".format(end-start))

