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

./build_oai --ninja --gNB --nrUE -w SIMU -c  # compile gNB and nrUE 編譯gnb和nrUE
```

### Start the core network
```
cd ~/oai-cn5g
docker compose up -d
watch -n 1 docker compose -f docker-compose.yml ps -a #to check container health(確認容器都健康)
```
### Start the wireshak (optional)
```
sudo wireshark -k -i any -Y "ngap"
```
Run the gNB from a second terminal
### start the gNB
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
./nr-softmodem -O ~/oai-workshops/ran/conf/gnb.sa.band78.106prb.rfsim.conf --rfsim
```
When you establish the connection, you can see Setup Request and Setup Response messages in the Wireshark capture.
<img width="853" height="61" alt="image" src="https://github.com/user-attachments/assets/3f534e94-c030-405a-b7ec-8d5421a187e1" />

Run the nrUE from a third terminal
### start the nrUE
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
sudo ./nr-uesoftmodem -C 3619200000 -r 106 --numerology 1 --ssb 516 -O ~/oai-workshops/ran/conf/ue.conf --rfsim
```
You will see an output message: “Registration reject (Illegal UE)”.
<img width="1442" height="36" alt="image" src="https://github.com/user-attachments/assets/0ea6edc8-61c3-4ca0-b3c7-f73fa4aca7da" />

This means the AMF does not accept it because it does not recognize this identity. You can check the UE log.
```
  [SIM]   UICC simulation: IMSI=001010000000101, ... DNN=oai, SST=0x01, SD=0xffffff
```
It means that the UE identity is IMSI = 001010000000101.

Check amf log
```
docker logs oai-amf --tail 50
```
You will see
<img width="1165" height="767" alt="螢幕擷取畫面 2025-11-25 154601" src="https://github.com/user-attachments/assets/31a658fc-0d3f-4afd-9784-7e5645bd2471" />

You can see that the UE IMSI currently recognized by the AMF is 001010000000001

The UE is using 001010000000101.

In the core (subscriber DB / AMF), there is only 001010000000001.

When an IMSI that is not in the DB tries to register, the AMF will, according to the standard, return:

Registration reject, cause = Illegal UE.

#### Solution (quick way to get it running)

Copy the ue.conf file, rename it to ue_test1.conf, and change the IMSI inside to 001010000000001.

<img width="415" height="131" alt="image" src="https://github.com/user-attachments/assets/f957b865-0a92-449e-a7f4-23cf4b50eb39" />

Re run
```
cd ~/openairinterface5g/cmake_targets/ran_build/build
sudo ./nr-uesoftmodem -C 3619200000 -r 106 --numerology 1 --ssb 516 -O ~/oai-workshops/ran/conf/ue_test1.conf --rfsim
```
Then the connection will succeed, and the Wireshark capture will look like this:

<img width="1809" height="264" alt="螢幕擷取畫面 2025-11-25 190112" src="https://github.com/user-attachments/assets/bc7c591e-0422-49cb-b6ae-cdb872e82946" />

### Inject traffic
#### Installation of dependencies(iperf3)
```
cd ~
sudo apt update
sudo apt install iperf3
```
Check the UE's IP address on interface oaitun_ue1 using:
```
ip address show oaitun_ue1
```
The IP address 192.168.70.135 is the address of the oai-ext-dn container.

Ping test:

  UL
  ```
  ping -I oaitun_ue1 192.168.70.135
  ```
  DL
  ```
  docker exec -it oai-ext-dn ping <UE IP address>
  ```
  
Iperf3 test:
Iperf3 can be used to test UL and DL throughput between the oai-ext-dn (in Docker) and the UE (running locally):
  
start the iperf3 server inside the container:
```
docker exec -it oai-ext-dn bash -c "iperf3 -s"
```
On the host, in a new terminal, run the iperf3 client and bind the UE IP address:
```
iperf3 -B <UE IP ADDRESS> -c 192.168.70.135 -u -b 50M -R # DL
iperf3 -B <UE IP ADDRESS> -c 192.168.70.135 -u -b 20M    # UL
```

#### result
ping test:
UE ip address 10.0.0.2

UL
<img width="1024" height="359" alt="image" src="https://github.com/user-attachments/assets/3554f69d-a9d5-4ea7-a45a-1821cb1cecd6" />

DL
<img width="1072" height="396" alt="image" src="https://github.com/user-attachments/assets/a809cd4d-69ef-4d60-bf6f-29a70e009c01" />

Iperf3 test:
<img width="1120" height="65" alt="image" src="https://github.com/user-attachments/assets/e29051d9-ce24-4d47-85ad-585a1995a0c1" />

<img width="1133" height="336" alt="image" src="https://github.com/user-attachments/assets/418c1389-3f49-4f7d-b58d-d880d3866c7b" />




### Troubleshooting

#### Error message: Insufficient permissions
```
Assertion (file!=((void *)0)) failed!
In nrmac_stats_thread() /home/kuan/openairinterface5g/openair2/LAYER2/NR_MAC_gNB/main.c:57
Cannot open nrMAC_stats.log, error Permission denied
```
It is likely that you previously ran the program with sudo and accidentally created some files as root, which then caused insufficient permissions later so the program could not be started

Solution
```
sudo chown -R kuan:kuan ~/openairinterface5g #將整個專案改回來
```
#### Error message: UE or gNB has been paused (you pressed Ctrl+Z instead of Ctrl+C)
```
ps aux | grep nr-softmodem
ps aux | grep nr-uesoftmodem
```
You can check whether there are any paused UEs or gNBs.
<img width="913" height="70" alt="image" src="https://github.com/user-attachments/assets/54e2457b-00df-46a3-8556-94980e7073d9" />
Normally, there should be only one process and its state should start with “S”. There should not be any extra ones whose state starts with “T”.
<img width="1358" height="60" alt="image" src="https://github.com/user-attachments/assets/50c939f1-305e-4378-a9bc-ac8876b79aec" />
please delete the gNB using the following commands (run them in order; if one doesn’t work, try the next).
```
pkill nr-softmodem
kill 81257 81258
kill -9 81257 81258
```
<img width="1617" height="84" alt="image" src="https://github.com/user-attachments/assets/ea5800aa-9386-4dd1-93ab-b98f5772aab5" />

For the UE, delete it using the following commands (run them in order; if one doesn’t work, try the next).
```
sudo pkill -9 nr-uesoftmodem
sudo pkill -9 -f "sudo ./nr-uesoftmodem"
```

### In the UE log, you should see these key steps

Initial synchronization succeeded
```
[PHY] Initial sync successful, PCI: 0
[PHY] UE synchronized!
```
RA succeeded and UE enters RRC_CONNECTED
```
[MAC] RA procedure succeeded. CB-RA: Contention Resolution is successful.
[NR_RRC] State = NR_RRC_CONNECTED
```
Security Mode, Capability exchange, and Registration Accept are completed

UE sends RegistrationComplete and PduSessionEstablishRequest
```
[NAS] Send NAS_UPLINK_DATA_REQ message(RegistrationComplete)
[NAS] Send NAS_UPLINK_DATA_REQ message(PduSessionEstablishRequest)
```

This means:
The RRC attach, NAS Registration, and PDU Session establishment procedures have all completed — the procedure is successful.


