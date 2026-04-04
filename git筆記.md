## 基本指令
```
git status #確認狀態
```

## 連結 repo
```
git init
git remote add origin https://github.com/你的帳號/專案名稱.git
```

## 更新(push)
```
git add .
git commit -m "你的更新訊息"
git push -u origin main # 第二次開始使用 git push 就好
```
## 建立忽略檔
```
echo "要忽略的檔案" > .gitignore # 之後push就不會push這個檔案(通常是執行檔)

git rm --cached [要忽略的檔案] #如果之前不小心複製過
```
## 下載
```
git clone https://github.com/你的帳號/專案名稱.git
```

