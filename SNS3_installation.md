# SNS3_Installation

> Reference :
>   https://github.com/liang924/SNS3/blob/dfde8e9b69fbb50e9f6159a1a4ac4c7c1d0bb9b0/SNS3%20Installation.md
>   https://github.com/sns3/sns3-satellite?tab=readme-ov-file#bake


###Install dependency
```
sudo apt update
sudo apt install -y git automake cmake qtbase5-dev python3-dev python3
```
apt update：更新套件清單。
git：之後要用來把原始碼倉庫複製下來。
automake、cmake：常見的建置工具。
qtbase5-dev：Qt5 的開發檔（之後像 NetAnim 這類基於 Qt 的視覺化工具會需要）。
python3、python3-dev：Bake 及 ns-3 的 Python 綁定/腳本需要 Python，python3-dev 提供 Python 的標頭檔給編譯器用。

### Installation by bake
```
cd ~
mkdir workspace
cd workspace
git clone https://gitlab.com/nsnam/bake.git
```
在home下建立一個工作區，並將bake抓下來
workspace:將所有資源存放在這方便管理/清理

### Set environment parameters:
```
export BAKE_HOME=`pwd`
export PATH=$PATH:$BAKE_HOME/build/bin
export PYTHONPATH=$BAKE_HOME/build/lib
export LD_LIBRARY_PATH=$BAKE_HOME/build/lib
```
```
cd bake
./bake.py configure -e ns-allinone-3.43
./bake.py check
```
BAKE_HOME：指定 Bake 的安裝/建置根目錄。pwd 會把「目前目錄」的絕對路徑填進去。
PATH+=.../build/bin：讓 shell 找得到由 Bake 建出的可執行檔（之後會出現在 build/bin）。
PYTHONPATH=.../build/lib：讓 Python 能 import Bake/NS-3 建出的 Python 模組與綁定（.so / .py）。
LD_LIBRARY_PATH=.../build/lib：讓 動態連結器 找到建出的共享函式庫（.so），可避免執行時「找不到庫」。

### Deploy ns3 by bake
```
./bake.py download
```
*note cppyy 可能會因為沒有安裝python套件而出現problem
可執行以下程式來解決
 1) 先裝 pip3
sudo apt update
sudo apt install -y python3-pip
 2) 用 pip 裝 cppyy（建議用 python -m 的寫法）
python3 -m pip install --user cppyy
 3) 驗證
python3 -c "import cppyy; print(cppyy.__version__)"

### Configure ns3
```
cd source/ns-3.43
./ns3 clean
./ns3 configure --build-profile=debug --enable-examples --enable-tests
```

./ns3 configure --build-profile=debug --enable-examples --enable-tests
呼叫 ns3 腳本（ns-3 的官方建置前端）去執行 CMake 的「設定」階段：
    --build-profile=debug：把編譯模式設成除錯（含符號、關閉最佳化），方便追蹤與測試。
    --enable-examples：把 examples/ 目錄下的示例程式也納入建置。
    --enable-tests：把單元測試/整合測試也納入建置，之後可 ./ns3 test 執行。

### Get satellite/ traffic/magister-stats modules
```
cd contrib
git clone https://github.com/sns3/sns3-satellite.git satellite
git clone https://github.com/sns3/traffic.git traffic
git clone https://github.com/sns3/stats.git magister-stats

cd ~/workspace/bake/source/ns-3.43/contrib/satellite
git checkout 3.43
cd ~/workspace/bake/source/ns-3.43/contrib/traffic
git checkout 3.43
cd ~/workspace/bake/source/ns-3.43/contrib/magister-stats
git checkout 3.43
```
contrib/ 是 ns-3 的外掛模組目錄：放在這裡的專案，ns-3 會在設定/建置時自動發現並一併編譯、連結。
*note 須將外掛模組隊齊版本壁面API不相容

### Configure CMake and ask it to build NS-3 
```
cd ~/workspace/bake/source/ns-3.43
./ns3 clean
./ns3 configure --build-profile=optimized --enable-examples --enable-tests
./ns3 build
```
./ns3 configure --build-profile=optimized --enable-examples --enable-tests：以最佳化模式設定建置，並且把範例與測試都納入。
./ns3 build：開始編譯。CMake 會自動把 contrib/ 裡找到的所有模組一起編譯

### Post-Compilation
```
cd contrib/satellite
git submodule update --init --recursive
```
<img width="626" height="333" alt="image" src="https://github.com/user-attachments/assets/040ec396-b4ab-444e-8993-fa4003428b4e" />

### Testing SNS-3
```
cd ~/workspace/bake/source/ns-3.43
./test.py --no-build
```
--no-build：不重新編譯（假設你剛剛已經 ./ns3 build 完成），直接跑所有啟用的單元/整合測試
