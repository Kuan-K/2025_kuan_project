# Open RAN study note

> Reference :
>   https://www.sharetechnote.com/html/OpenRAN/OR_WhatIsIt.html
> 
>   https://www.sharetechnote.com/html/5G/5G_RAN_Architecture.html
>
>   http://sharetechnote.com/html/OpenRAN/OR_WhereToSplit.html

## topic

1. [摘要](#摘要)
2. [ORAN 怎麼分](#ORAN-怎麼分)
3. [為什麼要分(優勢)](#為什麼要分-(優勢))
4. [挑戰(劣勢)](#挑戰-(劣勢))


## 摘要

  RAN (Radio Access Network) 是一種在通訊中UE與core network之間傳輸節點的統稱，在5G NR內叫做gNB

  ORAN(open RAN) 以5G NR 為例:是將5G protocol stack 內的RRC PDCP RLC MAC 與PHY層去做虛擬化、軟體化，將功能拆分
  讓大家能打破單一廠商的綁定，將過去被鎖在傳統設備的黑盒子被打開，讓大家能使用同類最佳，將不同部分的較好的物件合在一起。

## ORAN 怎麼分

<img width="897" height="881" alt="image" src="https://github.com/user-attachments/assets/d907a02d-d399-4c50-935f-63f8510fd317" />

quote from : [resource](http://sharetechnote.com/html/OpenRAN/OR_WhereToSplit.html)

OARN 一般切割為分為 CU、DU與RRU(RU) ， 切法有很多種視使用者的需求所切分

CU 與 DU 切分在 option2 並以F1介面連接
而 DU 與 RRU 切在option7 並以eCPRI 介面連接

## 為什麼要分(優勢)

將 CU 與 DU 拆開後可以
* 降低成本
* 提高靈活度
* 減少廠商綁定
* 提高可擴展性
* 增加競爭 (同類最佳)

## 挑戰 (劣勢)
* 效能問題 : 軟體化會產生較大的延遲
* 前期投入成本高
* 技術還不成熟
* 缺乏共通標準(產業尚未完群遵守O-RAN 規範)
