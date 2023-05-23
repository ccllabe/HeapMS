#!/usr/bin/python
import os
import time
import shutil
import sys

#######  main   ##############
start=time.time()
print("code 2 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("2_checkline.py",time.ctime(start)))
    f.close()

folder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"
for filename in os.listdir(folder):
    file = open(folder+"/"+filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    if(line_count!=9):
        print("name:{}\tline:{}".format(filename,line_count)) 
        count=str(line_count)
        if not os.path.exists(folder+"_"+count):
            os.makedirs(folder+"_"+count)
            os.chmod(folder+"_"+count, 0o777)
        shutil.move(folder+"/"+filename,folder+"_"+count+"/"+filename)
end=time.time()
print("2_checkline.py use {} seconds.".format(end-start))
