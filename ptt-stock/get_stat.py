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


def get_stock_num(article_title):
    results = GoogleSearchKeyword(article_title.encode("utf-8")).get_keywords()
    count = 0
    for word, _ in sorted(results.items(), key=operator.itemgetter(1)):
        if " " in word:
            continue
        if word != "...":
            print u"Using word : '{}'".format(word)
            num = GoogleSearchKeyword(word.encode("utf-8")).get_stock_num()
            if num:
                return str(num)
                break
            else:
                count += 1
                print u"Cannot find stock number from word '{}'".format(word)
        if count > 3:
            break



if __name__ == '__main__':
    c = PttWebCrawler("Stock", True, start=1, end=300)
    file_name = c.getFilename()

    # file_name = "Stock-1-200.json"

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
                        if u"{}年" in article["article_title"]:
                            if len(set(m)) == 1:
                                num = get_stock_num(article["article_title"])

                                if num not in results:
                                    results[num] = 1
                                else:
                                    results[num] += 1
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

