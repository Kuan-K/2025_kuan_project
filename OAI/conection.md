# Study Note: 接取流程步驟

> Reference :
> 
> 

# TOC
1. 摘要
2. AKA 回應與細節

---

## 1 摘要

要連上網的步驟

* UE (顧客/會員) 
* gNB (俱樂部/酒店員工)
* core network (公司高管/核心資料庫)

1. 同步 (顧客決定要去哪一間 確認是不是要那間)

2. RACH (到門口敲門等待 與保全對接)

3. RRC conection (進入俱樂部)

4. AKA 回應 (確認身分連上網)

5. PDU Session (可以傳送資料)

## 2 AKA 回應與細節

AKA 總共有6步

1. UE 將自己的身分碼加密成SUCI(Subscription Concealed Identifier)

2. core 收到請求後 計算出一組認證向量 包含 (RAND、AUTN、HXRES、K<sub>SEAF</sub>)

3. 透過基地台將 RAND AUTN 回傳給UE

4. UE 接收到資料 檢查AUTN是否正確 使用內部的金鑰 K計算出結果RES 並產生與core 同步的金鑰K<sub>amf</sub>

5. UE 回傳答案

6. core 對答案 並將金鑰 傳給gNB

* SUCI(Subscription Concealed Identifier) 將ISIM key 加密後的結果
* RAND 隨機數 (題目)
* AUTN (Authentication Token) 用來證明自己是真的基地台 (浮水印)
* HXRES* 預期回應值(謎底)
* K<sub>SEAF</sub>加密金鑰
