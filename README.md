![messageImage_1689681147873](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/51453a50-dc9c-4e6c-8a36-052c76811a74)
```diff
- Announcement: Scheduled power outage on July 23, 2023
 ```
# HeapMS-Installation-Process
First, open the terminal in your Ubuntu environment. Then, execute all the following commands and operations:
## Installing the environment   
1. Update  
   ```diff
   sudo apt-get update  
   ```
2. Remove the existing Docker environment.  
   ```diff
   sudo apt-get remove docker docker-engine docker.io   
   ```
3. Install a new Docker environment.  
   ```diff
   sudo apt install docker.io   
   ```
4. Run the Docker environment.  
   ```diff
   sudo service docker start    
   ```
   At this point, you will be able to execute Docker commands.
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/b48a5e90-ceec-4df7-a1bd-99485926fb62)
5. Find the absolute file path of the "pc4_heapms.tar" file stored on your computer.  
   Download pc4_heapms.tar (file size: ~60GB) link:
   (https://onedrive.live.com/?authkey=%21AO8kOvVhBSEuxZc&id=7309231C4353D1C0%21447583&cid=7309231C4353D1C0&parId=root&parQt=sharedby&o=OneUp) 
   ```diff
   realpath pc4_heapms.tar    
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/ab24823c-d153-4bde-bd3f-052551412e32)
7. Create a Docker image through the "pc4_heapms.tar" file. 
   ```diff
   docker load < /home/ccllab/Downloads/pc4_heapms.tar    
   ```
   After executing the command, the result will be as follows:
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/5924ad5e-039a-4f8a-a5f4-6ac92103ce80)
8. To check if the "pc4_heapms.tar" has been successfully created as a Docker image, you can use the following command:
   ```diff
   docker images   
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/87472e98-b8c2-46c8-8982-98961e8e4051)
9. To create a container named "node1," use the following command. If the container creation is successful, you will see the following output:
   ```diff
   sudo docker run -t -i --name node1 pc4_heapms:latest /bin/bash   
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/5f5c46d0-6cd5-4927-88c0-40f5b2585503)
10. To check if the container "node1" has the /docker_mount path, you can use the following command:
   ```diff
   ll  
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e102f704-bc7a-40c3-81e2-8d0de5dd5a49)
11. To check if the container "node1" has the /docker_mount path, you can use the following command:
   ```diff
   cd /docker_mount  
   ```
   ```diff
   ll  
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e6f4fbd7-514a-446f-b29f-e84890187978)
## Upload files
11. Next, use the 'cd' command to navigate to the directory /docker_mount/web/upload in order to prepare for uploading the data you want to execute.
   ```diff
   cd /web/upload 
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/d04eeec7-571c-4422-8f27-ee31ab2cdc7d)  
12. To upload a file, you need to use the following commands in your local terminal:
   ```diff
   sudo scp -P 22034 /home/brojack/Desktop/heapms_dataset/OSCC-1_time_intensity.tsv ccllab@120.126.17.213:/home/ccllab/Downloads 
   ```
   /home/brojack/Desktop/heapms_dataset/OSCC-1_time_intensity.tsv : Path of the file to be uploaded (local machine):
   ccllab@120.126.17.213:/home/ccllab/Downloads : Location where the file should be uploaded (remote machine):  
   #Because I'm using  a remote Ubuntu virtual machine, the IP address "120.126.17.213" represents the IP address of the virtual machine, and "22034" represents the port number of the virtual machine's IP.    
   The following image shows the execution result:
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/91ab04fe-538b-4e60-a4bd-14d7660df61e)  
   Afterward, you will be able to see the uploaded file in the '/Downloads' directory.
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/f19e3815-b42a-441f-9fbb-c107592205d7)  
13. After uploading all the files you want to execute, you need to move these files into the container "node1" that was created initially.
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/3945b14f-09d0-45ec-a8b8-668f9b1d55b2)  
14. Now, open a new terminal and connect to the previously created container "node1".
   ```diff
   sudo -s
   ```
   ```diff
   docker attach node1 
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/3653b33a-c497-4f92-a1a9-4c74936dfacb)  
15. Create a directory under /docker_mount/web/upload/ to store the files for execution.
   OSCC-1 : Folder name，You can name the folder whatever you like.
   ```diff
   mkdir OSCC-1 
   ```
   ```diff
   ll
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/aacbf30e-8a78-4e07-85cb-7f0c7b11785a)  
16. Move the data that needs to be executed from /Downloads to /docker_mount/web/upload/OSCC-1, which is the newly created folder named "OSCC-1".
   ```diff
   docker cp /home/ccllab/Downloads/OSCC-1_human.csv node1:/docker_mount/web/upload/OSCC-1/
   ```
   /Downlaods:  
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e86a7a28-6a2c-4ca8-89c1-4ebc0cdcd663)  
   /OSCC-1:  
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/8dc0e968-f4e1-47c1-9a0a-24972585233f)  
   After uploading all the files, the /OSCC-1 directory will contain the uploaded data, and you can proceed with running the program.
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/a03f9a7d-b654-422a-b4e5-31a47f845776)  
17. Before executing the program, you need to rename the three files in /OSCC-1 to the following names:
   ```diff
   mv OSCC-1_human.csv human.csv
   ```
   ```diff
   mv OSCC-1_skyline.csv skyline.csv
   ```
   ```diff
   mv OSCC-1_time_intensity.tsv time_intensity.tsv
   ```
   After renaming, the file names in /OSCC-1 will appear as shown in the following image:
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/9c3f69d7-0257-4f81-9246-c0215c4d6077)  
   #If the names of those three files are not modified, it will not be able to execute the program. 
## Start executing the program.  
18. Go back to the location /docker_mount/web/, and you will find the programs for execution inside.
   ```diff
   cd /docker_mount/web/
   ```
   ```diff
   ll
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/2bf42654-be3c-4fde-8d7d-ed5b723bc470)
19. Execute the program "exe.py".
   ```diff
   python3 exe.py upload OSCC-1
   ```
   exe.py : This program will automatically execute programs 1 to 13.
   upload OSCC-1: The files to be executed will be stored here.
   #If you want to execute each program one by one and see the output results, replace "exe.py" with the specific program you want to execute, as follows:
   ```diff
   python3 1_rmTQN_format_trans.py upload OSCC-1
   ```
   Path: /upload/OSCC-1, as shown in the following image:
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/d128d9d2-ed36-4db2-8f5c-56789ea860af)  
20. If it is displayed in a format similar to the image below, it means that the execution was successful.
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/a0229880-e151-4286-a927-04ff8ce78b11)

