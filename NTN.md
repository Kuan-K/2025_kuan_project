# Study Note: NTN backgroumd knowledge

> Reference :
>   https://hackmd.io/D7pXmmKXQf-7enZbBZy8cw
> 
>   3GPP TR 38.821
> 
>   3GPP TS 38.211 

## TOC
1. 摘要
2. 5G NR協定
3. NTN架構
4. NTN 的主要問題
5. 延遲補償（Delay Compensation）

---

## 1. : 摘要
  NTN技術就是整合衛星與5G架構，藉由衛星來連接，擴大服務範圍，讓沒有辦法架設硬體的偏遠地區也能受到服務。
  ![NTN_Fig1](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/3GPP%20NTN%20Architecture%20Overview.png)
* User Equipments (UE) : 使用者設備，例如手機
* Satellite : 衛星
* Gateway : 地面閘道站
* Service link：UE 與衛星之間的連線
* Feeder link：衛星與Gateway之間的連線
* Beam footprint：衛星波束覆蓋的區域
### NTN有兩種模Ttransparent Mode 與 Regenerative Mode，兩種架構圖如下:
  
   Ttransparent Mode：衛星只做轉傳信號，不做處理信號，只是作為一個點接收訊號後直接傳送不會動到訊號。 方塊圖 [trans](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%96%B9%E5%A1%8A%E6%A8%A1%E6%93%AC%E5%9C%96leo_tran_F.png)
   
   Regenerative Mode：衛星可做解碼處理信號，衛星像是一個太空中的基地台，而不只是轉傳訊號。 方塊圖 [regen](https://github.com/Kuan-K/2025_kuan_project/blob/main/%E7%AD%86%E8%A8%98%E5%9C%96%E7%89%87/%E6%96%B9%E5%A1%8A%E6%A8%A1%E6%93%AC%E5%9C%96leo_regen_F.png)
   
  ![NTN_Fig2](https://github.com/user-attachments/assets/3c7a4f8f-ef87-4388-ba6c-236efd8d0433)
## 2. : 5G NR協定堆疊(Protocol Stack)
  在3GPP NTN 中，無線介面沿用 5G NR Protocol Stack。
  
  <img width="355" height="391" alt="image" src="https://github.com/user-attachments/assets/807024da-4f9e-4055-8ce0-f7982d86ae3d" />
![NTN_Fig2]


## 4. : NTN 的主要問題

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

     3GPP的解法是：讓HARQ 回饋（feedback）變成可設定項(LEO必較有可能)，
     並在許多情況下直接關閉。
     
     *** HARQ/ARQ
     
         HARQ(Hybird Automatic Repeat Request)：
     
         當接受訊號有錯，如果錯誤是微小的則自動修復，如錯誤過大則請求重傳，並將新資料與舊資料合併再解碼
     
         ARQ：
     
         經過Hard處理後訊號大多已完整，或是訊號剩下可接受的範圍，而ARQ負責處理HARQ的殘餘錯誤，發現錯誤後直接丟棄不做合併。

         *HARQ在PHY運作，由MAC控制
          ARQ在RLC層運作

  2. 可靠性：
     
    當 HARQ 被關閉後，
    可靠性機制會上移到更高一層 —— RLC 層的「確認模式（Acknowledged Mode, RLC-AM）」。
    RLC-AM 雖然速度較慢，
    但能在長延遲環境下運作，
    確保資料在遺失時仍能被重新傳送。

  ## 4. Task 4: 延遲補償（Delay Compensation）
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
