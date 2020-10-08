from bs4 import BeautifulSoup
from util import Helper
import requests

class Crawl:
    def __init__(self):
        self.gall_base_url = "https://gall.dcinside.com/board/lists/"
        self.mgall_base_url = "https://gall.dcinside.com/mgallery/board/lists/"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        self.headers = {"User-Agent": self.user_agent, "Accpet": "text/*", "Accept-Charset": "utf-8"}
        

class Gall_crawler(Crawl):
    def __init__(self):
        super().__init__()

    def collect(self, isMinor):
        # cate_bind > cate_box > section_cate > cate_tit(=제목), list_num(=갤 개수)
        url = "https://gall.dcinside.com/"
        # 마갤 구조는 비슷한데 갯수가 너무 많아서 (약 1만6천) 전체 탐색은 의미 없음. 

        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        title_atag_list = soup.select("div.section_cate > div.cate > ul > li > a")
        for atag in title_atag_list:
            try:
                print(atag.string, atag["href"].split('=')[1])
            except(Exception):
                pass

    def collect_page_post(self, gall_code, page_num):
        """ 
        gall_code: 서치할 갤러리의 코드
        page_num: 서치할 페이지 번호

        return: (bs4.BeautifulSoup) 
        """
        payload = Helper().make_params(id=gall_code, page=page_num)
        resp = requests.get(self.gall_base_url, headers=self.headers, params=payload)
        return BeautifulSoup(resp.content, 'html.parser')

    # TODO: recursion limit
    def find_yesterday_post_range(self, gall_code, page_num, first_post_num, last_post_num):
        """
        gall_code: 서치할 갤러리의 코드
        page_num: 서치할 페이지 번호(그 페이지 안에서 서치 못 하면 다음 페이지로 넘겨서 재귀)
        first_post_num: 어제의 첫 포스트 번호
        last_post_num: 어제의 마지막 포스트 번호
        
        return: (first_post_num, last_post_num)
        """

        soup = self.collect_page_post(gall_code, page_num)
        post_list = soup.select("div.gall_listwrap > table.gall_list > tbody > tr.us-post") 
        # ub-content는 설문, 뉴스 포함
        # data-type기준 icon_notice=공지, icon_txt=짤 없는 글, icon_pic=짤 있는 글
        last_post_strtime = post_list[len(post_list) - 1].select("td.gall_date")[0]["title"]
        is_last_post_recursion = False
        is_first_post_recursion = False
        
        if ( last_post_num == -1
                and not Helper().is_post_yesterday(last_post_strtime) ):
            # pass to next recursion
            pass
        elif ( last_post_num == -1
                and Helper().is_post_yesterday(last_post_strtime) ):
            # find post number of last post of yesterday
            is_last_post_recursion = True
        elif ( (not last_post_num == -1 and first_post_num == -1)
                and not Helper().is_post_yesterday(last_post_strtime) ):
            # find post number of first post of yesterday
            is_first_post_recursion = True

        is_first_after_notice = True

        if is_last_post_recursion or is_first_post_recursion:
            for post in post_list:
                if ( post["data-type"] == "icon_notice"
                        or post.select("td.gall_num")[0].string == "설문" ):
                    pass
                else:
                    # print(post.select('td.gall_num')[0].string, post.select('td.gall_date')[0]['title'])
                    post_time_str = post.select("td.gall_date")[0]["title"]
                    if is_first_after_notice:
                        first_num_of_loop = int(post.select("td.gall_num")[0].string)
                    if Helper().is_post_yesterday(post_time_str):
                        if is_first_post_recursion:
                            pass
                        elif last_post_num == -1:
                            last_post_num = int(post.select("td.gall_num")[0].string)
                    elif is_first_post_recursion:
                        if first_post_num == -1:
                            first_post_num = int(post.select("td.gall_num")[0].string)
                        else:
                            break
            if is_first_post_recursion and first_post_num == -1:
                first_post_num = first_num_of_loop - 1

            if last_post_num == -1 or first_post_num == -1:
                (first_post_num, last_post_num) = self.find_yesterday_post_range(
                        gall_code, page_num+1, first_post_num, last_post_num)
            else:
                return (first_post_num, last_post_num)
        else:
            (first_post_num, last_post_num) = self.find_yesterday_post_range(
                        gall_code, page_num+1, first_post_num, last_post_num)
        
        return (first_post_num, last_post_num)