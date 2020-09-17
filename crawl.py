from bs4 import BeautifulSoup
import requests

class Crawl:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"

    def collect(self):
        # 패러미터 정리 등등
        param = {'user_agent': self.user_agent}
        return param
        

class Gall_outside(Crawl):
    def __init__(self):
        super().__init__()

    def collect(self):
        #cate_bind > cate_box > section_cate > cate_tit(=제목), list_num(=갤 개수)
        super().collect()
        

class Gall_inside(Crawl):
    def __init__(self):
        super().__init__()
        self.gall_base_url = "https://gall.dcinside.com/board/lists/?id="
        self.mgall_base_url = "https://gall.dcinside.com/mgallery/board/lists/?id="

    def collect(self):
        super().collect()