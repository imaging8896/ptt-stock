# ptt-stock
可更改 ptt-stock/get_stat.py
註解掉重抓 PTT 的部分
```
if __name__ == '__main__':
    # c = PttWebCrawler("Stock", True, start=1, end=300)  # 重爬 PTT 並生成檔案
    # file_name = c.getFilename()

    file_name = "Stock-1-200.json"  #  用既有檔案
```

執行
```
cd ptt-stock
python get_stat.py
```
