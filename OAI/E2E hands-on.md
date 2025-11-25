# OAI E2E hands-on

> Reference :
> - [5G RAN Workshop 2025](https://gitlab.eurecom.fr/oai/trainings/oai-workshops/-/tree/main/ran)

### Installation of dependencies and compilation(安裝相依套件與編譯)
```
cd ~
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git
cd openairinterface5g
git checkout 2025.w46                        # tested tag
cd cmake_targets
./build_oai --ninja -I                       # install dependencies

./build_oai --ninja --gNB --nrUE -w SIMU -c  # compile gNB and nrUE #編譯gnb和nrUE
```

### 開啟CN5G
```
cd ~/oai-cn5g
docker compose up -d
watch -n 1 docker compose -f docker-compose.yml ps -a #確認容器都健康
```
### 開啟wireshark(擷取ngap)
```
sudo wireshark -k -i any -Y "ngap"
```
開啟另一個終端機
### 啟gNB
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
./nr-softmodem -O ~/oai-workshops/ran/conf/gnb.sa.band78.106prb.rfsim.conf --rfsim
```
連線時會看到wireshark畫面有Setup Request and Response messages
<img width="853" height="61" alt="image" src="https://github.com/user-attachments/assets/3f534e94-c030-405a-b7ec-8d5421a187e1" />

再開啟另一個終端機
### 啟UE
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
sudo ./nr-uesoftmodem -C 3619200000 -r 106 --numerology 1 --ssb 516 -O ~/oai-workshops/ran/conf/ue.conf --rfsim
```
會看到輸出有Registration reject (Illegal UE)
<img width="1442" height="36" alt="image" src="https://github.com/user-attachments/assets/0ea6edc8-61c3-4ca0-b3c7-f73fa4aca7da" />

代表說 AMF 不接受因為AMF不認得這個身分，可以查看UE log有一行
```
  [SIM]   UICC simulation: IMSI=001010000000101, ... DNN=oai, SST=0x01, SD=0xffffff
```
代表UE 身份是 IMSI=001010000000101

查看amf log
```
docker logs oai-amf --tail 50
```
會看到類似
<img width="1165" height="767" alt="螢幕擷取畫面 2025-11-25 154601" src="https://github.com/user-attachments/assets/31a658fc-0d3f-4afd-9784-7e5645bd2471" />
可以看到AMF 目前認得的 UE IMSI 是：001010000000001

UE 拿的是 001010000000101

Core（subscriber DB / AMF）裡只有 001010000000001

當一個「DB 裡沒有的 IMSI」來註冊時，AMF 就會按標準回：

Registration reject, cause = Illegal UE

#### 解決方法(快速讓他能跑通)
Copy 一個ue.conf檔 改叫ue_test1.conf 並將裡面的ISMI改為"001010000000001" 
<img width="415" height="131" alt="image" src="https://github.com/user-attachments/assets/f957b865-0a92-449e-a7f4-23cf4b50eb39" />

重新執行
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
sudo ./nr-uesoftmodem -C 3619200000 -r 106 --numerology 1 --ssb 516 -O ~/oai-workshops/ran/conf/ue_test1.conf --rfsim
```
就會成功連線看到wireshark畫面為
<img width="1809" height="264" alt="螢幕擷取畫面 2025-11-25 190112" src="https://github.com/user-attachments/assets/bc7c591e-0422-49cb-b6ae-cdb872e82946" />



### 錯誤排查

#### 錯誤資訊:權限不足
```
Assertion (file!=((void *)0)) failed!
In nrmac_stats_thread() /home/kuan/openairinterface5g/openair2/LAYER2/NR_MAC_gNB/main.c:57
Cannot open nrMAC_stats.log, error Permission denied
```
很可能是用sudo跑程式不小心使用sudo建檔導致後續權限不足開不了

解決方法
```
sudo chown -R kuan:kuan ~/openairinterface5g #將整個專案改回來
```
#### 錯誤資訊:UE或gNB被暫停(按到ctrl+z而不是ctrl+c)
```
ps aux | grep nr-softmodem
ps aux | grep nr-uesoftmodem
```
可以查看是否有被暫停的UE或gNB
<img width="913" height="70" alt="image" src="https://github.com/user-attachments/assets/54e2457b-00df-46a3-8556-94980e7073d9" />
正常應該都只有一個並且是 S 開頭，如果有多餘的(T)開頭的
<img width="1358" height="60" alt="image" src="https://github.com/user-attachments/assets/50c939f1-305e-4378-a9bc-ac8876b79aec" />
gNB請用以下程式刪除(依序用，刪不掉再接著用)
```
pkill nr-softmodem
kill 81257 81258
kill -9 81257 81258
```
<img width="1617" height="84" alt="image" src="https://github.com/user-attachments/assets/ea5800aa-9386-4dd1-93ab-b98f5772aab5" />

UE請用以下程式刪除(依序用，刪不掉再接著用)
```
sudo pkill -9 nr-uesoftmodem
sudo pkill -9 -f "sudo ./nr-uesoftmodem"
```

### UE log 裡，有這些關鍵步驟
初始同步成功
```
[PHY] Initial sync successful, PCI: 0
[PHY] UE synchronized!
```
RA 成功、進 RRC_CONNECTED
```
[MAC] RA procedure succeeded. CB-RA: Contention Resolution is successful.
[NR_RRC] State = NR_RRC_CONNECTED
```
做完 Security Mode、Capability、Registration Accept

傳了 RegistrationComplete 和 PduSessionEstablishRequest
```
[NAS] Send NAS_UPLINK_DATA_REQ message(RegistrationComplete)
[NAS] Send NAS_UPLINK_DATA_REQ message(PduSessionEstablishRequest)
```

這表示：
RRC attach、NAS Registration、PDU Session 建立流程都有跑完，是成功的。
