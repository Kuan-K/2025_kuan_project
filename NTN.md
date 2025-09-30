# Study Note: NTN backgroumd knowledge

## TOC
1. HARQ/ARQ
2. TTI building

---

## 1. Task 1: HARQ/ARQ
  ![Screenshot_20250930_200938_Samsung Notes](https://github.com/user-attachments/assets/e802406d-474d-4884-af05-803a3b6fd688)

## 2. Task 2: TTI building
  在UE環境不好時會一直傳送與等待 ACK/NACK的訊號，會增加控制開銷與延遲，TTI building的技術就是將多個RV整合成一個TTI bundle 傳輸，
  這樣就只會收到一次 ACK/NACK的訊號提升上行率
