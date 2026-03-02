# Study Note: NTN backgroumd knowledge

> Reference :
>   https://hackmd.io/D7pXmmKXQf-7enZbBZy8cw
> 
>   3GPP TR 38.821
> 
>   3GPP TS 38.211
>
>   3GPP TS 38.331 

## TOC
1. [摘要](#一摘要)
2. [5G NR協定堆疊(Protocol Stack)與RACH](#二5G-NR協定堆疊Protocol-Stack與RACH)
3. [NTN 的主要問題](#三NTN的主要問題)
4. [延遲補償（Delay Compensation）](#四延遲補償Delay-Compensation)
5. [LEO 衛星特性與基本參數](#五LEO-衛星特性與基本參數)
6. [System information blocks Type 19 (SIB 19)](#六System-information-blocks-Type-19-SIB-19)
7. [UE 的 NTN 接取流程](#七UE-的-NTN-接取流程) 

---

## 一.摘要
  NTN技術就是整合衛星與5G架構，藉由衛星來連接，擴大服務範圍，讓沒有辦法架設硬體的偏遠地區也能受到服務。
  ![NTN_Fig1](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/3GPP%20NTN%20Architecture%20Overview.png)
* User Equipments (UE) : 使用者設備，例如手機
* Satellite : 衛星
* Gateway : 地面閘道站
* Service link：UE 與衛星之間的連線
* Feeder link：衛星與Gateway之間的連線
* Beam footprint：衛星波束覆蓋的區域
### NTN有兩種模Transparent Mode 與 Regenerative Mode，兩種架構圖如下:
  
   Ttransparent Mode：衛星只做轉傳信號，不做處理信號，只是作為一個點接收訊號後直接傳送不會動到訊號。 方塊圖 [trans](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%96%B9%E5%A1%8A%E6%A8%A1%E6%93%AC%E5%9C%96leo_tran_F.png)
   
   Regenerative Mode：衛星可做解碼處理信號，衛星像是一個太空中的基地台，而不只是轉傳訊號。 方塊圖 [regen](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%96%B9%E5%A1%8A%E6%A8%A1%E6%93%AC%E5%9C%96leo_regen_F.png)
   
  ![NTN_Fig2](https://github.com/user-attachments/assets/3c7a4f8f-ef87-4388-ba6c-236efd8d0433)
  
## 二.5G NR協定堆疊(Protocol Stack)與RACH

  在3GPP NTN 中，無線介面沿用 5G NR Protocol Stack。
  
  ![Uplane](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/NR%20Protocol%20Stack.png)    ![Cplane](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/NR%20Protocol%20Stack%20(C%20plane).png)

### 用戶平面 (User Plane, U-plane) 與 控制平面 (Control Plane, C-plane)

* 用戶平面 (User Plane)外部： 負責處理用戶實際產生的數據，目標是讓數據能高效、安全地在 UE（手機）與外部網路之間傳輸。
    最終連接到 UPF (User Plane Function)
* 控制平面 (Control Plane)內部： 負責處理信令（Signaling），目標是管理連線的建立與維護。
    最終連接到 AMF (Access and Mobility Management Function)
  
  [note] [核心網](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/5GCN.md#study-note-5gcn)
#### 各層介紹
* SDAP (Service Data Adaptation Protocol,服務數據適應協定)
  * 任務： 這是 5G 中的最頂層協定，其唯一的任務是將服務品質 (QoS) 流映射到特定的「無線承載 (Radio Bearer)」。
  * 比喻： 就像公司的郵件分類員，看到標註為「緊急/執行長」的信件（如語音通話）會放入「快遞」郵袋，而標註為「通訊報」的信件（如背景更新）則放入「大宗郵件」袋中。
  
    [note] 無線承載:用戶設備 (UE) 與 基地台 (gNB) 之間建立的「虛擬傳輸通道」，專門用來承載具有特定服務品質（QoS）要求的數據。
    可以想像成專屬的物流傳送帶，每條傳送帶都根據貨物的需求，例如:不能損壞、必須極速送達，設定了不同的運送規則。
    
* PDCP (Packet Data Convergence Protocol,封包數據匯聚協定)
  * 任務：此層接收來自 SDAP 的數據並執行兩大任務：1. 壓縮 IP 標頭以節省空間；2. 對數據進行加密以確保安全。
  * 比喻：這是安全與包裝部門。它會對郵件進行「真空密封」使其體積變小（壓縮），並放入「防篡改的鎖定袋」中（加密）。
    
* RLC (Radio Link Control,無線鏈路控制)
  * 任務：確保可靠性並處理大型封包。將大型封包分段，並在需要時使用 ARQ (自動重傳請求) 重新傳輸遺失的碎片。
  * 比喻：這是運輸部門。它接收大型物品（如自行車）並將其「拆解」以裝入數個小箱子，並標註「1號箱(輪子)，共 2 箱」、「2號箱(車架)，共 1 箱」等，以便在接收端重新組裝。
  * 模式： 包含透明模式 (TM)、不確認模式 (UM) 和確認模式 (AM)，其中 AM 提供可靠的數據傳輸。
     1. 透明模式 (Transparent Mode, TM)
         這是最簡單的模式，RLC 層幾乎「不做任何處理」。
      2. 不確認模式 (Unacknowledged Mode, UM)
         這種模式負責處理數據的分段，但「不負責檢查對方是否收到」。
      3. 確認模式 (Acknowledged Mode, AM)
         這是最複雜且最可靠的模式，除了分段功能外，它使用 [ARQ](https://github.com/Kuan-K/2025_kuan_project/edit/main/NTN.md#harqarq)（自動重傳請求） 機制。如果發送端沒收到接收端的確認（ACK），或者收到錯誤通知（NACK），就會重新發送遺失的數據碎片。
         
* MAC (Medium Access Control,媒體存取控制)
  * 任務：負責調度哪位用戶在何時可以傳輸，來自 RLC 層的小碎片多工處理 (Multiplex) 成一個大的傳輸區塊 (Transport Block)；調度 (Scheduling)、邏輯通道優先級排序、透過 HARQ (混合自動重傳請求) 進行錯誤校正，以及通道映射。
  * 比喻：裝卸碼頭經理。它查看所有小箱子，並決定哪些箱子適合裝入現在要出發的卡車。
* PHY (Physical Layer,實體層)
  * 任務：這是實體硬體，將來自 MAC 層的位元轉換為無線電訊號。
  * 比喻：卡車與司機，負責貨物的實際物理運輸。
  * 功能： 編碼、調變，以及頻率/時間同步。
    
* RRC (Radio Resource Control,無線資源控制)
  * 功能：(UE $\leftrightarrow$ gNB) 連線建立/釋放、系統資訊廣播 (SIB)、無線承載配置、測量報告
  * 比喻：飯店櫃檯與服務生。分配床位、換房間 (Handover)、拿地圖 (SIB)、連線狀態
    
* NAS (Non-Access Stratum,非接入層)
  * 功能：(UE $\leftrightarrow$ CN) 負責 UE 與核心網 (AMF/SMF) 之間的移動性管理、對談管理與安全控制。

  ### RACH
  
  Msg1:PRACH (UE 發 preamble)
  Msg2:Random Access Response ,RAR (gNB 回 RAR)
  Msg3: RRC Setup Request(UE 發送自己的身分識別與建立連線的請求。)
  Msg4: RRC Setup / Contention Resolution(gNB 確認連線，此後 UE 正式進入 RRC_CONNECTED 狀態)

  比喻
  * 走進飲料店說:「我要點餐」 店員沒空所以先給你號碼牌 (Msg1)
    *  你不知道店員什麼時候有空，店員也先只知道有個客人拿了號碼牌
  * 店員喊 :　「輪到幾號點餐了」(Msg2)
  * 走到櫃台，跟店員說：「我叫阿寬，我要一杯拿鐵」(Msg3)
  * 店員說：「好，阿寬，這是你的客戶編號 123，麻煩到旁邊等叫號。」(Msg4)
  

## 三.NTN的主要問題

### PHY
  1. 定時提前 (Timing Adavance, TA)：
      在地面5G中，gNB會計算延遲，告訴UE何時開始發送訊號，不過在NTN中延遲太大(LEO中延遲是毫秒等級的)，無法即時回饋。
     
      解決方法:
       因此UE會在第一次上行傳輸前先做預先補償時間延遲，利用自身的GNSS位置計算出與衛星的距離，調整上行傳輸時間。
       
  2. 多普勒提前補償(Doppler Pre-Compensation)：
     由於低軌衛星的移動速度非常快(LEO時速大約7.8km/s)，會造極大的多普勒效應，UE需預先調整自己的頻率來抵銷衛星移動造成的多普勒效應。
 ### MAC
  1. HARQ 停用：
     
     標準的MAC層HARQ在衛星的常往返延遲下無法使用，因為會導致整條鏈路停滯。

     3GPP的解法是：讓HARQ 回饋（feedback）變成可設定項(LEO)，或是在大多情況下直接關閉(GEO,MEO,HEO)。
     
     #### HARQ/ARQ
          
         HARQ(Hybird Automatic Repeat Request)：
         當接受訊號有錯，如果錯誤是微小的則自動修復，如錯誤過大則請求重傳，並將新資料與舊資料合併再解碼     
         ARQ：     
         經過Hard處理後訊號大多已完整，或是訊號剩下可接受的範圍，而ARQ負責處理HARQ的殘餘錯誤，發現錯誤後直接丟棄不做合併。
         *HARQ在PHY運作，由MAC控制
          ARQ在RLC層運作

  2. 可靠性：
     
     當 HARQ 被關閉後，可靠性機制會上移到更高一層 —— RLC 層的「確認模式（Acknowledged Mode, RLC-AM）」。

     RLC-AM 雖然速度較慢，但能在長延遲環境下運作，確保資料在遺失時仍能被重新傳送。

  ## 四.延遲補償（Delay Compensation）
  
  在地面 5G 中，基地台（gNB）會告訴手機（UE）應該如何調整它的時間（Timing）。
  但在 NTN 中，延遲太大了，無法像地面 5G 一樣讓 gNB 即時回饋。

  因此 UE 必須在傳送之前，自行計算延遲與頻率補償（Doppler），並在發射前先修正。

  頻道結構（邏輯、傳輸、實體層）與地面 5G 相同，
  但在這些頻道上運作的程序（尤其是錯誤修正與排程）
  都必須大改，才能處理巨大的衛星延遲。

  ### 問題

  1. 極大的時間延遲（Massive Timing Delay）：

     若 UE 剛剛傳送訊號，它的訊號會在錯誤的時間到達衛星，
     可能和其他使用者的訊號「碰撞」。
     
     在地面 5G：

      gNB 測量延遲
      gNB 發 Timing Advance（TA） 給 UE
      UE 依照 TA 調整上行傳輸時間
      但在 NTN：
      等 gNB 的 TA 指令回到 UE 時，衛星可能已經移動

      這代表 gNB 計算的 TA 已經是錯的
      → 無法即時補償
  2. 巨大的多普勒頻移（Large Doppler Shift）：

      衛星速度非常高（LEO 約 7.8 km/s），
      會把無線波拉伸或壓縮，造成頻率偏移。

      5G 的 OFDM 波形對頻率誤差非常敏感，
      只要錯一點點，就會無法解調。
  ### 解決方法
  
  上行預補償（uplink pre-compensation）：
 
   UE 在傳送前自己修正延遲與多普勒問題，不再由 gNB 幫它修正。
   因此 UE 必須知道兩件事：1)自己的精準位置（透過內建 GNSS）2)衛星的精準位置與速度（透過系統廣播的「衛星星曆」ephemeris data）
 
   取得這些資料後，UE 會做兩種計算：
   
   1. Timing Advance 預補償（TA Pre-compensation）
 
      UE 計算訊號到衛星的單向傳播延遲：
      Delay=Distance/c   *c為光速
 
      然後 UE 提前這麼多時間發送訊號，
      讓訊號剛好在正確時間到達衛星接收器。

   2. 多普勒預補償（Doppler Pre-compensation）
      
      UE 計算自己與衛星之間的相對速度，
      並對上行訊號施加相反方向的頻率偏移（pre-shift）。

      如此一來，無線訊號在傳輸過程中受到多普勒效應「拉回到正確頻率」，
      最後到達衛星時頻率剛好正確。


## 五.LEO 衛星特性與基本參數
  
![NTN_Fig1](https://github.com/user-attachments/assets/96f8afb3-c615-45de-9ac8-b3370c56f2dc)

針對LEO做介紹

LEO軌道特性

* 軌道高度：介於 500 km – 2,000 km 之間 (3GPP模擬常用600/1200km)
* 移動速度：約 7.5 km/s
* 週期：約 90 – 120 分鐘 繞行地球一圈
* 傳播延遲 (Propagation Delay)
  * 單向延遲 (One-way Delay) 約為2ms - 10ms
  * RTT(Round Trip time) 約 8 ms – 40 ms (UE 到 SAT 在從 SAT 到 gNB)所以是4倍(Ttransparent Mode)
* 多普勒頻移(Doppler Shift)
  * 在S-band(2Ghz)最大多普勒頻移大約為± 50.0 kHz
  * 基本計算公式 $$f_d = \frac{v_r}{c} \cdot f_c$$
* 路徑耗損
  * 自由空間損耗 (Free-Space Path Loss,FSPL)隨距離，在衛星高度600km使用S-band下大約為174 db 代表訊號強度會衰減 $10^{17.4}$ 倍
  * 基本計算公式 $$Loss = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$

[note] S-band 根據IEEE定義，S-band指的是頻率範圍在 2 GHz – 4 GHz，是目前 3GPP 針對非地面網路 (NTN) 專門劃分的頻段。常使用s-band是因為它具備較強的抗雨衰能力，且其波長適合整合進普通智慧型手機的天線設計中。

[note] FSPL 因為能量擃散而產生的衰減；能量向四面八方均勻發射能量，能量會平均分布在一個球型表面上，而距離越長代表表面積越大，所以單位面積接收到的功率密度之大幅下降。
 

## 六.System information blocks Type 19 (SIB 19)

### 摘要
  SIB19是3GPP在[TS 38.331 R17](https://www.etsi.org/deliver/etsi_ts/138300_138399/138331/18.05.01_60/ts_138331v180501p.pdf)中新加入的，專為NTN設計的SIB，裡面包含了ntn的資訊如星曆資料、共同定時偏移等，SIB19對於NTN的接入是必要的如果沒有，UE將會無法接入，SIB19裡面包含幾個重要參數ntn-Config、t-Service等，在r18又針對LEO高速移動的特性，加入numberOfMsg4HARQ-ACK-Repetitions、t-ServiceStart等參數。
 ### 接受到後的動作
   當ue接收到sib19時，會啟動或是重啟T430 timer，數值應設為該serving cell的ntn-UlSyncValidityDuration，計時應從該cell的 epochTime（參考時間點）開始計算。
   
[note] T430 timer是NTN特有的計時器用來監控上行同步資訊是否過期。 如果T430過期代表UE知道的衛星位置資訊已經太舊，誤差大到不能再傳送，必須停止上行傳輸並刻重新讀取 SIB19 以更新衛星軌道參數，到新的 SIB19後才能繼續傳送資料。
### SIB19重要的參數
```
SIB19-r17 ::= SEQUENCE {
 ntn-Config-r17 NTN-Config-r17 OPTIONAL, -- Need R
 t-Service-r17 INTEGER (0..549755813887) OPTIONAL, -- Need R
 referenceLocation-r17 ReferenceLocation-r17 OPTIONAL, -- Need R
 distanceThresh-r17 INTEGER(0..65525) OPTIONAL, -- Need R
 ntn-NeighCellConfigList-r17 NTN-NeighCellConfigList-r17 OPTIONAL, -- Need R
}
```
<table>
  <tr>
    <td>ntn-Config NTN 配置</td>
    <td> <a href="https://github.com/Kuan-K/2025_kuan_project/edit/main/NTN.md#ntn-config">
        衛星資料 </a> </td>
  </tr>
  <tr>
    <td>t-Service 服務截止時間</td>
    <td>告訴UE這顆衛星什麼時候會飛離服務範圍、停止服務，讓手機提前做好斷線重連或切換的準備</td>
  </tr>
  <tr>
    <td>referenceLocation 參考位置</td>
    <td>對於固定對準地面的衛星，提供一個地面的基準座標</td>
  </tr>
  <tr>
    <td>distanceThresh 距離臨界值</td>
    <td>規定手機移動超過多少距離需要重新進行定位量測，在 LEO 高速移動時可判斷UE是否還在服務區，單位是50m</td>
  </tr>
  <tr>
    <td>ntn-NeighCellConfigList 鄰區清單</td>
    <td>列出附近其他衛星的資料。如果這顆衛星快飛走了，手機可以提前看這張清單，準備換手（Handover）到下一顆</td>
  </tr>
  <table>

### NTN-CovEnh與SatSwitchWithReSync(R18針對LEO新加入的)
```
NTN-CovEnh-r18 ::= SEQUENCE {
  numberOfMsg4HARQ-ACK-Repetitions-r18 BIT STRING (SIZE(4)),
  rsrp-ThresholdMsg4HARQ-ACK-r18 RSRP-Range OPTIONAL -- Need R
}

SatSwitchWithReSync-r18 ::= SEQUENCE {
  t-ServiceStart-r18 INTEGER (0..549755813887) OPTIONAL, -- Need R
  ssb-TimeOffset-r18 INTEGER (0..159) OPTIONAL -- Need R
```
<table>
  <tr>
    <td>numberOfMsg4HARQ-ACK-Repetitions Msg4 重複傳送次數</td>
    <td>在連線初期RACH中的Msg4，手機回報收到的訊號要回傳幾次(1,2,4,8)，在訊號很弱的衛星環境下，確保gNB一定能聽見UE的回應</td>
  </tr>
  <tr>
    <td>rsrp-ThresholdMsg4HARQ-ACK 啟動重複傳送臨界值</td>
    <td>手機量測收訊品質，如果低於這個門檻，執行Msg4 重複傳送的機制</td>
  </tr>
  <tr>
    <td>t-ServiceStart 開始服務時間</td>
    <td>新衛星預計何時開始覆蓋UE所在的區域</td>
  </tr>
  <tr>
    <td>ssb-TimeOffset SSB 時間偏移</td>
    <td>告訴手機下一顆衛星發出的同步訊號（SSB），跟現在這顆衛星在時間上差了幾個子幀（subframe）</td>
  </tr>
  <table>

### ntn config
重要的參數與資訊
```
  NTN-Config-r17 ::= SEQUENCE {
      epochTime-r17 EpochTime-r17 OPTIONAL, -- Need R
      ntn-UlSyncValidityDuration-r17 ENUMERATED{ s5, s10, s15, s20, s25, s30, s35,
                                                     s40, s45, s50, s55, s60, s120, s180, s240, s900} OPTIONAL
      cellSpecificKoffset-r17 INTEGER(1..1023) OPTIONAL, -- Need R
      kmac-r17 INTEGER(1..512) OPTIONAL, -- Need R
      ta-Info-r17 TA-Info-r17 OPTIONAL, -- Need R
      ephemerisInfo-r17 EphemerisInfo-r17 OPTIONAL, -- Need R
      ta-Report-r17 ENUMERATED {enabled} OPTIONAL, -- Need R
```
<table>
  <tr>
    <td>欄位名稱</td>
    <td>說明</td>
  </tr>
  <tr>
    <td>epochTime 參考時間點</td>
    <td>星曆資料的「起算時間」；所有軌道計算都要有一個開始的時間點，讓UE知道這組座標是哪一秒開始生效的</td>
  </tr>
  <tr>
    <td>ntn-UlSyncValidityDuration 上行同步有效期限</td>
    <td>資訊的「保存期限」；衛星移動很快，這一秒的資料可能下一秒就不能用了，這個數值也是T340 Timer的總長度時間到就會重抓SIB19</td>
  </tr>
  <tr>
    <td>cellSpecificKoffset 小區特定偏移量</td>
    <td>訊號傳輸的「緩衝預留時間」，衛星與UE距離太遠，這個參數告訴UE排程時要額外多等幾個slot，才不會訊號沒到就過期</td>
  </tr>
  <tr>
    <td>kmac gNB端偏移量</td>
    <td>gNB端的「定時微調」，當上下行時間沒對準，用此參數來修正</td>
  </tr>
  <tr>
    <td>TA-Info 定時提前(TA)資訊</td>
    <td>共同定時提前量、漂移率、變化率</td>
  </tr>
  <tr>
    <td>ephemerisInfo 衛星資訊</td>
    <td>衛星的位置與速率</td>
  </tr>
  <tr>
    <td>ta-Report TA 報告</td>
    <td>啟用「回報機制」，告訴手機在連線時，是否要向基地台回報自己計算出的 TA 補償資訊。</td>
  </tr>
</table>

#### TA info
```
  TA-Info-r17 ::= SEQUENCE {
      ta-Common-r17 INTEGER(0..66485757), # 共同定時提前量
      ta-CommonDrift-r17 INTEGER(-257303..257303) OPTIONAL, -- Need R # 共同 TA 漂移率
      ta-CommonDriftVariant-r17 INTEGER(0..28949) # 共同 TA 漂移變化率
```
#### ephemerisInfo
```
PositionVelocity-r17 ::= SEQUENCE {
  positionX-r17 PositionStateVector-r17, # x軸座標
  positionY-r17 PositionStateVector-r17, # y軸座標
  positionZ-r17 PositionStateVector-r17, # z軸座標
  velocityVX-r17 VelocityStateVector-r17, # x軸速率
  velocityVY-r17 VelocityStateVector-r17, # y軸速率
  velocityVZ-r17 VelocityStateVector-r17  # z軸速率
```

### oai程式碼對照SIB19關鍵參數

在oai的NTN_LEO的gNB conf檔中

<img width="695" height="228" alt="image" src="https://github.com/user-attachments/assets/54719e49-08ad-455c-8ed2-1544b1ab730a" />

包含 UlSyncValidityDuration、cellSpecificKoffset 與 TA info、ephemerisInfo都可以對照，做修改調整。

### TA vs koffset

TA 在 PHY 層實作，是因為衛星距離太長，所以提前做物理上的補償，讓訊號準時在到 gNB 

koffset 在MAC/RLC 也是因為衛星距離太長，所以告訴gNB訊號會較晚才發送到，讓gNB等待而不直接判定為沒收到

兩個雖然都是類似的東西但在不同層執行 以現實中例子來講

TA就像司機到你家需要20分鐘就會提前20分鐘出發確保準時，而koffset像是行事曆如果你知道這是國際的包裹你就會預設，他可能會需要好幾天才會送到，不會再一天沒收到就打電話給客服說沒收到。


## 七.UE 的 NTN 接取流程
### flowchart
<img width="649" height="771" alt="flowchart about UE(RACH)" src="https://github.com/user-attachments/assets/8651b26c-de13-4d8b-bcca-c8c0f463f2a7" />

從gNB廣播MIB/SIB1/SIB19 UE 接收到資訊後，透過GNSS知道自身位置後計算預補償，接著進入RACH
[note]
* 在TRAN模式中所有UE與gNB傳送資料都須經過SAT
* 在REGEN模式中SAT即是gNB
  
### MSC
#### TRANS Mode
  <img width="721" height="602" alt="MSC about TRANS" src="https://github.com/user-attachments/assets/042ef218-5926-4c1f-8610-6b33bb1846b8" />


#### REGEN Mode
  <img width="481" height="602" alt="MSC about REGEN" src="https://github.com/user-attachments/assets/2a092889-f8b3-4df8-970d-52bf15909be7" />

### 接取流程解析

#### 1.Cell Search
UE 會掃描 S-band 頻段，尋找 PSS (主同步訊號) 與 SSS (輔助同步訊號)。 當成功找到並同步，UE 成功鎖定Cell並解析出 MIB

#### 2.讀取SIB1/SIB/SIB19
UE 解析 SIB19獲得星曆資料、Epoch Time 與 ta-common等資料

#### 3.UE 自主定位與計算 (GNSS & Self-Location)
UE 啟動內建的 GNSS (如 GPS) 以獲取自己的經緯度與高度。
* 算距離：UE 計算自身位置與 SIB19 提供之衛星位置間的直線距離 D
* 算延遲：計算單向傳播延遲 $T = D / c$
* 算頻移：計算都普勒頻移

#### 4.預補償 (Pre-compensation)
* 時間補償：UE 會主動提前發送訊號，提前的時間為$2 \times T + ta-common$
* 頻率補償：UE 將上行頻率主動加上或減去都普勒頻移
#### 5.隨機接入(RACH)
如同前面介紹的RACH
不過在NTN中，因為訊號跑很久，基地台會透過 SIB19 告知一個 k-Offset，讓 UE「等久一點」再開啟接收視窗，避免過早放棄連線。

在LEO因為極大的都普勒頻移常在這裡出現RAR reception failed 或是 RAR received but preamble doesn’t match的狀況
