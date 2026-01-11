# RF-simulator

> Reference :
> - [RF simulator](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/radio/rfsimulator/README.md)
> - [Channel Modeling](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/DOC/channel_simulation.md)
> - [NTN channel](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/RUNMODEM.md?ref_type=heads#ntn-channel)

## General
  The RF simulator allows you to test OAI without a physical RF board. It replaces the real RF board driver and can simulate a simple channel.

As much as possible, it works like an RF board, but not in real-time: It can run faster than real-time if there is enough CPU, or slower (it is CPU-bound instead of real-time RF sampling-bound).

## Architecture

The left part runs only once, like an initialization, and it reads parameters, channel models, etc. The right part, on the other hand, runs in a loop and keeps reading data

<img width="617" height="587" alt="image" src="https://github.com/user-attachments/assets/68a57d27-9e97-478d-bfb5-f507d77282b3" />

Quoted from ([Architecture](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/radio/rfsimulator/README.md?plain=0#architecture))

## Useful options

| CL option                        | usage                                                                          | default                |
|:---------------------            |:-------------------------------------------------------------------------------|----:                   |
|`--rfsimulator.serveraddr <addr>` | IPv4v6 address or DNS name to connect to, or `server` to behave as a IPv4v6 TCP server | 127.0.0.1      |
|`--rfsimulator.serverport <port>` | port number to connect to or to listen on (eNB, which behaves as a tcp server) | 4043                   |
|`--rfsimulator.options`           | list of comma separated run-time options, two are supported: `chanmod`, `saviq`| all options disabled   |
|`--rfsimulator.options saviq`     | store IQs to a file for future replay                                          | disabled               |
|`--rfsimulator.options chanmod`   | enable the channel model                                                       | disabled               |
|`--rfsimulator.IQfile <file>`     | path to a file to store the IQ samples to (only with `saviq`)                  | `/tmp/rfsimulator.iqs` |
|`--rfsimulator.prop_delay`        | simulated receive-path (gNB: UL, UE: DL) propagation delay in ms               | 0                      |
|`--rfsimulator.wait_timeout`      | wait timeout when no UE is connected                                           | 1                      |

Quoted from ([overview](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/radio/rfsimulator/README.md?plain=0#overview))

## Channel Modeling
In the context of wireless communications, a channel model refers to a mathematical model used to simulate how the transmission medium affects signal propagation. These models take into account factors such as attenuation, interference, and fading, all of which influence the quality of communication between the transmitter and the receiver.


## channel parameter
```
channel_desc_t *new_channel_desc_scm(uint8_t nb_tx, #  發射天線數量
                                     uint8_t nb_rx, #  接收天線數量
                                     SCM_t channel_model, #  選用通道模型
                                     double sampling_rate, #  取樣率
                                     uint64_t center_freq, #  中心頻率
                                     double channel_bandwidth, #  通道頻寬
                                     double DS_TDL, #  
                                     double maxDoppler, #  最大多普勒位移
                                     const corr_level_t corr_level, #
                                     double forgetting_factor, #
                                     int32_t channel_offset, #
                                     double path_loss_dB, #  路徑損耗
                                     float noise_power_dB); #  雜訊功率
```
### Channel Model configuration file

In the OAI / RFsimulator system, the channel parameters are not hard-coded in the source code; instead, they are placed in configuration files (.conf).

For the gNB main configuration file (for example, gnb.sa.band78.106prb.rfsim.conf), you only need to add the following line at the end:
```
@include "channelmod_rfsimu.conf"
```
and that channel configuration file will be loaded as well.

The same idea applies to the UE: at the end of its own configuration file, it includes the same file or another channel configuration file.
- *note* The included channelmod_rfsimu.conf file must be placed in the same directory as the gNB/UE configuration file; otherwise, the include statement will not be able to find it.

## Model lists

In OAI’s channel simulation configuration file, you can define multiple model lists.
When the system starts, it loads one list according to the value specified by the modellist parameter.
In the configuration file, each entry in a model list uses a set of parameters to describe a single channel model.

|Parameter name   |Type         |Default    |Description |
|:---             |:---:        |---:       |:----       |
| `model_name`    |char string  | mandatory |name of the model, as used in the code to retrieve a model definition.|
| `type`          |char string  | `AWGN`    |name of the channel modelization algorithm applied on RF signal. The list of available models is defined in [`sim.h`](../sim.h]|
| `ploss_dB`      |real (float) |          0|total path loss of the channel including shadow fading, in dB |
| `noise_power_dB`|real (double)|        -50|Noise power in dB, used to compute the SNR. Its value is proportional to the noise added.|
| `forgetfact`    |real (double)|          0|Forgetting factor, allows for simple 1st order temporal variation. 0 means a new channel every call, 1 means keep channel constant all the time|
| `offset`        |integer      |          0|channel offset for accessing the input signal, in samples|
| `ds_tdl`        |real double  |          0|delay spread for TDL models|

Quoted from ([model lists](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/DOC/channel_simulation.md?plain=0#model-lists))

## 預計要看的檔案

* [openair1/SIMULATION/TOOLS/multipath_channel.c](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/multipath_channel.c)	最核心的數學檔案。實現了多路徑卷積、多徑效應（Multipath）的計算。
* [openair1/SIMULATION/TOOLS/random_channel.c](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/random_channel.c)	負責通道模型的初始化與生成（例如生成隨機的衰落係數）。
* [openair1/SIMULATION/TOOLS/sim.h](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/sim.h)	定義了最重要的數據結構 channel_desc_t，包含了通道的所有參數（延遲、增益、天線數等）。
* [openair1/SIMULATION/TOOLS/DOC/channel_simulation.md](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair1/SIMULATION/TOOLS/DOC/channel_simulation.md)	官方的技術說明文件，詳細描述了配置參數與模型原理。


## RFsimulator重要函式與模擬邏輯
### 摘要
  在 OAI 中扮演的是「虛擬射頻卡（Virtual RF Device）」的角色，原本 OAI 訊號應該送往 USRP 等硬體設備，但 rfsimulator 攔截了這些 IQ Samples（同相正交訊號），透過網路（TCP Sockets）在基站（gNB）與終端（UE）之間傳遞，並在過程中「加料」來模擬通道效應。
### service Link & Feeder Link
在標準的 rfsimulator 中，它通常不區分這兩段。它將「基站 $\rightarrow$ 衛星 $\rightarrow$ 終端」視為一個整體的 End-to-End Channel。但在NTN中會分開

service Link:主要是模擬多普勒頻移（Doppler）和多路徑衰落（Fading）

feeder Link:主要是模擬巨大的傳播延遲 (Propagation Delay)

### rfsimulator.cpp
  #### device_init
  讀取參數、時間/延遲設定、函數指針掛載、對外接口設定

  ##### 初始化(讀取參數)
    ```
    rfsimulator->tx_num_channels = openair0_cfg->tx_num_channels;
    rfsimulator->rx_num_channels = openair0_cfg->rx_num_channels;
    rfsimulator->sample_rate = openair0_cfg->sample_rate;
    rfsimulator_readconfig(rfsimulator);
    ```
    抓取基本硬體參數如(天線數、採樣率)
    rfsimulator_readconfig(rfsimulator); # 會去抓取設定檔中關於rfsimulator的參數，例如判斷他是server or client 、 使用的通道模型等
  ##### 傳播延遲(時間/延遲設定)
    ```
    if (rfsimulator->prop_delay_ms > 0.0)
      rfsimulator->chan_offset = ceil(rfsimulator->sample_rate * rfsimulator->prop_delay_ms / 1000);
    if (rfsimulator->chan_offset != 0) {
      rfsimulator->prop_delay_ms = rfsimulator->chan_offset * 1000 / rfsimulator->sample_rate;
      LOG_I(HW, "propagation delay %f ms, %lu samples\n", rfsimulator->prop_delay_ms, rfsimulator->chan_offset);}
    ```
    程式將你設定的毫秒級延遲（prop_delay_ms）轉換成採樣點數量（samples）。
    計算方式：rfsimulator->sample_rate * rfsimulator->prop_delay_ms / 1000
    在 NTN 中，如果設定 10ms 的延遲，chan_offset 就會告訴模擬器在發送訊號時要「往後推」多少採樣點。這就是模擬 Feeder Link 長距離傳輸的初步實作。

  ##### Server vs Client(對外接口設定)
  ```
    device->trx_start_func = rfsimulator->role == SIMU_ROLE_SERVER ? startServer : startClient;
    device->trx_get_stats_func = rfsimulator_get_stats;
    device->trx_reset_stats_func = rfsimulator_reset_stats;
    device->trx_end_func = rfsimulator->role == SIMU_ROLE_SERVER ? stopServer : rfsimulator_end;
    device->trx_stop_func = rfsimulator_stop;
    device->trx_set_freq_func = rfsimulator_set_freq;
    device->trx_set_gains_func = rfsimulator_set_gains;
  ```
OAI 的 rfsimulator 使用 TCP 連線。通常 gNB（基站）是 Server，UE（終端）是 Client。這裡就是在確定腳色設定無誤。
  ##### 攔截訊號 (函數指針掛載)
  ```
    device->trx_write_func = rfsimulator_write;
    device->trx_read_func = rfsimulator_read;
  ```
    當 OAI 想要「送出訊號」到天線時，它其實是呼叫了 rfsimulator_write（把資料寫入 Socket 傳給對方）。

    當 OAI 想要「接收訊號」時，它呼叫 rfsimulator_read（從 Socket 讀取對方的資料並套用通道模型）。
    rfsimulator_read的關鍵有一個rfsimulator_read_beam的func他主要為了模擬天線的陣列，可以先理解為把資料讀進來的過程

### apply_channelmod.c
    


