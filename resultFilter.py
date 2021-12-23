import re
from collections import deque

class ResultFilter:
    def __init__(self, resultQueue: deque, search_keyword: str):
        self.result = resultQueue
        self.searchKeyword = search_keyword
        
    def reInit(self):
        self.re = {
            'cpu' : "r'(intel|amd).*?(processor|프로세서)(?!system|시스템|pc)\b'",
            'gpu' : "r'(nvdia|radeon).*?(gpu|graphics? cards?|video card|그래픽 카드)(?!system|시스템|pc)'",
            'ram' : "r'ddr4.*?(ram|메모리)(?!system|시스템|pc)'",
            'ssd' : "r'ssd.*?(nvme|sata)(?!system|시스템|pc)",
            'cooler' : "r'(liquid cooler|cpu cooler).*'",
        }
        