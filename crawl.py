from bs4 import BeautifulSoup
from util import String_helper
import requests

class Crawl:
    def __init__(self):
        self.gall_base_url = "https://gall.dcinside.com/board/lists/"
        self.mgall_base_url = "https://gall.dcinside.com/mgallery/board/lists/"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent, 'Accpet': 'text/*', 'Accept-Charset': 'utf-8'}
        

class Gall_lists(Crawl):
    def __init__(self):
        super().__init__()

    def collect(self, isMinor):
        #cate_bind > cate_box > section_cate > cate_tit(=제목), list_num(=갤 개수)
        url = "https://gall.dcinside.com/"
        # if isMinor:
        #     url = String_helper.concat(url, 'm')
        # 마갤 구조는 비슷한데 갯수가 너무 많아서 (약 1만6천) 전체 탐색은 의미 없음. 날짜별 실북갤만 수집하는게 좋을 듯

        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.content, 'html.parser')
        title_atag_list = soup.select('div.section_cate > div.cate > ul > li > a')
        for single_atag in title_atag_list:
            try:
                print(single_atag.string, single_atag['href'].split('=')[1])
            except(Exception):
                pass
        

class Gall_inside(Crawl):
    def __init__(self):
        super().__init__()

    def find_yesterday_post(self, gall_code):
        gall_url = String_helper.concat(self.gall_base_url, gall_code)
        resp = requests.get(self.gall_base_url)