import re
from collections import deque

class ResultFilter:
    def __init__(self, resultQueue: deque, search_keyword: list()):
        self.result = resultQueue
        self.searchKeyword = search_keyword
        self.reInit()
        
    def reInit(self):
        self.expression = {
            'cpu' : "r'[Ii][Nn][Tt][Ee][Ll]|[Aa][Mm][Dd]|인텔.*?[Pp][Rr][Oo][Cc][Ee][Ss][Ss][Oo][Rr]|프로세서.*?(?![Ss][Yy][Ss][Tt][Ee][Mm]|시스템|[Pp][Cc])'",
            'gpu' : "r'(nvdia|radeon).*?(gpu|graphics? cards?|video card|그래픽 카드)(?!system|시스템|pc)'",
            'ram' : "r'ddr4.*?(ram|메모리)(?!system|시스템|pc)'",
            'ssd' : "r'ssd.*?(nvme|sata)(?!system|시스템|pc)",
            'cpu cooler' : "r'(liquid cooler|cpu cooler).*'",
        }
        
    def filtering(self):
        f = open("result.txt", 'w', encoding="UTF-8")
        for result_item in self.result:
            id, image, name, price, keyword = result_item
            self.re = re.compile(self.expression[keyword])
            match_result = self.re.findall(name)
            if len(match_result) == 0:
                print(name)
                print("부적합\n")
            else:
                f.write(id + " "  + image + " " + price + " " + keyword + "\n")
                f.write(name + "\n")
                ##print(match_result.group(1))
        f.close()
