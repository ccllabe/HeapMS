# HeapMS-Installation-Process
首先在你的Ubuntu環境下開啟terminal，接著執行以下所有指令及操作:
## 安裝環境   
1. 更新  
   ```diff
   sudo apt-get update  
   ```
2. 移除舊有的docker環境  
   ```diff
   sudo apt-get remove docker docker-engine docker.io   
   ```
3. 安裝新的docker環境  
   ```diff
   sudo apt install docker.io   
   ```
4. 執行docker環境  
   ```diff
   sudo service docker start    
   ```
   做到這裡，你就可以執行docker指令了!
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/b48a5e90-ceec-4df7-a1bd-99485926fb62)
5. 找出pc4_heapms.tar這個檔案在你的電腦儲存的位置絕對路徑  
   下載 pc4_heapms.tar (file size: ~60GB): (https://onedrive.live.com/?authkey=%21AO8kOvVhBSEuxZc&id=7309231C4353D1C0%21447583&cid=7309231C4353D1C0&parId=root&parQt=sharedby&o=OneUp) 
   ```diff
   realpath pc4_heapms.tar    
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/ab24823c-d153-4bde-bd3f-052551412e32)
6. 將pc4_heapms.tar製作成docker image
   ```diff
   docker load < /home/ccllab/Downloads/pc4_heapms.tar    
   ```
   執行完後會如同以下:
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/5924ad5e-039a-4f8a-a5f4-6ac92103ce80)
7. 查看pc4_heapms.tar有沒有成功製作成docker image
   ```diff
   docker images   
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/87472e98-b8c2-46c8-8982-98961e8e4051)
8. 創建一個名為node1的container，若成功創建container: node1，則會顯示以下內容
   ```diff
   sudo docker run -t -i --name node1 pc4_heapms:latest /bin/bash   
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/5f5c46d0-6cd5-4927-88c0-40f5b2585503)
9. 查看該container: node1 是否有/docker_mount這個路徑
   ```diff
   ll  
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e102f704-bc7a-40c3-81e2-8d0de5dd5a49)
10. 使用以下兩個指令，檢查/docker_mount是否有以下模型及路徑
   ```diff
   cd /docker_mount  
   ```
   ```diff
   ll  
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e6f4fbd7-514a-446f-b29f-e84890187978)
## 上傳檔案  
11. 接下來cd到這個目錄/docker_mount/web/upload，準備上傳要執行的data
   ```diff
   cd /web/upload 
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/d04eeec7-571c-4422-8f27-ee31ab2cdc7d)  
12. 上傳檔案，以下指令需要在(本機端的terminal輸入)
   ```diff
   sudo scp -P 22034 /home/brojack/Desktop/heapms_dataset/OSCC-1_time_intensity.tsv ccllab@120.126.17.213:/home/ccllab/Downloads 
   ```
   /home/brojack/Desktop/heapms_dataset/OSCC-1_time_intensity.tsv : 要上傳的檔案路徑(本機端)
   ccllab@120.126.17.213:/home/ccllab/Downloads : 檔案要上傳到哪裡(遠端)  
   #由於我是使用遠端的Ubuntu虛擬機，因此120.126.17.213為虛擬機的ip，22034為虛擬機ip的port number    
   以下圖片為執行結果
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/91ab04fe-538b-4e60-a4bd-14d7660df61e)  
   接著在/Downloads 裡就能看到剛剛傳的檔案
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/f19e3815-b42a-441f-9fbb-c107592205d7)  
13. 上傳完所有要執行的檔案後，就要把這些檔案移動到一開始建立的container: node1內了
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/3945b14f-09d0-45ec-a8b8-668f9b1d55b2)  
14. 現在開一個新的terminal，連到剛建立好的container: node1
   ```diff
   sudo -s
   ```
   ```diff
   docker attach node1 
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/3653b33a-c497-4f92-a1a9-4c74936dfacb)  
15. 在/docker_mount/web/upload/下建立一個資料夾，用來儲存要執行的檔案
   OSCC-1 : 資料夾名稱，想要叫什麼都可以
   ```diff
   mkdir OSCC-1 
   ```
   ```diff
   ll
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/aacbf30e-8a78-4e07-85cb-7f0c7b11785a)  
16. 把/Downlaods內要執行的資料移動到/docker_mount/web/upload/OSCC-1，即剛剛建立的OSCC-1資料夾內
   ```diff
   docker cp /home/ccllab/Downloads/OSCC-1_human.csv node1:/docker_mount/web/upload/OSCC-1/
   ```
   /Downlaods:  
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/e86a7a28-6a2c-4ca8-89c1-4ebc0cdcd663)  
   /OSCC-1:  
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/8dc0e968-f4e1-47c1-9a0a-24972585233f)  
   都上傳完檔案後，/OSCC-1裡面就會有這些資料，就可以開始跑程式了
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/a03f9a7d-b654-422a-b4e5-31a47f845776)  
17. 在執行程式前，需要將/OSCC-1裡的那三個檔案改名，改成以下名稱
   ```diff
   mv OSCC-1_human.csv human.csv
   ```
   ```diff
   mv OSCC-1_skyline.csv skyline.csv
   ```
   ```diff
   mv OSCC-1_time_intensity.tsv time_intensity.tsv
   ```
   改完後會像下面這張圖片一樣的檔案名稱
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/9c3f69d7-0257-4f81-9246-c0215c4d6077)  
   #若沒有修改那三個檔案名稱，就會無法執行程式!  
## 開始執行程式  
18. 回到 /docker_mount/web/ 的位置，裡面會有這些執行的程式
   ```diff
   cd /docker_mount/web/
   ```
   ```diff
   ll
   ```
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/2bf42654-be3c-4fde-8d7d-ed5b723bc470)
19. 執行exe.py這隻程式
   ```diff
   python3 exe.py upload OSCC-1
   ```
   exe.py : 這支程式會自動執行1-13支程式。
   upload OSCC-1: 儲存要執行的檔案位置。
   #若想要一支一支程式執行看輸出結果，就將exe.py換成要執行的那隻程式，如下:
   ```diff
   python3 1_rmTQN_format_trans.py upload OSCC-1
   ```
   路徑/upload/OSCC-1，如下圖
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/d128d9d2-ed36-4db2-8f5c-56789ea860af)  
20. 有顯示成下面這張圖的樣子，就代表執行成功了
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/a0229880-e151-4286-a927-04ff8ce78b11)

