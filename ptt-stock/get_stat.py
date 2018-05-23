# -*- coding: utf-8 -*-
from PttWebCrawler import PttWebCrawler
import codecs
import json
import re
import operator


if __name__ == '__main__':
    # c = PttWebCrawler("Stock", True, start=1, end=10)
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
            m = re.findall('\d+', article["article_title"])
            if m:
                for num in set(m):
                    if len(num) == 4:
                        a = str(num)
                        print str(a)
                        if a not in results:
                            results[a] = 1
                        else:
                            results[a] += 1

    sorted_results = sorted(results.items(), key=operator.itemgetter(1))
    for k, v in sorted_results:
        print "{} : {}".format(k, v)
