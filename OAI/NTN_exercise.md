# OAI NTN E2E hands-on

> Reference :
> - [5G RAN Workshop 2025](https://gitlab.eurecom.fr/oai/trainings/oai-workshops/-/tree/main/ran)
> - https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn-leo.conf
> - https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/ci-scripts/conf_files/nrue.uicc.ntn-leo.conf

## system architecture

![arc](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%9E%B6%E6%A7%8B%E5%9C%96F.png)
## check the ip address about CN and gNB

Use the following command to find the IP address.
```
cd ~
ip addr
```
*** output (you might see output like this)

<img width="1051" height="761" alt="image" src="https://github.com/user-attachments/assets/fce33ff3-9f5b-4c5d-bc4d-7ed965bfc729" />

OAI CN5G bridge oai-cn5g : 192.168.70.129/26

Use the following command to find the amf IP address.
```
docker ps        # 找 amf 那個 container 名字
docker inspect <amf-container-name> | grep "IPAddress"
```
*** output (you might see output like this)
<img width="1730" height="283" alt="image" src="https://github.com/user-attachments/assets/478a95ca-99b3-4e76-9b37-62a0e8e0e55c" />

amf_ip_addres = 192.168.70.132

## Change the gNB configuration
First, make a copy of gnb.sa.band254.u0.25prb.rfsim.ntn-leo.conf. Then open the copied file, find the code shown above
```
    # ------- SCTP definitions
    SCTP :
    {
        # Number of streams to use in input/output
        SCTP_INSTREAMS  = 2;
        SCTP_OUTSTREAMS = 2;
    };


    ////////// AMF parameters:
    amf_ip_address = ({ ipv4 = "192.168.71.132"; });

    NETWORK_INTERFACES :
    {
        GNB_IPV4_ADDRESS_FOR_NG_AMF              = "192.168.71.140/26";
        GNB_IPV4_ADDRESS_FOR_NGU                 = "192.168.71.140/26";
        GNB_PORT_FOR_S1U                         = 2152; # Spec 2152
    };
```
Modify the following two parts

GNB_IPV4_ADDRESS_FOR_NG_AMF/NGU = OAI CN5G bridge oai-cn5g

 amf_ip_address = amf_ip_addres
## start the gNB with (NTN-LEO example 官方)
```
cd ~/openairinterface5g/cmake_targets

sudo ./ran_build/build/nr-softmodem -O ../ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn.conf --rfsim #GEO執行這行

sudo ./ran_build/build/nr-softmodem -O ../ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn-leo-copy.conf #LEO執行這行


```

### Start the nrUE

Run the nrUE from a third terminal
```
cd ~/openairinterface5g/cmake_targets

sudo ./ran_build/build/nr-uesoftmodem -O ../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 238.74 # GEO執行這行

sudo ./ran_build/build/nr-uesoftmodem -O ../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 20 --rfsimulator.options chanmod --time-sync-I 0.1 --ntn-initial-time-drift -46 --initial-fo 57340 --cont-fo-comp 2 #LEO執行這行
```

## result

### GEO

#### ping test
UE to DN (UL,RTN)

<img width="760" height="287" alt="image" src="https://github.com/user-attachments/assets/4326720f-4fb5-4c6b-a1b4-dc68fae21c4f" />

DN to UE (DL,FWR)

<img width="638" height="287" alt="image" src="https://github.com/user-attachments/assets/aac8d2ce-4159-424b-a99a-bd377c07e96a" />

#### iperf3
UE to DN (UL,RTN)

<img width="791" height="381" alt="image" src="https://github.com/user-attachments/assets/69f85534-ea3c-4d7c-8d88-1e421b7b9ea3" />

DN to UE (DL,FWR)

<img width="801" height="360" alt="image" src="https://github.com/user-attachments/assets/665cc911-edf9-4f27-8cd4-cb4dcb062c4c" />

[note] 設定 -b 8Mbps 是因為GEO 模擬環境頻寬上限就大概在 8-10 Mbps 左右 已使用 -50M確認過

### LEO

*** output (UE log)
```
[PHY]    Initial sync: pbch decoded sucessfully, ssb index 0
[PHY]    pbch rx ok. rsrp:51 dB/RE, adjust_rxgain:-1 dB
[NR_PHY] Cell Detected with GSCN: 0, SSB SC offset: 60
...
[PHY]    UE synchronized! decoded_frame_rx=686 ...
[NR_RRC] SIB1 decoded
[NR_RRC] Found SIB2
[NR_RRC] Found SIB19
```
This means:
  1. Cell search and synchronization succeeded ✅
     * The gNB’s SSB was found
     * The frequency offset and timing offset were measured and corrected.
  2. MIB/SIB1/SIB2/SIB19 were successfully decoded ✅
     * The UE has already obtained the system information (including the RACH configuration, frequency allocation, NTN timing offset, etc.)
       
So at this point, the PHY and the RRC system information are completely fine; the gNB is definitely transmitting, and you are receiving it correctly.

Next, you will see a large number of repeated messages:
```
[MAC]    Initialization of 4-Step CBRA procedure
[NR_MAC] PRACH scheduler: Selected RO Frame ...
[PHY]    PRACH [UE 0] in frame.slot ... preambleIndex = XX
[MAC]    [UE 0] RAR reception failed
```
sometimes
```
[PHY]    [UE 0] RAR-Msg2 decoded
[NR_MAC] ... Got BI RAR subPDU 5 ms
[NR_MAC] ... Got RAPID RAR subPDU
[NR_MAC] ... Received RAR preamble (6) doesn't match the intended RAPID (28)
[MAC]    [UE 0] RAR reception failed
```
This part is doing the 4-step Random Access procedure:
  1. The UE sends Msg1 (preamble) on the PRACH resources.In the log, that’s the line like:PRACH [UE 0] ... preambleIndex = XX
  2. The gNB should reply with Msg2 (RAR, Random Access Response).
  3. After the UE receives the RAR, it checks whether the preamble index (RAPID) inside the RAR is the same as the one it sent.
     * If it matches → success, move on to the next step (send RRC Connection Request).
     * If it doesn’t match / nothing is received → treat it as a failure and try again.
These two cases appear in the log.
  * RAR not received:
    
    → RAR reception failed
    
  * RAR received but preamble doesn’t match:
    
    → Received RAR preamble (xx) doesn't match the intended RAPID (yy)
    
    → This means that RAR is “for someone else,” not for this UE.

This is because, in NTN scenario, there is a large NTN delay and a more complex RACH mapping relationship.

You can see this line:
```
[PHY] k_offset = 40 ms (40 slots), total_ta_ms ≈ 37 ms, computed timing_advance ≈ 28x000 samples
```
This means the system is taking into account a ~238 ms propagation delay,
but the RACH/RAR mapping can still fail to match the preamble because of timing offsets.
### 在核網新增新的UE資訊 (以更改 IMSI = '0010100007487' 其他key opc等都不變為例)
1. 進入MySQL 容器
```
docker exec -it mysql mariadb -u root -p
mysql -u root -p # 預設密碼為linux

USE oai_db; # 切換至 oai 資料庫
```
2. 可以先進入核網的資料夾確認 UE 的格式(oai-cn5g/docker-compose/database/oai_db.sql)
   
```
--
-- Dumping data for table `AuthenticationSubscription`
--

INSERT INTO `AuthenticationSubscription` (`ueid`, `authenticationMethod`, `encPermanentKey`, `protectionParameterId`, `sequenceNumber`, `authenticationManagementField`, `algorithmId`, `encOpcKey`, `encTopcKey`, `vectorGenerationInHss`, `n5gcAuthMethod`, `rgAuthenticationInd`, `supi`) VALUES
    ('001010000000001', '5G_AKA', 'fec86ba6eb707ed08905757b1bb44b8f', 'fec86ba6eb707ed08905757b1bb44b8f', '{\"sqn\": \"000000000000\", \"sqnScheme\": \"NON_TIME_BASED\", \"lastIndexes\": {\"ausf\": 0}}', '8000', 'milenage', 'C42449363BBAD02B66D16BC975D77CC1', NULL, NULL, NULL, NULL, '001010000000001');
INSERT INTO `AuthenticationSubscription` (`ueid`, `authenticationMethod`, `encPermanentKey`, `protectionParameterId`, `sequenceNumber`, `authenticationManagementField`, `algorithmId`, `encOpcKey`, `encTopcKey`, `vectorGenerationInHss`, `n5gcAuthMethod`, `rgAuthenticationInd`, `supi`) VALUES
    ('001010000000002', '5G_AKA', 'fec86ba6eb707ed08905757b1bb44b8f', 'fec86ba6eb707ed08905757b1bb44b8f', '{\"sqn\": \"000000000000\", \"sqnScheme\": \"NON_TIME_BASED\", \"lastIndexes\": {\"ausf\": 0}}', '8000', 'milenage', 'C42449363BBAD02B66D16BC975D77CC1', NULL, NULL, NULL, NULL, '001010000000002');
INSERT INTO `AuthenticationSubscription` (`ueid`, `authenticationMethod`, `encPermanentKey`, `protectionParameterId`, `sequenceNumber`, `authenticationManagementField`, `algorithmId`, `encOpcKey`, `encTopcKey`, `vectorGenerationInHss`, `n5gcAuthMethod`, `rgAuthenticationInd`, `supi`) VALUES
    ('001010000000003', '5G_AKA', 'fec86ba6eb707ed08905757b1bb44b8f', 'fec86ba6eb707ed08905757b1bb44b8f', '{\"sqn\": \"000000000000\", \"sqnScheme\": \"NON_TIME_BASED\", \"lastIndexes\": {\"ausf\": 0}}', '8000', 'milenage', 'C42449363BBAD02B66D16BC975D77CC1', NULL, NULL, NULL, NULL, '001010000000003');
INSERT INTO `AuthenticationSubscription` (`ueid`, `authenticationMethod`, `encPermanentKey`, `protectionParameterId`, `sequenceNumber`, `authenticationManagementField`, `algorithmId`, `encOpcKey`, `encTopcKey`, `vectorGenerationInHss`, `n5gcAuthMethod`, `rgAuthenticationInd`, `supi`) VALUES
    ('001010000000004', '5G_AKA', 'fec86ba6eb707ed08905757b1bb44b8f', 'fec86ba6eb707ed08905757b1bb44b8f', '{\"sqn\": \"000000000000\", \"sqnScheme\": \"NON_TIME_BASED\", \"lastIndexes\": {\"ausf\": 0}}', '8000', 'milenage', 'C42449363BBAD02B66D16BC975D77CC1', NULL, NULL, NULL, NULL, '001010000000004');

```

3. 新增身分驗證資料 (Authentication)

   增加key與 opc
```
INSERT INTO AuthenticationSubscription (ueid, authenticationMethod, encPermanentKey, protectionParameterId, sequenceNumber, authenticationManagementField, algorithmId, encOpcKey, supi)
SELECT '0010100007487', authenticationMethod, encPermanentKey, protectionParameterId, sequenceNumber, authenticationManagementField, algorithmId, encOpcKey, '0010100007487'
FROM AuthenticationSubscription WHERE ueid = '001010000000001';
```
4. 新增接入與移動性資料 (Access & Mobility)
   
```
INSERT INTO AccessAndMobilitySubscriptionData (ueid, servingPlmnId, gpsis, internalGroupIds, sharedVnGroupDataIds, nssai)
SELECT '0010100007487', servingPlmnId, gpsis, internalGroupIds, sharedVnGroupDataIds, nssai
FROM AccessAndMobilitySubscriptionData WHERE ueid = '001010000000001';
```

5. 新增會話管理資料 (Session Management)
 
```
INSERT INTO SessionManagementSubscriptionData (ueid, servingPlmnId, singleNssai, dnnConfigurations)
SELECT '0010100007487', servingPlmnId, singleNssai, dnnConfigurations
FROM SessionManagementSubscriptionData WHERE ueid = '001010000000001'
   ```
6. 驗證結果

<img width="1451" height="437" alt="image" src="https://github.com/user-attachments/assets/d93985c5-807a-4b31-b30e-f3dc4dfb86e3" />

可以看到IMSI = '0010100007487' 的UE已經可以跑通了

7. 查看有哪些UE資訊合法(option)

```
USE oai_db;

SELECT 
    ueid AS IMSI, 
    encPermanentKey AS 'Key (K)', 
    encOpcKey AS OPc 
FROM AuthenticationSubscription;
```

<img width="811" height="278" alt="image" src="https://github.com/user-attachments/assets/a44d4a4f-172c-442a-998b-c8af6d5b2a06" />



### log 資訊
 #### gNB
 ##### 在正常情況下
 
<img width="803" height="218" alt="image" src="https://github.com/user-attachments/assets/d694c685-f8e1-4d66-9da0-dd0718af3a80" />

從
```
[NGAP]   Send NGSetupRequest to AMF
[NGAP]   Received NGSetupResponse from AMF
```
可以看到 NGAP 的連線

<img width="1331" height="694" alt="image" src="https://github.com/user-attachments/assets/18f68959-baf4-47c4-a1e4-04faa8dc04ba" />

從第一行 可以對照參數是否正確

從第二行可以看到gNB 成功偵測到 UE 發出的 Preamble（編號 24），代表 UE 已經同步並嘗試連線。

從第六行可以看到gNB 發出 Msg2 (Random Access Response)

在圖片中間Received Ack of Msg4.可以看出競爭隨機接入 (CBRA) 正式成功。這意味著 物理層與 MAC 層的握手已完成，UE 正式與基地台連上。
##### 錯誤排查

#### UE
<img width="1202" height="687" alt="螢幕擷取畫面 2026-01-12 210820" src="https://github.com/user-attachments/assets/3eb48ae8-38d3-4288-b6a8-13c58f753c2e" />

Initial sync: pbch decoded successfully: 初始同步成功，成功解碼實體廣播通道 (PBCH)。

Initial sync successful, PCI: 0: 初始同步完成。

Found SIB1/SIB2/SIB19:偵測到 SIB1/SIB2/SIB19。

[NR_MAC] [UE 0][RAPROC][882.6] Found RAR with the intended RAPID 59:UE 確認收到了正確的 RAR 回應。

[MAC]    [UE 0][932.3][RAPROC] 4-Step RA procedure succeeded. CBRA: Contention Resolution is successful.:四步式隨機接入成功。代表 UE 與 gNB 已經在 MAC 層連上線了。

<img width="903" height="53" alt="image" src="https://github.com/user-attachments/assets/cc7b0bf1-3514-4e59-86e4-8483ba5a9caf" />

代表上行鏈路穩定 70/0 代表發送了 70 個封包，錯誤為 0
