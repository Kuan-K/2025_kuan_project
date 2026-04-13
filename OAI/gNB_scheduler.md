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
  idx_to_clear = (idx_to_clear + beam_info->beam_allocation_size - 1) % beam_info->beam_allocation_size; //只有當前的 slot 剛好是一個「新波束週期的開始」時，才執行清除。
```
清除舊的資料，騰出記憶體空間

#### clear_nr_nfapi_information
