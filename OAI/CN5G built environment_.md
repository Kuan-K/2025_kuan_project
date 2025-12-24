# OAI CN5G

> Reference :
> - [NR_SA_Tutorial_OAI_CN5G](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/NR_SA_Tutorial_OAI_CN5G.md?ref_type=heads)


## OAI CN5G snapshot

This folder is a snapshot of `doc/tutorial_resources/oai-cn5g` from the OAI openairinterface5g project
as of 2024-05-22.

- upstream repo: openairinterface5g
- branch: `2025.w46`
- file: `doc/tutorial_resources/oai-cn5g/docker-compose.yaml`
- commit: `92980ceb72`
- license: OAI Public License v1.1（詳見原專案）

This version has been tested on Ubuntu 22.04 + Docker and can be started successfully。


### Install development and networking tools（git、net-tools、PuTTY）
```
sudo apt update
sudo apt install -y git net-tools putty
```

### Install Docker Engine and the Docker Compose plugin
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
### Add the current user to the docker group (so you can run Docker without sudo afterward), then reboot
```
sudo usermod -a -G docker $(whoami)
reboot
```

### Download the tutorial resource archive provided by OAI, extract it, move the oai-cn5g directory to your home directory, and then delete the intermediate files and the archive.
```
wget -O ~/oai-cn5g.zip https://gitlab.eurecom.fr/oai/openairinterface5g/-/archive/develop/openairinterface5g-develop.zip?path=doc/tutorial_resources/oai-cn5g
unzip ~/oai-cn5g.zip
mv ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g/doc/tutorial_resources/oai-cn5g ~/oai-cn5g
rm -r ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g ~/oai-cn5g.zip
```

### Pull OAI CN5G docker images
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

### Start OAI CN5G(After that, you just need to run this to start the Core Network.)
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
### Check whether the containers are healthy
```
watch -n 1 docker compose -f docker-compose.yml ps -a
```
**Output**
<img width="1840" height="233" alt="image" src="https://github.com/user-attachments/assets/bb20ea4b-8cdd-4556-9851-b08f08680e7c" />

### Stop OAI CN5G(Make sure to shut it down when you’re done, otherwise the containers will be left running.)
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
### Troubleshooting

#### Error message: Overlapping IP addresses
```
 ✘ Network oai-cn5g-public-net  Error                                      0.0s 
failed to create network oai-cn5g-public-net: Error response from daemon: invalid pool request: Pool overlaps with other one on this address space
```

#### Solution
```
docker network inspect bridge #you will see something like："Subnet": "192.168.70.0/24"
```
Open the docker-compose.yml file in the project and find this section:
```
networks:
  oai-cn5g-public-net:
    ipam:
      config:
        - subnet: 192.168.70.128/26
```
Check whether they are the same. If not, run the following commands.
```
docker network inspect $(docker network ls -q) | grep -E '"Name"|"Subnet"'# 看每一個 network 的 Subnet
```
If you find this in the output：
```
"Name": "xxxxxx",
    "Subnet": "192.168.70.0/24",
```
remove：
```
docker network rm xxxxxx
```
**Don't remove bridge / host / none

#### Error message: Duplicate containers
```
Error response from daemon: Conflict. The container name "/mysql" is already in use by container "e9b912e99f6060da3969c1c169deb8c9b3ed724657a12595b031d57aa067915e". You have to remove (or rename) that container to be able to reuse that name.
```
This means the `mysql`container is duplicated — the one from last time was not removed.

```
docker rm -f mysql
```
Use `docker rm -f xxxxxx` to delete the specified container. After deleting it, just run the setup again.
