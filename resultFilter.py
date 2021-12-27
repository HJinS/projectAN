import re
from collections import deque
from typing import Pattern

class ResultFilter:
    def __init__(self, resultQueue: deque):
        self.result = resultQueue
        self.beforeKeyword = None
        self.reInit()
        
    def reInit(self):
        self.expression = {
            "intel cpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|[Aa][Mm][Dd]).*([Ii][Nn][Tt][Ee][Ll]|인텔).*([Pp][Rr][Oo][Cc][Ee][Ss][Ss][Oo][Rr]|프로세서|[Cc][Pp][Uu]).*",
            "amd cpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|인텔|[Ii][Nn][Tt][Ee][Ll]).*([Aa][Mm][Dd]).*([Pp][Rr][Oo][Cc][Ee][Ss][Ss][Oo][Rr]|프로세서|[Cc][Pp][Uu]).*",
            "radeon gpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|지포스|[Nn][Vv][Ii][Dd][Ii][Aa]).*(라데온|[Rr][Aa][Dd][Ee][Oo][Nn]|[Rr][Xx]).*([Gg][Pp][Uu]|[Gg][Rr][Aa][Pp][Hh][Ii][Cc][Ss]?\s?[Cc][Aa][Rr][Dd][Ss]?|[Vv][Ii][Dd][Ee][Oo]\s?s[Cc][Aa][Rr][Dd][Ss]?|그래픽 카드)?.*?",
            "nvidia gpu" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|라데온|[Rr][Aa][Dd][Ee][Oo][Nn]).*(지포스|[Gg][Ee][Ff][Oo][Rr][Cc][Ee]|[Nn][Vv][Ii][Dd][Ii][Aa]|[RrGg][Tt][Xx]).*([Gg][Pp][Uu]|[Gg][Rr][Aa][Pp][Hh][Ii][Cc][Ss]?\s?[Cc][Aa][Rr][Dd][Ss]?|[Vv][Ii][Dd][Ee][Oo]\s?[Cc][Aa][Rr][Dd][Ss]?|그래픽 카드)?.*?",
            "ddr4 ram" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Dd][Dd][Rr][4]).*([Rr][Aa][Mm]|메모리)?.*",
            "ddr5 ram" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]).*([Dd][Dd][Rr][5]).*([Rr][Aa][Mm]|메모리)?.*",
            "nvme ssd" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|[Ss][Aa][Tt][Aa]).*([Nn][Vv][Mm][Ee]).*([Ss][Ss][Dd]|솔리드 스테이트 드라이브).*\2?",
            "sata ssd" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|[Nn][Vv][Mm][Ee]).*([Ss][Aa][Tt][Aa]).*([Ss][Ss][Dd]|솔리드 스테이트 드라이브).*\2?",
            "liquid cpu cooler" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|[Ll][Ii][Qq][Uu][Ii][Dd]|액체).*([Cc][Pp][Uu].*?([Cc][Oo][Oo][Ll][Ee][Rr]|쿨러)).*",
            "air cpu cooler" : "(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc]|[Aa][Ii][Rr]|에어).*([Cc][Pp][Uu].*?([Cc][Oo][Oo][Ll][Ee][Rr]|쿨러)).*",
        }
        
    def filtering(self):
        f = open("result.txt", 'w', encoding="UTF-8")
        for result_item in self.result:
            id, image, name, price, keyword = result_item
            if self.beforeKeyword == None or self.beforeKeyword != keyword:
                print("keyword = ", keyword)
                self.re = re.compile(r""+self.expression[keyword])
            match_result = self.re.findall(name)
            if len(match_result) == 0:
                print(match_result)
                print(name)
                print("부적합\n")
            else:
                f.write(id + " "  + image + " " + price + " " + keyword + "\n")
                f.write(name + "\n")
                ##print(match_result.group(1))
            self.beforeKeyword = keyword
        f.close()
