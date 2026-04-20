# Study Note: gNB scheduler

> Reference :
>
>  https://gitlab.eurecom.fr/oai/openairinterface5g/-/tree/develop/openair2/LAYER2/NR_MAC_gNB?ref_type=heads
> 
>  https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair2/LAYER2/NR_MAC_gNB/gNB_scheduler.c?ref_type=heads
> 
## TOC
1. 摘要
2. flowchart
3. 程式碼

---
### 1 摘要

#### what is schedule

schedule 是指 gNB 的 MAC 層如何控制及分配資源，告訴 UE 什麼時候可以傳輸或接收訊息

以3GPP為例在time domain最小的單位通常是 slot 而在Frequency domain 則是以PRB為單位來進行分配

就像是一個棋盤每個格子代表可用的資源，gNB會去決定哪格要分給哪個UE

下行排程 : 就是gNB，判斷有多少資料量需分配給UE，以及有多少資源可以分配，並根據不同的演算法分配給UE
  
上行排程 : 是因為UE無法主動發送大量資料，必須先透過 PUCCH 發送 Scheduling Request(SR)，基地台收到後會分一小塊資源讓UE回傳BSR (Buffer Status Report,緩衝區狀態回報)。經基地台確認後發放uplink grant

* PRB(Physical Resource Block)
* 
  一個PRB 包含 12 個 subcarriers 是在 Frequency domain 的單位，實際占用頻寬會根據子載波間距(SCS)而改變(常見的有15kHz或30kHz)

  [note] 5G NR 不把所有的資料塞在一個很寬的頻率通道裡傳送，而是把一整段寬頻譜，切成非常多條「很細、很窄且互不干擾的頻率小徑」，這些小徑就叫做 Subcarrier（子載波）。
  
* PUCCH (Physical Uplink Control Channel)
  
  可以說是控制通道，裡面包含 HARQ 的 ack ， 手機目前的訊號品質CSI (Channel State Information) 及 SR(當手機有資料要上傳但又沒被分配到資源的時候)
  
* PUSCH (Physical Uplink Shared Channel)
  
  可以說是資料通道，裡面包含實際流量，Youtube影片等

* DCI(Downlink Control Information)
  
  是gNB對手機發號司令的文件，裡面包含資源分配，調變與編碼等
  * Downlink Grant : 叫手機準備收資料
  * Uplink Grant 允許手機準備傳資料，手機收到後才知道自己可以用那些PRB

### 演算法
*  最大載量 (Max C/I) : 只將資源分配給訊號最好的人，訊號差的人會永遠斷線。
*  絕對公平 (Round Robin) : 大家輪流發一人一個PRB，訊號好的會容易覺得資源被浪費，訊號差的會佔用太多資源，效率不高。
*  比例公平 (Proportional Fair, PF) 藉由各種因素來分配資源例如，當下能達到的速率、UE過去一段時間的平均速率，UE太久沒被排到，都會使權重改變，進而提升效率。

### 2 flowchart

<img width="431" height="671" alt="gNB_scheduler c_flowchart" src="https://github.com/user-attachments/assets/b1518b4c-bfcb-42ed-af8e-60018e44833e" />

### gNB_scheduler.c

source : [openair2/LAYER2/NR_MAC_gNB/gNB_scheduler.c](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair2/LAYER2/NR_MAC_gNB/gNB_scheduler.c?ref_type=heads)

#### clear_beam_information

```
  if (beam_info->beam_mode == NO_BEAM_MODE) // 如果基地台，就不需要管理波束，直接結束函式。
    return;
  AssertFatal(beam_info->beam_allocation_size >= 0, "Beam information not initialized\n"); //確保波束分配陣列的大小大於等於 0
  int idx_to_clear = (frame * slots_per_frame + slot) / beam_info->beam_duration; //計算「當前絕對週期」
  idx_to_clear = (idx_to_clear + beam_info->beam_allocation_size - 1) % beam_info->beam_allocation_size; 
  if (slot % beam_info->beam_duration == 0) { //只有當前的 slot 剛好是一個「新波束週期的開始」時，才執行清除。
    LOG_D(NR_MAC, "%d.%d Clear beam information for index %d\n", frame, slot, idx_to_clear);
    for (int i = 0; i < beam_info->beams_per_period; i++)
      beam_info->beam_allocation[i][idx_to_clear] = -1;
  }

```
清除舊的資料，騰出記憶體空間

#### clear_nr_nfapi_information

```
const int num_slots = gNB->frame_structure.numb_slots_frame; //取得一個 Frame 裡面總共有幾個 Slot
  UL_tti_req_ahead_initialization(gNB, num_slots, CC_idP, frameP, slotP); // 呼叫另一個初始化函式

  nfapi_nr_dl_tti_pdcch_pdu_rel15_t **pdcch = (nfapi_nr_dl_tti_pdcch_pdu_rel15_t **)gNB->pdcch_pdu_idx[CC_idP];

  gNB->pdu_index[CC_idP] = 0;// 將當前載波的 PDU 計數器歸零

  memset(pdcch, 0, sizeof(*pdcch) * MAX_NUM_CORESET); // 使用 memset 清空記憶體

  const int size = gNB->UL_tti_req_ahead_size; // 取得上行請求環狀緩衝區的大小
  const int prev_slot = frameP * num_slots + slotP + size - 1; //計算目標 Slot 索引值
  nfapi_nr_ul_tti_request_t *future_ul_tti_req = &gNB->UL_tti_req_ahead[CC_idP][prev_slot % size];
  future_ul_tti_req->SFN = (prev_slot / num_slots) % 1024; // 將 Slot 貼上正確的 SFN
  LOG_D(NR_MAC, "%d.%d UL_tti_req_ahead SFN.slot = %d.%d for index %d \n", frameP, slotP, future_ul_tti_req->SFN, future_ul_tti_req->Slot, prev_slot % size);
  /* future_ul_tti_req->Slot is fixed! */
  for (int i = 0; i < future_ul_tti_req->n_pdus; i++) { // 清空可能殘留的舊 PDU 資料
    future_ul_tti_req->pdus_list[i].pdu_type = 0;
    future_ul_tti_req->pdus_list[i].pdu_size = 0;
  }
  // 歸零計數器
  future_ul_tti_req->n_pdus = 0;
  future_ul_tti_req->n_ulsch = 0;
  future_ul_tti_req->n_ulcch = 0;
  future_ul_tti_req->n_group = 0;
```
