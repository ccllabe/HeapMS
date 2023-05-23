# HeapMS-Installation-Process
首先在你的Ubuntu環境下開啟terminal，接著執行以下所有指令及操作:
1. 更新  
   <span style="color:red;">sudo apt-get update  </span>
3. 移除舊有的docker環境  
   sudo apt-get remove docker docker-engine docker.io  
3. 安裝新的docker環境  
   sudo apt install docker.io  
4. 執行docker環境  
   sudo service docker start  
   做到這裡，你就可以執行docker指令了!
   ![image](https://github.com/ccllabe/HeapMS-Installation-Process/assets/134360047/b48a5e90-ceec-4df7-a1bd-99485926fb62)
5. 找出pc4_heapms.tar這個檔案在你的電腦儲存的位置絕對路徑
   realpath pc4_heapms.tar
6. 
