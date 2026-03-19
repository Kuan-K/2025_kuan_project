# installation : free5gc

> Reference :
> - [free5GC compose](https://github.com/calee0219/free5gc-docker-compose)
>
> - [gtp5g](https://github.com/free5gc/gtp5g)
>
> - [installation note](https://hackmd.io/@Yueh-Huan/S1eC0g3Gi#Free5GC-Installation-Guide)


請先安裝[docker](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/oaicn5g%20built%20environment_.md#install-docker-engine-and-the-docker-compose-plugin)

## pull docker image
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
## [DKMS](https://github.com/free5gc/gtp5g?tab=readme-ov-file#dkms-support) (option) 強烈建議

如果不做VM 每次重開機，都會把原本的東西更新掉導致不能跑

因為目前的docker compose裡面認得的是0.9.5以下的版本，所以以0.9.5示範

```

sudo cp -r ~/gtp5g /usr/src/gtp5g-0.9.5

# 如果需要降版本 請執行下面這邊(直接整段複製執行)
sudo tee /usr/src/gtp5g-0.9.5/dkms.conf <<EOF
PACKAGE_NAME="gtp5g"
PACKAGE_VERSION="0.9.5"
MAKE[0]="make CC=gcc-12"
CLEAN="make clean"
BUILT_MODULE_NAME[0]="gtp5g"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net"
AUTOINSTALL="yes"
EOF
# -------------------------

# 不需要降版本直接接著執行
sudo dkms add -m gtp5g -v 0.9.5
sudo dkms build -m gtp5g -v 0.9.5
sudo dkms install -m gtp5g -v 0.9.5

echo "gtp5g" | sudo tee -a /etc/modules # 讓模組開機自動啟用

# 驗證 如果顯示version 0.9.5 就代表成功
sudo modprobe gtp5g
modinfo gtp5g | grep version
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
