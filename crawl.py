from bs4 import BeautifulSoup
from util import Helper
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
        #     url = Helper.concat(url, 'm')
        # 마갤 구조는 비슷한데 갯수가 너무 많아서 (약 1만6천) 전체 탐색은 의미 없음. 날짜별 실북갤만 수집하는게 좋을 듯

        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.content, 'html.parser')
        title_atag_list = soup.select('div.section_cate > div.cate > ul > li > a')
        for atag in title_atag_list:
            try:
                print(atag.string, atag['href'].split('=')[1])
            except(Exception):
                pass
        

class Gall_inside(Crawl):
    def __init__(self):
        super().__init__()

    def find_yesterday_post(self, gall_code):
        payload = Helper().make_params(id=gall_code)
        resp = requests.get(self.gall_base_url, headers=self.headers, params=payload)
        soup = BeautifulSoup(resp.content, 'html.parser')
        post_list = soup.select('div.gall_listwrap > table.gall_list > tbody > tr.us-post') 
        # ub-content는 설문, 뉴스 포함
        # data-type기준 icon_notice=공지, icon_txt=짤 없는 글, icon_pic=짤 있는 글
        for post in post_list:
            if post['data-type'] == "icon_notice":
                pass
            else:
                # print(post.select('td.gall_num')[0].string, post.select('td.gall_date')[0]['title'])
                post_time_str = post.select('td.gall_date')[0]['title']
                if Helper().is_post_today(post_time_Str):
                    # WIP
                    pass
                elif Helper().is_post_yesterday(post_time_str):
                    # WIP
                    pass