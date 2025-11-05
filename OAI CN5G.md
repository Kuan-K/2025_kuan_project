# OAI CN5G

> Reference :
> - [NR_SA_Tutorial_OAI_CN5G](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/NR_SA_Tutorial_OAI_CN5G.md?ref_type=heads)

### 安裝開發與網路工具（git、net-tools、PuTTY）
```
sudo apt update
sudo apt install -y git net-tools putty
```

### 安裝 Docker Engine 與 Docker Compose 外掛
```
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
### 把目前使用者加入 docker 群組（之後即可不需 sudo 執行 docker），然後重開機。
```
sudo usermod -a -G docker $(whoami)
reboot
```

### 下載 OAI 提供的教學資源壓縮包，解壓後把 oai-cn5g 目錄移到家目錄，然後刪除中間產物與壓縮檔。
```
wget -O ~/oai-cn5g.zip https://gitlab.eurecom.fr/oai/openairinterface5g/-/archive/develop/openairinterface5g-develop.zip?path=doc/tutorial_resources/oai-cn5g
unzip ~/oai-cn5g.zip
mv ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g/doc/tutorial_resources/oai-cn5g ~/oai-cn5g
rm -r ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g ~/oai-cn5g.zip
```

### 下載 OAI CN5G 的 Docker 映像
```
cd ~/oai-cn5g
docker compose pull
```
**Output**
```

[+] Pulling 83/83
 ✔ oai-amf Pulled
 ✔ oai-udr Pulled
 ✔ mysql Pulled
 ✔ oai-ausf Pulled
 ✔ oai-udm Pulled
 ✔ oai-upf Pulled
 ✔ oai-nrf Pulled
 ✔ oai-smf Pulled
 ✔ oai-ext-dn Pulled
 ✔ ims Pulled
```

### Start OAI CN5G(之後只要執行這個就可開啟CoreNetwork)
```
cd ~/oai-cn5g
docker compose up -d
```
**Output**
```

+] Running 11/11
 ✔ Network oai-cn5g-public-net  Created                                    0.1s 
 ✔ Container oai-nrf            Started                                    0.9s 
 ✔ Container ims                Started                                    0.9s 
 ✔ Container oai-ext-dn         Started                                    0.9s 
 ✔ Container mysql              Started                                    0.9s 
 ✔ Container oai-udr            Started                                    1.0s 
 ✔ Container oai-udm            Started                                    1.2s 
 ✔ Container oai-ausf           Started                                    1.4s 
 ✔ Container oai-amf            Started                                    1.6s 
 ✔ Container oai-smf            Started                                    1.7s 
 ✔ Container oai-upf            Started                                    2.0s 
```
### 查看容器是否健康
```
watch -n 1 docker compose -f docker-compose.yml ps -a
```
**Output**
<img width="1840" height="233" alt="image" src="https://github.com/user-attachments/assets/bb20ea4b-8cdd-4556-9851-b08f08680e7c" />

### Stop OAI CN5G
```
cd ~/oai-cn5g
docker compose down
```
**Output**
```
[+] Running 11/11
 ✔ Container oai-ext-dn         Removed                                    0.2s 
 ✔ Container oai-upf            Removed                                    0.4s 
 ✔ Container ims                Removed                                    0.2s 
 ✔ Container oai-smf            Removed                                    0.4s 
 ✔ Container oai-amf            Removed                                    0.9s 
 ✔ Container oai-ausf           Removed                                    0.3s 
 ✔ Container oai-udm            Removed                                    0.3s 
 ✔ Container oai-udr            Removed                                    0.3s 
 ✔ Container oai-nrf            Removed                                    0.3s 
 ✔ Container mysql              Removed                                    0.8s 
 ✔ Network oai-cn5g-public-net  Removed                                    0.2s 
```
