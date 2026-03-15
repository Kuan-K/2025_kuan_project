# installation : OAI CN5G

> Reference :
> - [free5GC compose](https://github.com/calee0219/free5gc-docker-compose)
>
> - [gtp5g](https://github.com/free5gc/gtp5g)
>
> - [installation note](https://hackmd.io/@Yueh-Huan/S1eC0g3Gi#Free5GC-Installation-Guide)


請先安裝[docker](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/oaicn5g%20built%20environment_.md#install-docker-engine-and-the-docker-compose-plugin)

## pull socker image
```
docker compose pull
```

## Build docker images
```
# Clone the project
git clone https://github.com/free5gc/free5gc-compose.git
cd free5gc-compose

# clone free5gc sources
cd base
git clone --recursive -j `nproc` https://github.com/free5gc/free5gc.git
cd ..

# Build the images
make all
docker compose -f docker-compose-build.yaml build
```

## install gtp5g
```
cd ~
git clone https://github.com/free5gc/gtp5g.git

sudo apt -y update
sudo apt -y install gcc g++ cmake autoconf libtool pkg-config libmnl-dev libyaml-dev

cd ~/gtp5g
make
sudo make install
```

## Run free5GC
```
docker compose up -d
```
## stop free5GC
```
docker compose down
```

## setup UE info

請先打開VM或是電腦瀏覽器

輸入http://127.0.0.1:5000 或 http://<Free5GC_IP>:5000

* Default User: admin
* Default Password: free5gc

進入後點旁變 subscribers

就可以更改ISIM key等ue資訊

## 與 OAI整合
如果要跟oai連線請先設定好QoS，因為在 OAI 的預設核心網資料庫中，通常對一個用戶只會設定最基礎的「單一預設通道」（Default QoS Flow）

所以進入剛剛跟改UE info的地方，找到S-NSSAI Configuration的部分，先將Flow Rules 1 的部分刪掉

並且連線時要對齊所有的ISIM、key、amf ip address與docker ip address 不然會抱錯

### NTN_exercise
```
cd ~/openairinterface5g/cmake_targets
#gNB
sudo ./ran_build/build/nr-softmodem -O ../ci-scripts/conf_files/gnb.sa.band254.u0.25prb.rfsim.ntn-leo-free5gc.conf --rfsim
#UE
sudo ./ran_build/build/nr-uesoftmodem -O ../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue_free5gc.conf --band 254 -C 2488400000 --CO -873500000 -r 25 --numerology 0 --ssb 60 --rfsim --rfsimulator.prop_delay 20 --rfsimulator.options chanmod --time-sync-I 0.1 --ntn-initial-time-drift -46 --initial-fo 57340 --cont-fo-comp 2
```
