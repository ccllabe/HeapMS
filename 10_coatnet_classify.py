#!/usr/bin/python
import os 
import glob
from shutil import copyfile
import time
import numpy as np
import sys

def rm_olddata(path):#remove old testing data(heatmap) & object detect result 
	files = glob.glob(path+"*")
	if len(files) !=0:
		for f in files:
			print("rm",f)
			os.remove(f) 
def readinfo(info_name):
	allfile=[]
	with open(info_name) as f:
		for line in f:
			name=line.split("\t")[0].strip()
			if name=="ori_name":
				continue
			png_name=line.split("\t")[1]
			start_human=line.split("\t")[2]
			end_human=line.split("\t")[3]
			start_skyline=line.split("\t")[4]
			end_skyline=line.split("\t")[5]
			allfile.append([name,png_name,start_human,end_human,start_skyline,end_skyline[:-1]])
	return allfile
			

#######  main   ##############
start=time.time()
print("code 10 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("10_coatnet_classify.py",time.ctime(start)))
    f.close()

##parameter
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"
info_name=txtfolder+"_info.txt"
imgfolder= txtfolder + "/high_interference/image_weight/"
CoAtNet_path="/docker_mount/CoAtNet/"
rawdata_path="/docker_mount/web/"
testfolder="auto_test"

test_HM=CoAtNet_path+"data/test/HM/"
test_NA=CoAtNet_path+"data/test/NA/"
result_HM=CoAtNet_path+"data/result/HM/"
result_NA=CoAtNet_path+"data/result/NA/"

rm_olddata(test_HM)
rm_olddata(test_NA)

allfile=readinfo(info_name)
for filename in os.listdir(imgfolder):
	for i in range(len(allfile)):
		if filename==allfile[i][1]:
			if allfile[i][2]=="NA":#NA
				copyfile(imgfolder+filename , test_NA+filename)
			else:
				copyfile(imgfolder+filename , test_HM+filename)
				
classify_path_HM= txtfolder + "/high_interference/"+ testfolder + "/classify_result/image_weight_acce_HM/"
classify_path_NA= txtfolder + "/high_interference/"+ testfolder + "/classify_result/image_weight_acce_NA/"
if not os.path.exists(classify_path_HM):
        os.makedirs(classify_path_HM)
        os.chmod(classify_path_HM, 0o777)
if not os.path.exists(classify_path_NA):
        os.makedirs(classify_path_NA)
        os.chmod(classify_path_NA, 0o777)

rm_olddata(classify_path_HM)
rm_olddata(classify_path_NA)

os.chdir(CoAtNet_path)
os.system('python test.py')
#os.system('python test451.py')
os.chdir(rawdata_path)

for filename in os.listdir(result_HM):
	copyfile(result_HM+filename , classify_path_HM+filename)
for filename in os.listdir(result_NA):
	copyfile(result_NA+filename , classify_path_NA+filename)
copyfile(CoAtNet_path+"data/result/classification.txt", txtfolder + "/high_interference/"+ testfolder + "/classify_result/classification.txt")
os.chmod(txtfolder + "/high_interference/"+ testfolder + "/classify_result", 0o777)
os.chmod(txtfolder + "/high_interference/"+ testfolder, 0o777)
    
end=time.time()
print("10_coatnet_classify.py use {} seconds.".format(end-start))
	
