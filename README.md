# HeapMS-Installation-Process
首先在你的Ubuntu環境下開啟terminal，接著執行以下所有指令及操作:
1. 更新  
   ```diff
   sudo apt-get update  
   ```
3. 移除舊有的docker環境  
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
14. rrr
