# Study Note: gNB scheduler

> Reference :
>
>  https://gitlab.eurecom.fr/oai/openairinterface5g/-/tree/develop/openair2/LAYER2/NR_MAC_gNB?ref_type=heads
> 
>  https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair2/LAYER2/NR_MAC_gNB/gNB_scheduler.c?ref_type=heads
> 
## TOC
1. flowchart

---

### 1 flowchart

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
