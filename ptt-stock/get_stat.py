# -*- coding: utf-8 -*-
from PttWebCrawler import PttWebCrawler
import codecs
import requests
import json
import re
import operator
import random, time
from bs4 import BeautifulSoup
from GoogleSearchKeyword import GoogleSearchKeyword


NON_STOCK_NAMES = [
    u"股票", u"股利", u"交易", u"研究員", u"投顧", u"面試", u"網路", u"下單", u"網路下單", u"選股", u"股票價格", u"股市關係",
    u"投資人", u"所得", u"銀行", u"檔次", u"看法", u"操作", u"底部", u"每股", u"價格", u"財務", u"外汇", u"外匯",
    u"关系", u"財務報表", u"财务报表", u"主力進出表", u"基金", u"紀錄", u"買盤", u"選舉", u"你會怎麼做", u"你会怎么做", u"心態",
    u"被砍", u"閒聊", u"闲聊", u"賭盤", u"追高殺低", u"券當沖", u"當沖", u"融資", u"除息", u"除權", u"回填", u"計算", u"套利",
    u"指數", u"外資", u"大跌", u"大漲", u"分析師", u"新手", u"電腦", u"撿骨", u"法則", u"交割", u"合庫", u"獲利", u"Stock",
    u"stock", u"股市", u"書籍", u"推薦", u"財報", u"分析", u"及", u"失業率", u"台灣", u"採訪", u"一注獨買", u"心態", u"黃金",
    u"分類", u"上櫃", u"上市", u"興櫃", u"下市", u"下櫃", u"操作心得", u"心得", u"匯損", u"long", u"short", u"公司", u"討論",
    u"個案", u"問題", u"撮合", u"資產股", u"當選", u"全球股市", u"國際股市", u"全球", u"放空", u"行情", u"心理學", u"代号",
    u"代號", u"坑殺", u"高捷", u"高雄捷運", u"價值", u"清算", u"清算價值", u"資產負債表", u"當沖", u"對沖", u"权证对冲", u"權證",
    u"权证", u"權證操作", u"資訊", u"文", u"匯率", u"類股", u"指標", u"財務指標", u"财务指标", u"介紹", u"順勢", u"逆勢", u"逆势",
    u"有關賭盤", u"心理", u"券", u"維持率", u"警示股", u"太陽能", u"概念股", u"碳纖維", u"風力發電", u"價差", u"迷思", u"正",
    u"各種", u"利率", u"買賣", u"請問", u"问题", u"请问", u"競價", u"零股", u"零股交易", u"經濟指標", u"經濟", u"美國", u"大盤",
    u"有人知道", u"大盤買賣差", u"消息嗎", u"消息", u"知道", u"損益", u"族群", u"企業減資", u"減資", u"觀點", u"淨利", u"營業淨利",
    u"电影", u"電影", u"漲", u"跌", u"金融", u"盤後", u"成交量", u"買超", u"賣超", u"K", u"k", u"Ｋ", u"五百大", u"500大",
    u"美国500", u"美國500", u"史上", u"主權基金", u"伊斯蘭", u"陰宅", u"套房", u"選擇權", u"顧問", u"降息", u"升息", u"月線",
    u"外資分析師", u"套現", u"持股", u"領先指標", u"指數類", u"指数类", u"入門", u"新手入门", u"新手入門", u"一", u"倒閉", u"附圖",
    u"合理", u"不合理", u"什麼叫做", u"什麼是山", u"所得稅", u"證交稅", u"法人", u"證所稅", u"成交", u"三大法人", u"导言", u"導言",
    u"營建股", u"基本", u"技術", u"好朋友", u"投資", u"道瓊指數", u"道瓊", u"面试题", u"研究員面試", u"升降單位", u"台指", u"股價",
    u"讀書心得", u"關係", u"站穩", u"不破", u"生質", u"酒精", u"選舉行情", u"心态", u"黄金", u"黃金切割率", u"跳空见鬼",
    u"跳空見鬼", u"借錢", u"名詞", u"該做", u"上市股票", u"上櫃股票", u"產業", u"柏南克", u"一年", u"兩年", u"Short", u"Long",
    u"厚積而薄發", u"破曉", u"破曉雙星", u"筆撮合", u"勘誤", u"高鐵", u"高鐵高捷", u"查詢", u"網站", u"港股", u"日股", u"陸股",
    u"出貨文", u"出貨", u"相關", u"行业", u"顺", u"順勢逆勢", u"顺势", u"逆", u"反彈", u"洩", u"瀉", u"強制", u"融券", u"在对",
    u"做對", u"做对的事", u"股價查詢", u"融券回補", u"順勢操作", u"四大指數", u"股價指數", u"養套殺", u"養", u"套", u"資本",
    u"報酬", u"報酬率", u"資本報酬率", u"被男客", u"男客", u"因素", u"盈餘分配", u"盈餘", u"政策", u"股利分配", u"影響", u"生技",
    u"好書", u"好书", u"推荐", u"好书推荐", u"好書推薦", u"混沌操作法", u"解決", u"股東", u"太陽能產業", u"會漲", u"會跌", u"LED",
    u"半對數", u"費氏", u"紀念品", u"委託書", u"轉折", u"黑天鵝", u"黑天鵝效應", u"違約交割", u"營業員", u"飆股", u"轉錄", u"進步",
    u"進步了", u"有進步了", u"下落", u"下落二星", u"新聞", u"WiMAX", u"股票通", u"KD", u"推理", u"股票股利", u"除權息", u"為什麼"
    u"除權除息", u"信用戶", u"主力", u"券商", u"投顾", u"怎麼", u"功課", u"做功課", u"期待你的愛", u"開盤", u"台指期", u"美股",
    u"走勢", u"經濟成長率", u"下半年", u"上半年", u"Q1", u"Q2", u"Q3", u"Q4", u"过剩", u"過剩", u"哇", u"趨吉避凶", u"利用",
    u"全額交割股", u"竞价", u"電子玩具", u"电子玩具", u"逆價差", u"均買均賣", u"均買", u"均賣", u"有人知道這", u"背光模組", u"DRAM",
    u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"500", u"五百", u"漲金融", u"陰宅概念股", u"ETF", u"FED",
]

global_word_buf = {}
global_title_buf = {}


def get_stock_num(article_title):
    global global_word_buf, global_title_buf

    if article_title in global_title_buf:
        results = global_title_buf[article_title]
    else:
        results = GoogleSearchKeyword(article_title.encode("utf-8")).get_keywords()
        global_title_buf[article_title] = results

    count = 0
    for word, w_c in sorted(results.items(), key=operator.itemgetter(1)):
        print u"Cur word : '{}'".format(word)
        if " " in word or len(word) > 5 or word in NON_STOCK_NAMES or w_c < 3:
            continue
        if word != "...":
            print u"Using word : '{}'".format(word)
            if word in global_word_buf:
                num = global_word_buf[word]
            else:
                num = GoogleSearchKeyword(word.encode("utf-8")).get_stock_num()
                global_word_buf[word] = num

            if num:
                print str(num)
                return str(num)
            else:
                count += 1
                print u"Cannot find stock number from word '{}'".format(word)
        if count > 2:
            break
    return None


if __name__ == '__main__':
    # c = PttWebCrawler("Stock", True, start=1, end=300)
    # file_name = c.getFilename()

    file_name = "Stock-1-200.json"

    data = json.loads(codecs.open(file_name, "r", encoding='utf-8').read())
    results = {}
    additional = {}

    for article in data["articles"]:
        if "error" in article:  # Dirty data
            continue

        if article["article_title"] in [""]:
            continue
        elif u"水桶" in article["article_title"]:
            continue
        else:
            print article["article_title"]
            if article["article_title"].startswith("Re:"):
                article["article_title"] = article["article_title"][3:].strip()
            elif article["article_title"].startswith(u"[轉錄]Re:"):
                article["article_title"] = article["article_title"][7:].strip()
            if article["article_title"].startswith(u"[公告]"):
                continue

            article["article_title"] = article["article_title"].replace(u"紅茶店", "2498")

            try:
                i = article["article_title"].index("]") + 1
                article["article_title"] = article["article_title"][i:].strip()
            except:
                pass

            if len(article["article_title"]) == 0:
                continue

            print article["article_title"]

            m = re.findall('\d+', article["article_title"])
            if m:
                for num in set(m):
                    if len(num) == 4:
                        if u"{}年".format(num) in article["article_title"] or u"{}萬".format(num) in article["article_title"] or u"{}億".format(num) in article["article_title"]:
                            if len(set(m)) == 1:
                                num = get_stock_num(article["article_title"])

                                if num not in results:
                                    results[num] = 1
                                else:
                                    results[num] += 1
                                break
                            continue
                        a = str(num)
                        print str(a)
                        if a not in results:
                            results[a] = 1
                        else:
                            results[a] += 1
            else:
                num = get_stock_num(article["article_title"])
                if num not in results:
                    results[num] = 1
                else:
                    results[num] += 1

    sorted_results = sorted(results.items(), key=operator.itemgetter(1))
    for k, v in sorted_results:
        print "{} : {}".format(k, v)

