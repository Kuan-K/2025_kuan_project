# Study Note: multiple UE

> Reference :
> 
>   https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/NR_SA_Tutorial_OAI_multi_UE.md?ref_type=heads
> 
>   https://gitlab.eurecom.fr/oai/trainings/oai-workshops/-/tree/main/ran#exercise
> 

## TOC
1. telnet
2. multi UE (TN)
3. multi UE (NTN)

---

## 1 telnet

### 摘要
telnet 像是一個儀表板，負責觀察與傳遞資訊，並可以動態修改一些參數不用重啟就可調整

### 編譯 Telnet 資料庫
```
 cd ~/openairinterface5g
 source oaienv
 cd cmake_targets
 ./build_oai  --build-lib telnetsrv
```

### 相關參數

| 參數名稱 | 類型 | 預設值 | 功能 | 是否可做動態更改 |
|:---:|:---:|:---:|:----|:----:|
| `listenaddr` | `ipV4 位址` | "0.0.0.0" | 伺服器監聽的本地位址| N |
| `listenport` | `整數` | 9090 | 伺服器監聽的連接埠號 | N |
| `listenstdin` | `布林`  | 0 | enable input from stdin via additional thread | N |
| `policy` | `整數` | 0 | Telnet 的調度優先級 (0-99) | N |
| `loopcount` | `整數` | 10 | loop 命令的次數  | Y |
| `loopdelay` | `整數` | 5000 | loop 命令之間的延遲 (ms)  | Y |
| `staticmod`  | `字串` | (empty) | 啟動時加載的額外內建 Telnet 模組 | N |
| `shrmod`  | `字串` | (empty) | 啟動時加載的額外共享對象檔案 | N |

## 2 multi UE (NTN_LEO)

```
sudo ./multi-ue.sh -c1
sudo ./multi-ue.sh -o1
```

```
sudo /home/kuan/openairinterface5g/cmake_targets/ran_build/build/nr-uesoftmodem -O /home/kuan/openairinterface5g/targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 20 --rfsimulator.options chanmod --time-sync-I 0.1 --ntn-initial-time-drift -46 --initial-fo 57340 --cont-fo-comp 2 --uicc0.imsi 001010000000001 --rfsimulator.options chanmod --rfsimulator.serveraddr 10.201.1.100 --telnetsrv --telnetsrv.listenport 9095
```

```
sudo ./multi-ue.sh -c2
sudo ./multi-ue.sh -o2
```

```
sudo /home/kuan/openairinterface5g/cmake_targets/ran_build/build/nr-uesoftmodem -O /home/kuan/openairinterface5g/targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 20 --rfsimulator.options chanmod --time-sync-I 0.1 --ntn-initial-time-drift -46 --initial-fo 57340 --cont-fo-comp 2 --uicc0.imsi 001010000000002 --rfsimulator.options chanmod --rfsimulator.serveraddr 10.202.1.100 --telnetsrv --telnetsrv.listenport 9096
```

### amf log
<img width="1225" height="746" alt="image" src="https://github.com/user-attachments/assets/4e7d36be-1b00-475a-b210-bb304867517a" />

### ifconfig
<img width="557" height="309" alt="image" src="https://github.com/user-attachments/assets/f3f035fb-fc9f-4b7a-9f2f-aa1b212f7670" />
