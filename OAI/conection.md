# Study Note: 接取流程步驟

> Reference :
> 
> 

# TOC
1. 摘要
2. AKA 回應與細節
3. Flowchart
4. MSC
5. oai程式碼

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

* SUPI(Subscription Permanent Identifier) 身分代碼
* SUCI(Subscription Concealed Identifier) 將SUPI 加密後的結果
* RAND 隨機數 (題目)
* AUTN (Authentication Token) 用來證明自己是真的基地台 (浮水印)
* HXRES* 預期回應值(謎底)
* K<sub>SEAF</sub>加密金鑰

## 3 Flowchart

<img width="522" height="1042" alt="connection_flowchart" src="https://github.com/user-attachments/assets/e6623491-77cd-4f58-8137-4a6d595220ed" />

## 4 MSC 

<img width="829" height="1103" alt="connection_MSC" src="https://github.com/user-attachments/assets/9e4383c6-1e7e-4835-92bc-1e781d38c35b" />


## 5 oai程式碼

### TN vs NTN

在NTN與TN中gNB 的config 檔中程式碼沒有太大的修改，除了修改一些參數的值，最主要就是增加[SIB19與衛星的速度及位置的資訊](https://github.com/Kuan-K/2025_kuan_project/blob/main/NTN.md#oai%E7%A8%8B%E5%BC%8F%E7%A2%BC%E5%B0%8D%E7%85%A7sib19%E9%97%9C%E9%8D%B5%E5%8F%83%E6%95%B8)

UE 的 [command](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/NTN_exercise.md#start-the-nrue)也沒有 出現IFDEF的參數，所以AKA 認證TN 是一樣的


### 程式摘要
 OAI 透過 呼叫milenage_generate() 來進行AKA認證與生成金鑰的演算法，底層數學核心邏輯式AES-128

 milenage 會接 根金鑰(K<sub>i</sub>)、電信商金鑰(OP<sub>c</sub>)、隨機碼(RAND) 並對資料加密及解密

 | 函式名稱 | 功能 | 說明 |
|:---:|:---:|:---:|
| `f1` | `計算MAC-a與MAC-s` | UE用來驗證基地台送來的AUTN是否合法 |
| `f2` | `計算RES(response)` | UE要回傳的答案證明自己是合法UE |
| `f3` | `計算CK(confidentiality key)加密金鑰`  | 後續傳送的資料會以它加密 |
| `f4` | `計算IK(integrity key)完整性金鑰` | 確保後資料完整性 |
| `f5` | `計算AK(anonymity key)匿名金鑰` | 用來將SQN(序號)隱藏起來 |

### [milenage.h](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/oai_codes/milenage.h)

#### [f1 函式](https://github.com/Kuan-K/2025_kuan_project/blob/72784d93f2b5b62efb7aadfbeab3d65ef148ef28/OAI/oai_codes/milenage.h#L63)

input : opc,k,_rand,sqn,amf
output : mac_a,mac_s


加密過程先將RAND 與 opc 做 XOR 接著呼叫aeS-128使用金鑰K加密並存到tmp1

公式： $TEMP = E_K(RAND \oplus OP_c)$
```
 for (i = 0; i < 16; i++)
    tmp1[i] = _rand[i] ^ opc[i];

  aes_128_encrypt_block(k, tmp1, tmp1);
```

接著將SQN與amf 接在一起並重複一次存在tmp2
```
  /* tmp2 = IN1 = SQN || AMF || SQN || AMF */
  memcpy(tmp2, sqn, 6);
  memcpy(tmp2 + 6, amf, 2);
  memcpy(tmp2 + 8, tmp2, 8);
```

最後將tmp2與opc做XOR 並旋轉位移r1的長度(規範定義 $r_1 = 64$ bits，即 8 bytes)
算出的結果在與tmp1做XOR，最後呼叫aes-128使用金鑰再次加密存到tmp1 並與opc做最後的XOR

公式： $tmp3 = TEMP \oplus rot(IN1 \oplus OP_c, r_1) \oplus c_1$

公式： $OUT = E_K(tmp3) \oplus OP_c$
```
  /* rotate (tmp2 XOR OP_C) by r1 (= 0x40 = 8 bytes) */
  for (i = 0; i < 16; i++)
    tmp3[(i + 8) % 16] = tmp2[i] ^ opc[i];

  /* XOR with TEMP = E_K(RAND XOR OP_C) */
  for (i = 0; i < 16; i++)
    tmp3[i] ^= tmp1[i];

  /* XOR with c1 (= ..00, i.e., NOP) */
  /* f1 || f1* = E_K(tmp3) XOR OP_c */
  aes_128_encrypt_block(k, tmp3, tmp1);

  for (i = 0; i < 16; i++)
    tmp1[i] ^= opc[i];
```

而tmp 前8位 為mac_a、後8位 為mac_s
```
  if (mac_a)
    memcpy(mac_a, tmp1, 8); /* f1 */

  if (mac_s)
    memcpy(mac_s, tmp1 + 8, 8); /* f1* */
```


#### [f2345 函式](https://github.com/Kuan-K/2025_kuan_project/blob/72784d93f2b5b62efb7aadfbeab3d65ef148ef28/OAI/oai_codes/milenage.h#L126)

input: opc, k, rand
output: res, ck, ik, ak, akstar

先將RAND與opc做XOR，再使用AES_128與k做加密，並將結果存至 tmp2

先算不用旋轉位移的res(f2)與AK(f5)

將tmp2的結果與opc做XOR之後再XOR常數c2=1 並經過AES加密，與opc做XOR後把存入tmp3 前6bytes給ak 後面8bytes給res

接著算CK(f3)，將tmp2循環左移4bytes並與opc做XOR的結果傳入tmp1 接著與常數c3=2 做XOR 並經過AES加密 最後與opc做XOR 得出CK

繼續算IK(f4)，將tmp2循環左移8bytes並與opc做XOR的結果傳入tmp1 接著與常數c4=4 做XOR 並經過AES加密 最後與opc做XOR 得出IK

最後算AKstar，將tmp2循環左移12bytes並與opc做XOR的結果傳入tmp1 接著與常數c5=8 做XOR 並經過AES加密 最後與opc做XOR 得出aKstar

#### [milenage_generate()](https://github.com/Kuan-K/2025_kuan_project/blob/72784d93f2b5b62efb7aadfbeab3d65ef148ef28/OAI/oai_codes/milenage.h#L222)

呼叫函式計算f1~f5

將sqn與ak做XOR 並串接amf與mac_a讓AUTN變為完整的16bytes


### [nr_nas_msg.c](https://github.com/Kuan-K/2025_kuan_project/blob/main/OAI/oai_codes/nr_nas_msg.c)

當OAI的內部系統訊息 ITTI (Inter-Task Interface) 為 NAS_DOWNLINK_DATA_IND 時，會經由 swuich case 選擇後進入 case [NAS_DOWNLINK_DATA_IND](https://github.com/Kuan-K/2025_kuan_project/blob/d648d50d9135c5ea515d13ea475708860dfede11/OAI/oai_codes/nr_nas_msg.c#L2110)

當 msg_type = FGS_AUTHENTICATION_REQUEST 時 呼叫 handle_fgmm_authentication_request 去做身分認證及計算RES

#### [handle_fgmm_authentication_request](https://github.com/Kuan-K/2025_kuan_project/blob/1cd927a7a3a23e6d94ef855b753969df1e832340/OAI/oai_codes/nr_nas_msg.c#L1071)

* input
 * nas : 包含所有狀態、key、sim卡資訊
 * buffer : 原始封包
* output
 * initialNasMsg 最終要回給基地台的Authentication Response 封包
   
```
  fgmm_msg_header_t mm_header = {0};
  if ((decoded = decode_5gmm_msg_header(&mm_header, buffer->buf + size, buffer->len - size)) < 0) {
    LOG_E(NAS, "decode_5gmm_msg_header failure in NAS Authentication Request handling\n");
    return;
  }
  size += decoded;
```
呼叫解碼函式把標頭拆開，如果不是一個標準的NAS函式則直接回傳error

```
 if ((decoded = decode_nas_key_set_identifier(&msg.ngKSI, 0, buffer->buf[decoded])) < 0) {
    LOG_E(NAS, "decode_nas_key_set_identifier failure in NAS Authentication Request handling\n");
    return;
  }
  size += decoded;
```
從封包中挖出ngKSI((NAS Key Set Identifier)) 對齊金鑰

```
 generateAuthenticationResp(nas, initialNasMsg, buffer->buf);
```

呼叫 generateAuthenticationResp
傳入 nas,initialNasMsg與buffer->(只有資料沒有長度)
#### [generateAuthenticationResp](https://github.com/Kuan-K/2025_kuan_project/blob/59700c8614c7ceee2488119eaffa06d32a29ed45/OAI/oai_codes/nr_nas_msg.c#L1026)

* input
 * nas : 包含所有狀態、key、sim卡資訊
 * buf : 封包資料(陣列指標)
* output
 * initialNasMsg 最終要回給基地台的Authentication Response 封包

呼叫 [dreive_ue_keys](https://github.com/Kuan-K/2025_kuan_project/blob/ab641c689f8ca1394c8889eb6caa97ddf76f60d0/OAI/oai_codes/nr_nas_msg.c#L623)
傳入 buf,nas

```
// get RAND for authentication request 收到的封包 buf 的第8個位元開始挖出16bytes的RAND
  for (int index = 0; index < 16; index++) {
    rand[index] = buf[8 + index];
  }

  uint8_t resTemp[16];
  uint8_t ck[16], ik[16];
  f2345(nas->uicc->key, rand, resTemp, ck, ik, ak, nas->uicc->opc); // 呼叫f2345 算出RES CK IK AK

  transferRES(ck, ik, resTemp, rand, output, nas->uicc); //呼叫transferRES 計算RES*
```
拆解封包 取得RAND 呼叫f2345 與 transferRES 取得CK IK AK RES*

[note] OAI並沒有乎叫f1 取的AUTN 認證基地台

#### [transferRES](https://github.com/Kuan-K/2025_kuan_project/blob/7f5c73d26631fa3babd4bcb3151d31f0afc04c12/OAI/oai_codes/nr_nas_msg.c#L508)

呼叫 [servingNetworkName](https://github.com/Kuan-K/2025_kuan_project/blob/7f5c73d26631fa3babd4bcb3151d31f0afc04c12/OAI/oai_codes/nr_nas_msg.c#L104) 取得SNN後與rand合併

並呼叫 kdf 將結果 與 CK+IK 做計算得出 RES*

kdf會呼叫 [sha_256_hmac](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/openair3/SECU/sha_256_hmac.c#L16)
