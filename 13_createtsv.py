import pandas as pd
import os
import time
import csv
import numpy
import sys

def csvinfo(peak,num):
    all_file=[]
    with open(peak, newline='') as csvfile:
        rows = csv.reader(csvfile)
        #skip 1st row of csv
        next(rows)
        for row in rows:
            name=row[0]
            peptide=row[1]
            
            all_file.append(name+"-..-"+peptide+"-..-"+num)
        new=numpy.unique(all_file)
    return new

def csvinfo_list(peak,num):
    all_file=[]
    with open(peak, newline='') as csvfile:
        rows = csv.reader(csvfile)
        #skip 1st row of csv
        next(rows)
        for row in rows:
            name=row[0]
            peptide=row[1]
            final_type=row[2]
            
            all_file.append(name+"-..-"+peptide+"-..-"+num+"-..-"+final_type)
        new=numpy.unique(all_file)
    return new

#######  main   ##############
import time
start=time.time()
print("code 13 start time: {}".format(time.ctime(start)))

with open(sys.argv[1]+"/"+sys.argv[2]+"/log.txt", 'a') as f:
    f.write("{}\t{}\n".format("13_createtsv.py",time.ctime(start)))
    f.close()
    
txtfolder=sys.argv[1]+"/"+ sys.argv[2]+"/Mass_txt"

peak_NA=txtfolder+"/NA.csv"
peak_human=txtfolder+"/human.csv"
peak_AI=txtfolder+"/AI.csv"
peak_list=txtfolder+"/list.csv"

csv_NA=csvinfo(peak_NA,'3')
csv_human=csvinfo(peak_human,'2')
csv_AI=csvinfo(peak_AI,'1')
csv_list=csvinfo_list(peak_list,'4')
total=numpy.concatenate((csv_NA, csv_human, csv_AI,csv_list))

df = pd.read_csv(sys.argv[1]+"/"+sys.argv[2]+"/time_intensity.tsv",sep='\t')

peptide_all=[]
tsv_NA=[]
tsv_human=[]
tsv_AI=[]
tsvcol=["FileName","PeptideModifiedSequence","PrecursorCharge","ProductMz","FragmentIon","ProductCharge","IsotopeLabelType","TotalArea","Times","Intensities"]

for index, row in df.iterrows():
    peptide_total=row["PeptideModifiedSequence"]
    peptide_all.append(peptide_total)
    new_name = row["FileName"]+"-..-"+row["PeptideModifiedSequence"]
    for n in range(len(csv_NA)):
        if(new_name+"-..-3"==csv_NA[n]):
           tsv_NA.append([row["FileName"],row["PeptideModifiedSequence"],row["PrecursorCharge"],row["ProductMz"],row["FragmentIon"],row["ProductCharge"],row["IsotopeLabelType"],row["TotalArea"],row["Times"],row["Intensities"]])

    for h in range(len(csv_human)):
        if(new_name+"-..-2"==csv_human[h]):
            tsv_human.append([row["FileName"],row["PeptideModifiedSequence"],row["PrecursorCharge"],row["ProductMz"],row["FragmentIon"],row["ProductCharge"],row["IsotopeLabelType"],row["TotalArea"],row["Times"],row["Intensities"]])

    for a in range(len(csv_AI)):
        if(new_name+"-..-1"==csv_AI[a]):
            tsv_AI.append([row["FileName"],row["PeptideModifiedSequence"],row["PrecursorCharge"],row["ProductMz"],row["FragmentIon"],row["ProductCharge"],row["IsotopeLabelType"],row["TotalArea"],row["Times"],row["Intensities"]])

peptide=numpy.unique(peptide_all)
csvcol=["Replicate Name\Protein Name"]
for p in range(len(peptide)):
    csvcol.append(peptide[p])
name=[]
csv=[]
csv_list=[]

for i in range(len(total)):
    filename=total[i].split(".wiff-..-")[0].strip()
    name.append(filename)
    
total_name=numpy.unique(name)

for j in range(len(total_name)):
    csv.append([total_name[j]])
    for p in range(len(peptide)):
        csv[j].append('0')
        
for j in range(len(total_name)):
    csv_list.append([total_name[j]])
    for p in range(len(peptide)):
        csv_list[j].append('0')
        
for n in range(len(total)):
    filename=total[n].split(".wiff-..-")[0].strip()
    pep=total[n].split("-..-")[1].strip()
    num_type=total[n].split("-..-")[2].strip()
    if num_type!='4':
        for t in range(len(total_name)):
            for e in range(len(peptide)):
                if filename==total_name[t] and pep==peptide[e]:
                    csv[t][e+1]=num_type
    elif num_type=='4':
        final_type=total[n].split("-..-")[3].strip()
        for t in range(len(total_name)):
            for e in range(len(peptide)):
                if filename==total_name[t] and pep==peptide[e]:
                    csv_list[t][e+1]=final_type
    
   
df_tsv_NA = pd.DataFrame(tsv_NA,columns=tsvcol)
df_tsv_NA = df_tsv_NA.sort_values(["PeptideModifiedSequence","FileName","IsotopeLabelType"], ascending = (False,False,False))
df_tsv_NA.to_csv(txtfolder+"/NA.tsv",index=False,sep='\t')
os.chmod(txtfolder+"/NA.tsv", 0o777)

df_tsv_human = pd.DataFrame(tsv_human,columns=tsvcol)
df_tsv_human = df_tsv_human.sort_values(["PeptideModifiedSequence","FileName","IsotopeLabelType"], ascending = (False,False,False))
df_tsv_human.to_csv(txtfolder+"/human.tsv",index=False,sep='\t')
os.chmod(txtfolder+"/human.tsv", 0o777)

df_tsv_AI = pd.DataFrame(tsv_AI,columns=tsvcol)
df_tsv_AI = df_tsv_AI.sort_values(["PeptideModifiedSequence","FileName","IsotopeLabelType"], ascending = (False,False,False))
df_tsv_AI.to_csv(txtfolder+"/AI.tsv",index=False,sep='\t')
os.chmod(txtfolder+"/AI.tsv", 0o777)

df_csv=pd.DataFrame(csv,columns=csvcol)
df_csv.to_csv(txtfolder+"/correspond.csv",index=False,sep='\t')
os.chmod(txtfolder+"/correspond.csv", 0o777)

df_csv_list=pd.DataFrame(csv_list,columns=csvcol)
df_csv_list.to_csv(txtfolder+"/all_list.csv",index=False,sep='\t')
os.chmod(txtfolder+"/all_list.csv", 0o777)

os.remove(txtfolder+"/list.csv")

end=time.time()
print("13_createtsv.py use {} seconds.".format(end-start))

