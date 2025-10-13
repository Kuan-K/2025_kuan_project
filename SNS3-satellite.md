# Study Note: SNS3-Satellite

## TOC
1.Forward Link
2.ACM
3.Scheduler
4.Fading
5.GW / UT（Gateway / User Terminal）
6.BBFrame（Baseband Frame）
7.CBR vs OnOff
---

## 1. Forward Link
  節點:GW user(來源端)、GEO衛星(SAT)、UT users(接收端)
  鏈路方向:只測前向 (GW->SAT->UT) 回向(rtn)不在支援範圍內
## 2. ACM
  根據信道品質自行切換ModCod，讓傳輸效率與可靠性取得平衡
## 3. Scheduler
  在 MAC 層決定哪個使用者在什麼時候用多少資源、用哪種幀長度送
  目的是為了提高頻譜效率與公平性（使用者都能輪到）
## 4. Fading
  無線通道隨時間/空間波動（多路徑、陰影、天氣、遮蔽物），造成信號好壞起伏。
## 5. GW / UT（Gateway / User Terminal）
  GW：地面端「總控/上游」，連外部核心網或伺服器
  UT：使用者端的衛星終端裝置
## 6. BBFrame（Baseband Frame）
  可把它視為 MAC/PHY 的「載具幀」，把多個上層封包（UDP/IP 等）塞進來一起送
  如果同一時間有多個小幀、或幀未滿，合併可以降低開銷、提升頻譜效率（像把零碎貨櫃併成滿櫃）。
## 7. CBR vs OnOff
  CBR 模式:
          在程式中 單一流的供給速率 ≈ 128 B / 50 μs = 2.56 MB/s ≈ 20.48 Mbps。
          總供給速率 ≈ (#UT) × 20.48 Mbps 程式中總UT數預設為10
  OnOff 模式:
          平均資料率 DataRate(16000)（bit/s）看起來很小（16 kbps），
          但因為是突發型，短時間內可能造成隊列尖峰，導致 merge 次數上升、幀佔用率抖動、排程更忙
  
  
