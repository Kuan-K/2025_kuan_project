# NTN_exercise.

> Reference :
> - [5G RAN Workshop 2025](https://gitlab.eurecom.fr/oai/trainings/oai-workshops/-/tree/main/ran)
> - https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn-leo.conf
> - https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/ci-scripts/conf_files/nrue.uicc.ntn-leo.conf

### system architecture

![arc](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%9E%B6%E6%A7%8B%E5%9C%96F.png)
### check the ip address about CN and gNB

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

### Change the gNB configuration
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
### start the gNB with (NTN-LEO example 官方)
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
./nr-softmodem --rfsim -O ../../../ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn-leo-copy.conf
```

### Start the nrUE

Run the nrUE from a third terminal
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
./nr-uesoftmodem -O ../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 20 --rfsimulator.options chanmod --time-sync-I 0.1 --ntn-initial-time-drift -46 --initial-fo 57340 --cont-fo-comp 2
```

### result





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


### 模組與程式碼參數對照方塊圖
<img width="771" height="800" alt="方塊對照圖" src="https://github.com/user-attachments/assets/1df78cf6-6bc4-44ca-bf96-9948ca63449c" />



### log 關鍵訊息

 
