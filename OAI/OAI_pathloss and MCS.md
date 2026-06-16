# Study Note: OAI NTN LEO channel model and MCS

## Topic
  1. NTN channel model
  2. 3GPP TR 38.811 / TR 38.901 規格定義
  3. OAI channel model 功能對照

## NTN channel model




pathloss 會呼叫 compute_nr_SSB_PL

MAC排程時 會判斷差距有沒有大於PathlossChange_db 並發一個(功率報告)給gNB 提供給MCS 使用

而pathloss的計算公式是由referenceSignalPower(基地台使用多少能量發射) - max_ssb_rsrp_dBm(UE量測到的能量) 由此來計算path loss

referenceSignalPower 可以由gNB conf中的ssPBCH_BlockPower設定

max_ssb_rsrp_dBm 則是由UE直接呼叫 nr_ue_calculate_ssb_rsrp做計算
