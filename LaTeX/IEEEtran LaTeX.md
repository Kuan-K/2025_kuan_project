# Study Note: IEEEtran LaTeX

## TOC
1. Introduction
2. CLASS OPTIONS
3. THE CLASSINPUT, CLASSOPTION AND CLASSINFO CONTROLS
4. THE TITLE PAGE
5. ABSTRACT AND INDEX TERMS
6. SECTIONS
7. CITATIONS
8. EQUATIONS
9. MULTI-LINE EQUATIONS
10. FLOATING STRUCTURES
11. LISTS
12. THEOREMS AND PROOFS
13. END SECTIONS
14. LAST PAGE COLUMN EQUALIZATION
---

## 1. Task 1: introduction
  心得與資料
  1. LaTex可以能快速且低成本，就能做很好的排版。
  2. conference 與 journal的差異，前者篇幅較短，更新快但相對後者沒那麼嚴謹
  3. 有4大bare bones範例模板可以快速產生論文的格式
## 2. Task 2: CLASS OPTIONS
  IEEEtran有許多列類別選項控制模式與行為 且每項都是明確切獨立的
  
  字體大小 預設為10pt （大多數論文）
  technote 9pt
  部分conference 首次會使用11pt
  IEEEtran會自動微調字級
  
  草稿模式 會有雙倍行 距邊界為1in
  draft 不繪出圖
  draftcls 有圖
  draftclsnofoot 有圖但不顯示頁腳日期
  
  五種主要模式conference journal technote peerreviewed peerreviewca
  匿名模式會產生單欄封面頁含標題作者摘要
  coinference 邊界加大 頁腳不顯示頁碼
  
  comsoc 影響數學字型 更接近Time Roman
  compsoc 字型為Palatine 章節改為阿拉伯數字 如想用傳統conference 模式不要開compsoc模式
  transmag 使用長格式輸入 標題使用較小的粗體 可用endfloat.sty將圖集中至文末
  
  紙張 Us letter(IEEE主要) A4
  conference/journal 改邊界不改排版
  compsoc邊界固定 有可能影響排版


附錄預設為A B...編號也可使用羅馬數字
## 3. Task 3: THE CLASSINPUT, CLASSOPTION AND CLASSINFO CONTROLS
  IEEEtran 有三類特殊命令，讓類別檔與使用者文件互通資訊
  CLASSINPUT 輸入值 客製化行為
  CLASSOPTION 輸出旗標 可對列別選項作條件式編譯
  CLASSINFO 輸出資訊 查詢執行環境

  CLASSINPUTs

  \CLASSINPUTbaselinestretch（行距）
  \CLASSINPUTinnersidemargin（內側邊界）
  \CLASSINPUToutersidemargin（外側邊界）
  \CLASSINPUTtoptextmargin（上邊界）
  \CLASSINPUTbottomtextmargin（下邊界）
  CLASSINPUT 的好處是 IEEEtran 能同步調整其他內部參數
  壞處則是可能產生不符合IEEE標準的文件

  CLASSOPTIONs

  \CLASSOPTIONpt 點數大小
  \CLASSOPTIONpaper 字型
  *CLASSOPTION視為唯獨，IEEEtran用它們來判斷版式，不要擅自更改

  CLASSINFOs

  \ifCLASSINFOpdf 判斷是否為PDF輸出
  \CLASSINFOnormalsizebaselineskip 長度
  \CLASSINFOpaperwidth 與 \CLASSINFOpaperheight 字串巨集
## 4. Task 4: THE TITLE PAGE
  以標準 \maketitle 產生，呼叫需前先宣告標題、作者、隸屬單位等
  A
  標題需要大寫 介係詞、冠詞、連接詞不在首位可不用大寫
  可用"\\"換行調整長度
  不要使用數學和特殊符號
  
  B
  journal/tectnote Mode
  
  \IEEEmembership{}會員身分
  \thanks{} 產生第一註腳*若要產生多個須拆開產生
  
  conference Mode
  
  \IEEEauthorblockN{}作者姓名
  \IEEEauthorblockA{}隸屬單位 用\and做分隔
  
  compsoc journal Mode
  \IEEEcompsocitemizethanks 作者隸屬以條列放在第一個註腳中
  
  compsoc conference Mode
  與conference模式相同
  
  Transmag journal Mode
  長格式 姓名與位址各一行 不列Email跟電話
  
  C
  \markboth{<期刊名與卷期日期>}{<作者與題名縮寫>}
  期刊名會自動轉大寫 須小寫可用\MakeLowercase{}
  雙面期刊中 第二引數只用於右頁跑頭
  tectnote不須第二引數 conference沒有跑頭
  匿名的跑頭不要放作者資訊
  
  D
  \IEEEpubid{0000--0000/00\$00.00~\copyright~2015 IEEE}
  投稿時雖未有正式編號，但可預先檢查版面占用
  conference不放出版編號IEEE會自動在頁底留白
  draft 會留空間但不印編號
  compSoc journal會將編號放在頁底邊界不影響文字高度
  
  E
  例如邀稿論文 \IEEEspecialpapernotice{(Invited Paper)}
  journal/technote出現在作者名與本文之間
  conference出現在標題與作者名之間
## 5. Task 5: ABSTRACT AND INDEX TERMS
  摘要
  \begin{abstract}
    ...
  \end{abstract}
  
  索引詞
  \begin{IEEEkeywords}
    Broad band networks, quality of service, WDM.
  \end{IEEEkeywords}
  不建議在摘要使用數學式與特殊符號
  可向keywords@ieee.org取得可用關鍵詞列表
  
  compsoc journal與 transmag 中，摘要與索引詞應以單欄、放在作者資訊之後
  \IEEEtitleabstractindextext{} 可用此段程式讓摘要與索引詞顯示於作者名後的單欄  
  其他格式則放在本文第一欄之前
## 6. Task 6: SECTIONS
  LaTeX語法宣告 \section \subsection \subsubsection \paragraph
  compsoc mode 子章節 一律使用阿拉伯數字
  其他模式下各層依序是 大寫羅馬數字 大寫英文字母 阿拉伯數字 小寫英文字母
  technote與compsoc conference 通常不允許\paragraph
  
  首字下沉 放大第一個字母並下降一行
  \IEEEPARstart{W}{ith} 第一個引數是首字，第二則是該詞剩餘字母
## 7. Task 7: CITATIONS
  一律使用 \cite 同一組相鄰的多個引文（務必在同一個 \cite{...} 中用逗號分隔
## 8. Task 8: EQUATIONS
  單行方程式用：
  \begin{equation}
  \label{eqn_example}
  x = \sum\limits_{i=0}^{z} 2^{i}Q
  \end{equation}
  
  如果不需要編號則使用displaymath
  IEEE雙欄版對方程式寬度限制很嚴格，大多數過寬公式應拆成多行
## 9. Task 9: MULTI-LINE EQUATIONS
  最常見的做法是 LaTeX 2ε 的 eqnarray
  缺點是
  1.欄間距不自然
  2.欄定義不能更改
  3.只能三欄對齊
  4.欄內不能覆寫對齊
  更好的選擇可用 AMS 的 amsmath
  提供多行對齊的環境跟很多工具

  數學間距觀念
  <img width="340" height="127" alt="image" src="https://github.com/user-attachments/assets/fcb06a1e-6350-41be-93cd-ad2dc1c96434" />
  
  若分段函數的每一支都需要能以不同的方程式編號引用
  \begin{numcases}{|x|=}
   x, & for $x\ge 0$\\
   -x,& for $x< 0$
  \end{numcases}
  用cases.sty中的numcase/subnumcases
  *如需同時使用amsmath與cases.sty先載入前者否則會出現錯誤

## 10. Task 10: FLOATING STRUCTURES
  多數 IEEE 期刊偏好把浮動體放在頁首，幾乎不會用頁底
  IEEE Computer Society偶爾會放在底頁
  LaTeX 會把腳註放在頁底浮動體上方
  
  \begin{figure}[!t]
  \centering
  \includegraphics[width=2.5in]{myfigure}
  \caption{Simulation results for the network.}
  \label{fig_sim}
  \end{figure}
  
  圖（Figures）
  \centering 置中
  圖說在圖後
  \label 必須在 \caption 之後（或其內），否則交叉參照會指到章節號而非圖號。
  
  子圖（subfigures）
  建議用 subfig.sty 務必加 caption=false 避免相依的caption.sty格式被改寫
  
  演算法（Algorithms）
  IEEE 規範將不屬於正文流程的演算法放在figure 浮動體中
  
  表（Tables）
  表題置於表格之前，視為標題，除短詞外字首大寫
  表格內預設字級是 \footnotesize
  
  跨雙欄浮動體（Double Column Floats）
  figure* / table* 產生跨雙欄的圖表
  LaTeX 2ε 無法把跨欄浮動體放在頁底
  技術上可以用 figure* 放置跨欄公式，但 IEEE 極少使用（容易浪費空間）
  *注意
  由上而下方程式編號必續遞增
  跨欄公式應出現在被引用的那一頁
  跨欄公式的環境提前定義於前一頁
  不允許其他圖表插在跨欄公式與主文本之間
## 11. Task 11: LISTS
  全域控制 \IEEEiedlistdecl
  區域控制\itemize, \enumerate, \description
  A. enumerate（編號清單）
  \labelwidth 預設以正常字級寬度9為準
  以下狀況必須手動調整labelwidth
  外層清單超過9項
  重新定義\labelenumX 或 \theenumX
  用了\item[X] 或 非預設字級/字型
  清單是巢狀
  
  範例：預先把最長標籤寬度設為12
  \begin{enumerate}[\IEEEsetlabelwidth{12)}]
  
  B. itemize（條列清單）
  itemize 也遵循 IEEE 版式如需調整須放在全域的 \IEEEiedlistdecl，或清單的可選引數裡調整
  C. description（描述清單）
  必須指定最長標籤
  D. 進階長度與巢狀縮排
  \IEEElabelindent IED 清單標籤盒相對頁邊的縮排
  \IEEEiednormlabelsep：標籤盒到清單文字的一般間距
  \IEEElabelindentfactori … \IEEElabelindentfactorvi：自動縮排回退係數
## 12. Task 12: THEOREMS AND PROOFS
  struct_type環境名稱
  struct_title顯示的標頭
  A. 證明（Proofs）
  \begin{IEEEproof}
    ...
  \end{IEEEproof}
## 13. Task 13: END SECTIONS
  A. 附錄
  單一附錄：用 \appendix  
  \section 會停用不再有編號章節
  \appendix[Proof of the Zonklar Equations]
  
  多個附錄：用 \appendices
  用 \section 各自宣告每一個附錄章節
  \appendices
  \section{Proof of the First Zonklar Equation}
  B. 致謝
  基本寫法 \section*{Acknowledgment}
  C. 參考文獻
  \bibliographystyle{IEEEtran}
  \bibliography{IEEEabrv,mybibfile}
  強烈建議將編譯出的.bbl直接貼回論文
  避免依賴外部檔案減少重編時異動風險
  D. 作者簡歷
  \begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{./shell}}]{Michael Shell}
  ...
  \end{IEEEbiography}
  照片區域大小：1 in × 1.25 in。建議灰階 220 dpi、8 bits/sample。
## 14. Task 14: LAST PAGE COLUMN EQUALIZATION
  IEEE會把最後一頁的兩欄控制得差不多高(不會完全一樣)
  相機就緒（camera-ready）時特別重要
  在最後一頁第一欄頂端附近放 \enlargethispage{-X.Yin}
  *提醒：論文內容變動後，等高的參數通常要重調。
