#!/usr/bin/python
import pandas as pd
import os
import time
import sys

start=time.time()
print("code 1 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("1_rmTQN_format_trans.py",time.ctime(start)))
    f.close()

df = pd.read_csv(sys.argv[1]+"/"+sys.argv[2]+"/time_intensity.tsv",sep='\t')

folder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"
if not os.path.exists(folder):
    os.makedirs(folder)
    os.chmod(folder, 0o777) # for example

for index, row in df.iterrows():
    #remove peptide TQN
    if(row["PeptideModifiedSequence"]=="TQNDVDIADVAYYFEK"):
        continue
    #generate txt
    f=open("./"+folder+"/"+row["FileName"]+"-..-"+row["PeptideModifiedSequence"]+"_"+row["IsotopeLabelType"]+".txt",'a')
    os.chmod(folder+"/"+row["FileName"]+"-..-"+row["PeptideModifiedSequence"]+"_"+row["IsotopeLabelType"]+".txt", 0o777)
    #f.write(str(row["PrecursorCharge"])+"."+row["FragmentIon"]+"."+str(row["ProductCharge"])+"\n"+str(row["Times"])+"\n"+str(row["Intensities"])+"\n")
    f.write(str(row["PrecursorCharge"])+"&"+row["FragmentIon"]+"&"+str(row["ProductCharge"])+"\n"+str(row["Times"])+"\n"+str(row["Intensities"])+"\n")
    
end=time.time()
print("1_rmTQN_format_trans.py use {} seconds.".format(end-start))
