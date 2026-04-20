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
## 1 摘要

### what is schedule

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

## 2 flowchart

<img width="431" height="671" alt="gNB_scheduler c_flowchart" src="https://github.com/user-attachments/assets/b1518b4c-bfcb-42ed-af8e-60018e44833e" />

## 程式碼
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
### gNB_scheduler_dlsch.c

source : [openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_dlsch.c](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_dlsch.c?ref_type=heads)

#### [nr_schedule_ue_spec](https://github.com/Kuan-K/2025_kuan_project/blob/27bf1d81e16029bbaa4343c547c687424c12d80a/OAI/oai_codes/gNB_scheduler_dlsch.c#L1368)

* input
  * module_id_t module_id :  MAC id 通常為0
  * frame_t frame : 當前的frame
  * slot_t slot : 當前的slot 有了frame 跟 slot 才能知道現在的絕對時間
  * nfapi_nr_dl_tti_request_t *DL_req : 空白的DL控制單
  * nfapi_nr_tx_data_request_t *TX_req : 空白的DL資料單

這個函是會先看是否需要做下行排成，如果需要會將所需要的資料打包之後呼叫 nr_dlsch_preprocessor

#### [nr_dlsch_preprocessor](https://github.com/Kuan-K/2025_kuan_project/blob/27bf1d81e16029bbaa4343c547c687424c12d80a/OAI/oai_codes/gNB_scheduler_dlsch.c#L894)

* input
  * gNB_MAC_INST *mac : gNB_MAC的資訊
  * post_process_pdsch_t *pp_pdsch : 前面打包的資料
 
這個函式會檢查並確認頻寬、beam資源，並計算現在最多可服務 UE ，最後呼叫pf_dl

```
  int average_agg_level = 4; // TODO find a better estimation 假設一個 ue 需要 4 個 CEE來接收DCI
  int max_sched_ues = bw / (average_agg_level * NR_NB_REG_PER_CCE); // 總數 = BW(總REG數,106)/每支手機消耗的REG數
```
REG 在頻率上是一個PRB (PDCCH)能使用的最小單位 ； CEE = 6 個 REG(標準紙箱) 

#### [pf_dl](https://github.com/Kuan-K/2025_kuan_project/blob/27bf1d81e16029bbaa4343c547c687424c12d80a/OAI/oai_codes/gNB_scheduler_dlsch.c#L610)

* input
  * gNB_MAC_INST *mac : 基地台的設定與狀態
  * post_process_pdsch_t *pp_pdsch : 上一層的資料
  * NR_UE_info_t **UE_list : 目前連線到基地台的所有手機名單
  * int max_num_ue : 這個slot 最多能排程幾支手機
  * int num_beams : 系統目前使用的beam數量
  * int n_rb_sched[num_beams] : 紀錄還有多少 PRB 可以分配

這個函式會幫UE評估及打分，並且照分數將UE排序，最後確認是否有資源可以分配，決定好要分配給誰後，會計算UE的資料量打包後傳送接著處理下UE。以上動作皆在1個slot(<=1ms)內完成。

<img width="701" height="811" alt="pf_dl_flowchart" src="https://github.com/user-attachments/assets/3e1f62d1-976e-4e6d-9391-39ddb7a75f2f" />

##### 計算歷史吞吐量

```
    /* Calculate Throughput */
    const float a = 0.01f;
    const uint32_t b = stats->current_bytes; // 上次傳了多少Byte
    UE->dl_thr_ue = (1 - a) * UE->dl_thr_ue + a * b; // 平均速率等於(0.99 * 舊的平均速率) + (0.01 * 剛剛傳送的資料量)

    stats->current_bytes = 0;
    stats->current_rbs = 0;
```
##### 是否重傳
```
 if (harq_pid >= 0) { // 進入這裡代表：這支手機有資料傳失敗，急需重傳！
      NR_beam_alloc_t beam = beam_allocation_procedure(&mac->beam_info, frame, slot, UE->UE_beam_index, slots_per_frame);
      bool sch_ret = beam.idx >= 0;
      /* Allocate retransmission  重傳享有最高優先權，不需要算分數！直接呼叫 allocate_dl_retransmission */

else {// 進入這裡代表：沒有需要重傳的封包，準備評估要不要發送「新的資料」
      if (sched_ctrl->available_dl_harq.head < 0) { // 檢查harq 是否還有空位
        LOG_D(NR_MAC, "[UE %04x][%4d.%2d] UE has no free DL HARQ process, skipping\n",
              UE->rnti,
              frame,
              slot);
        continue;
      }
      update_dlsch_buffer(pp_pdsch->frame, pp_pdsch->slot, UE);
      if (!dlsch_to_schedule(sched_ctrl)) // 檢查RLC層的buffer有沒有資料要下載
        continue;
```

##### PF權重(coeff)計算
```
//決定 MSC 的邏輯

selected_mcs = get_mcs_from_bler(bo, stats, &sched_ctrl->dl_bler_stats, max_mcs, frame); //會根據通道品質(CQI)或錯誤率(BLER)選出一個等級，訊號越好，MSC越高
      int l = get_dl_nrOfLayers(sched_ctrl, current_BWP->dci_format); l (空間層數, Layers)
      const uint8_t Qm = nr_get_Qm_dl(selected_mcs, current_BWP->mcsTableIdx); // Qm (調變階數, Modulation Order)
      const uint16_t R = nr_get_code_rate_dl(selected_mcs, current_BWP->mcsTableIdx); //R (編碼率, Code Rate)

// 計算 TBS 網路有多好，一個CEE可以裝多少

uint32_t tbs = nr_compute_tbs(Qm, R,
                                    1, /* rbSize */
                                    10, /* hypothetical number of slots */
                                    0, /* N_PRB_DMRS * N_DMRS_SLOT */
                                    0 /* N_PRB_oh, 0 for initialBWP */,
                                    0 /* tb_scaling */,
                                    l) >> 3;

// 計算PF 權重分數
float coeff_ue = (float) tbs / UE->dl_thr_ue; // 分子 tbs (追求最大載量 Max C/I)，分母 dl_thr_ue (追求公平性 Fairness)
```

##### 安排控制與回饋通道
```
// 檢查有沒有 CEE
int CCEIndex = get_cce_index();
    if (CCEIndex < 0) {
      sched_ctrl->dl_cce_fail++; // 即使有 PRB 也沒用，排程失敗。
      iterator++; continue;
    }
// 安排手機回傳 ACK/NACK 的資源
 int alloc = -1;
    if (!get_FeedbackDisabled(iterator->UE->sc_info.downlinkHARQ_FeedbackDisabled_r17, sched_ctrl->available_dl_harq.head)) {
      int r_pucch = nr_get_pucch_resource(sched_ctrl->coreset, ul_bwp->pucch_Config, CCEIndex);
      alloc = nr_acknack_scheduling(mac, iterator->UE, frame, slot, iterator->UE->UE_beam_index, r_pucch, 0); // 在未來的某個上行 Slot，預留一個位置給手機傳 ACK
      if (alloc < 0) {
        LOG_D(NR_MAC, "[UE %04x][%4d.%2d] could not find PUCCH for DL DCI\n", rnti, frame, slot);
        reset_beam_status(&mac->beam_info, frame, slot, iterator->UE->UE_beam_index, slots_per_frame, beam.new_beam);
        iterator++;
        continue;
      }
    }
```

##### 計算資料量與更新

```

/*
前面get_rb_alloc 找到的 max_rbSize 是「目前最大剩餘空間」，但 UE 不一定需要這麼多 PRB。
nr_find_nb_rb 會根據 UE 的資料量 往回推算，算出剛剛好的 PRB 數量
*/
const int oh = 3 * 4 + (sched_ctrl->ta_apply ? 2 : 0);
    nr_find_nb_rb(sched_pdsch.Qm,
                  sched_pdsch.R,
                  1, // no transform precoding for DL
                  sched_pdsch.nrOfLayers,
                  tda_info.nrOfSymbols,
                  sched_pdsch.dmrs_parms.N_PRB_DMRS * sched_pdsch.dmrs_parms.N_DMRS_SLOT,
                  sched_ctrl->num_total_bytes + oh,
                  min_rbSize,
                  max_rbSize,
                  &sched_pdsch.tb_size,
                  &sched_pdsch.rbSize);

// 更新

n_rb_sched[beam.idx] -= sched_pdsch.rbSize; // 從系統扣掉剛發給UE的PRB數量
    for (int rb = bwp_start + sched_pdsch.rbStart; rb < bwp_start + sched_pdsch.rbStart + sched_pdsch.rbSize; rb++)
      rballoc_mask[rb] |= slbitmap; // 將資源上對應的格子標示為「已佔用」
    remainUEs[beam.idx]--;// 這個波束的派車單名額減 1
    iterator++;    // 換名單上的下一個 UE
```
