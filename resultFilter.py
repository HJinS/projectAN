import re
from collections import deque
from typing import Pattern

class ResultFilter:
    def __init__(self, resultQueue: deque, search_keyword: list()):
        self.result = resultQueue
        self.searchKeyword = search_keyword
        self.reInit()
        
    def reInit(self):
        self.expression = {
            "cpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Ii][Nn][Tt][Ee][Ll]|인텔|[Aa][Mm][Dd]).*([Pp][Rr][Oo][Cc][Ee][Ss][Ss][Oo][Rr]|프로세서|[Cc][Pp][Uu]).*",
            "gpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*(지포스|[Gg][Ee][Ff][Oo][Rr][Cc][Ee]|[Nn][Vv][Ii][Dd][Ii][Aa]|[Rr][Aa][Dd][Ee][Oo][Nn]).*([Gg][Pp][Uu]|[Gg][Rr][Aa][Pp][Hh][Ii][Cc][Ss]? [Cc][Aa][Rr][Dd][Ss]?|[Vv][Ii][Dd][Ee][Oo] [Cc][Aa][Rr][Dd][Ss]?|그래픽 카드)",
            "ram" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Dd][Dd][Rr][45]|[Rr][Aa][Mm]|메모리).*",
            "ssd" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Ss][Ss][Dd]|[Nn][Vv][Mm][Ee]|[Ss][Aa][Tt][Aa]|솔리드 스테이트 드라이브)",
            "cpu cooler" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Cc][Pp][Uu].*?([Cc][Oo][Oo][Ll][Ee][Rr]|쿨러)).*",
        }
        
    def filtering(self):
        f = open("result.txt", 'w', encoding="UTF-8")
        for result_item in self.result:
            id, image, name, price, keyword = result_item
            self.re = re.compile(r""+self.expression[keyword])
            match_result = self.re.findall(name)
            if len(match_result) == 0:
                print(name)
                print("부적합\n")
            else:
                f.write(id + " "  + image + " " + price + " " + keyword + "\n")
                f.write(name + "\n")
                ##print(match_result.group(1))
        f.close()
