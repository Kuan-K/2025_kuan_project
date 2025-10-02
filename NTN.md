# Study Note: NTN backgroumd knowledge

## TOC
1. HARQ/ARQ
2. TTI building
3. LEO/MEO/GEO/HEO
4. Payload

---

## 1. Task 1: HARQ/ARQ
  ![Screenshot_20250930_200938_Samsung Notes](https://github.com/user-attachments/assets/e802406d-474d-4884-af05-803a3b6fd688)

## 2. Task 2: TTI building
  在UE環境不好時會一直傳送與等待 ACK/NACK的訊號，會增加控制開銷與延遲，TTI building的技術就是將多個RV整合成一個TTI bundle 傳輸，
  這樣就只會收到一次 ACK/NACK的訊號提升上行率
## 3. Task 3: LEO/MEO/GEO/HEO
  ![Screenshot_20251002_205757_Samsung Notes](https://github.com/user-attachments/assets/d76133af-b732-4575-9ba0-6df81f55a1c0)
  
## 4. Task 4: Payload
  Payload 有效載荷 : 指搭載在飛行器上真正執行任務的部分
  
  Non-regenerative payload 與 regenerative payload
  Non-regenerative payload:只單純傳送信號，當中繼站做頻率轉換、濾波、放大、下行轉發
  regenerative payload:可做訊號處理，等同在太空中的基地台

  spaceborne/airborne platform 天基/空基平台(兩者都是把通訊設備載上天空)
  spaceborne platform : 在太空中，最常見的就是衛星
  airborne platform : 在大氣層中，HAPS、旋翼無人機等 (高度約為8-50km)
  
  ![Screenshot_20251002_220752_Samsung Notes](https://github.com/user-attachments/assets/7d85fd2c-0c11-4526-88a9-164289b4f140)
