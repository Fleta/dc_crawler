from bs4 import BeautifulSoup
import requests

class Crawl:
    def __init__(self):
        self.gall_base_url = "https://gall.dcinside.com/board/lists/"
        self.mgall_base_url = "https://gall.dcinside.com/mgallery/board/lists/"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"

    def make_header(self): 
        # 패러미터 정리 등등
        headers = {'User-Agent': self.user_agent, 'Accpet': 'text/*', 'Accept-Charset': 'utf-8'}
        return headers
        

class Gall_lists(Crawl):
    def __init__(self):
        super().__init__()

    def collect(self, isMinor):
        #cate_bind > cate_box > section_cate > cate_tit(=제목), list_num(=갤 개수)
        headers = super().make_header()
        url = "https://gall.dcinside.com/"
        # if isMinor:
        #     url = url.split()
        #     url.append('m')
        #     url = ''.join(url)
        # 마갤 구조는 비슷한데 갯수가 너무 많아서 (약 1만6천) 전체 탐색은 의미 없음. 날짜별 실북갤만 수집하는게 좋을 듯

        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, 'html.parser')
        title_atag_list = soup.select('div.section_cate > div.cate > ul > li > a')
        for single_atag in title_atag_list:
            print(single_atag.string)
        

class Gall_inside(Crawl):
    def __init__(self):
        super().__init__()

    def collect(self):
        super().make_header()