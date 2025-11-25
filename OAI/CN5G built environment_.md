# OAI CN5G

> Reference :
> - [NR_SA_Tutorial_OAI_CN5G](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/NR_SA_Tutorial_OAI_CN5G.md?ref_type=heads)


## OAI CN5G snapshot

本資料夾為 OAI openairinterface5g 專案中  
`doc/tutorial_resources/oai-cn5g` 於 2024-05-22 的快照。

- upstream repo: openairinterface5g
- branch: `develop`
- file: `doc/tutorial_resources/oai-cn5g/docker-compose.yaml`
- commit: `246a8aff`
- license: OAI Public License v1.1（詳見原專案）

此版本已在 Ubuntu 22.04 + Docker 上測試可正常啟動。


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

### Stop OAI CN5G(結束一定要關不然會留下容器)
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
### 錯誤排查

#### 錯誤資訊:IP重疊
```
 ✘ Network oai-cn5g-public-net  Error                                      0.0s 
failed to create network oai-cn5g-public-net: Error response from daemon: invalid pool request: Pool overlaps with other one on this address space
```

解決方法
```
docker network inspect bridge #會看到類似："Subnet": "192.168.70.0/24"
```
打開專案中的docker-compose.yml找到：
```
networks:
  oai-cn5g-public-net:
    ipam:
      config:
        - subnet: 192.168.70.128/26
```
查看是不是一樣，如果不一樣
```
docker network inspect $(docker network ls -q) | grep -E '"Name"|"Subnet"'# 看每一個 network 的 Subnet
```
如果輸出裡有像：
```
"Name": "xxxxxx",
    "Subnet": "192.168.70.0/24",
```
可以用：
```
docker network rm xxxxxx
```
**不要刪到bridge / host / none

#### 錯誤資訊:容器重疊
```
Error response from daemon: Conflict. The container name "/mysql" is already in use by container "e9b912e99f6060da3969c1c169deb8c9b3ed724657a12595b031d57aa067915e". You have to remove (or rename) that container to be able to reuse that name.
```
代表mysql這個容器重疊了上次沒有刪

```
docker rm -f mysql
```
用docker rm -f xxxxxx刪除指定容器，如果刪完後再重新跑就好
