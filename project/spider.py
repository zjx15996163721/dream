import requests
from lxml import etree
import time
import sys
from lib.log import LogHandler
from project.parse import Parse
log = LogHandler(__name__)


class Spider:

    def __init__(self, cookie):
        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'ehire.51job.com',
            'Referer': 'https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Cookie': cookie
        }
        self.cookie = cookie
        self.start_url = 'https://ehire.51job.com/InboxResume/InboxRecentEngine.aspx?Style=1'
        # 计数器
        self.count = 0

    def start(self):
        r = requests.get(url=self.start_url, headers=self.headers)
        tree = etree.HTML(r.text)
        # 获取第二页的关键参数VIEWSTART
        VIEWSTART = tree.xpath("//input[@id='__VIEWSTATE']")[0].xpath("@value")[0]
        # 获取最大页码
        max_page = tree.xpath("//a[@id='pagerBottomNew_btnNum_ma']/text()")[0]
        # 获取第一页简历链接
        user_links = tree.xpath("//input[@id='chkBox']")
        for link in user_links:
            user_id = link.xpath('@value1')[0]
            # todo 更加ID 去重
            url = 'https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx?hidSeqID=' + user_id + '&hidFolder=EMP&pageCode=24'
            print(url)
            # todo 请求解析
            p = Parse(self.cookie)
            p.start('https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx', user_id)
            time.sleep(1)
        self.count += 1
        self.small_six_page_params(VIEWSTART, 2, int(max_page))

    # 页码小于6的请求参数
    def small_six_page_params(self, VIEWSTART, page, max_page):
        data = {
            '__EVENTTARGET': 'pagerBottomNew$btnNum' + str(page),
            '__VIEWSTATE': VIEWSTART,
            'pagerTopNew$ctl06': '50',
            'hid_posttime': '180',
        }
        self.request_next_page(data, page, max_page)

    # 页码大于6的请求参数
    def large_six_page_params(self, VIEWSTART, page, max_page):
        data = {
            '__EVENTTARGET': 'pagerBottomNew$btnNum4',
            '__VIEWSTATE': VIEWSTART,
            'pagerTopNew$ctl06': '50',
            'hid_posttime': '180',
        }
        self.request_next_page(data, page, max_page)

    def request_next_page(self, data, page, max_page):
        r = requests.post(url=self.start_url, headers=self.headers, data=data)
        tree = etree.HTML(r.text)
        # 获取下一页的关键参数VIEWSTART
        VIEWSTART = tree.xpath("//input[@id='__VIEWSTATE']")[0].xpath("@value")[0]
        # 获取简历链接
        user_links = tree.xpath("//input[@id='chkBox']")
        for link in user_links:
            user_id = link.xpath('@value1')[0]
            # todo 根据id 去重
            url = 'https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx?hidSeqID=' + user_id + '&hidFolder=EMP&pageCode=24'
            print(url)
            # todo 请求解析
            p = Parse(self.cookie)
            p.start('https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx', user_id)
            time.sleep(1)
        print(VIEWSTART)
        # 延迟请求，防止被封IP
        time.sleep(5)
        self.count += 1
        if self.count > max_page:
            sys.exit()
        else:
            if page >= 5:
                # 页面大于5之后的所有页面 __EVENTTARGET均为pagerBottomNew$btnNum4
                self.large_six_page_params(VIEWSTART, page, max_page)
            else:
                page += 1
                self.small_six_page_params(VIEWSTART, page, max_page)


if __name__ == '__main__':
    cookie = 'guid=6cfadb91bfb463e76a875d9012ee90ef; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; ps=needv%3D0; _ujz=MTUzNjE4NTk1MA%3D%3D; 51job=cuid%3D153618595%26%7C%26cusername%3Dphone_15996163721_201903126789%26%7C%26cpassword%3D%26%7C%26cname%3D%25D5%25C5%25BD%25F0%25D0%25A4%26%7C%26cemail%3D1735429225%2540qq.com%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0BXdfJgAFuI.%26%7C%26cconfirmkey%3D176PQZKsaFYdM%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D17IYfSY3xlHpg%26%7C%26to%3Dfed7de1ed92e5b4ccd97ebf566f02ad35d7a441d%26%7C%26; search=jobarea%7E%60020000%2C070300%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60020000%2C070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C9%CF%BA%A3%B7%E1%B2%DD%CE%C4%BB%AF%B4%AB%B2%A5%D3%D0%CF%DE%B9%AB%CB%BE%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60020000%2C070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60020000%2C070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA02%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60020000%2C070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60020000%2C070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21; adv=adsnew%3D0%26%7C%26adsnum%3D2004282%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fsp0.baidu.com%252F9q9JcDHa2gU2pMbgoY3K%252Fadrc.php%253Ft%253D06KL00c00fDewkY0KKG-00uiAsjjuLkI000007jzr-C00000LXA5xZ.THYdnyGEm6K85yF9pywd0ZnquHwBPW0zm10snj0dmvnkPsKd5RRdnbnsn1Fjrj6vrHb3njFAwj-afHN7wH6sP1PDnYRd0ADqI1YhUyPGujY1nWT4njbsPHTdFMKzUvwGujYkP6K-5y9YIZK1rBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqnW0sPjc3nBu9pM0qmR9inAPcHHunXH-YmHPwIR4RwM7Bnb-dyHc4IDs1Rh4nnY4_m-n4IvN_rZ-PwDRYHAdCnAFgIzqpUbGvm-fkpN-gUAVbyDcvFh_qn1u-njRYmyDsPjR4m1F-uAfdmWfLuWRLmvcvnHKbrjc0mLFW5HfLn1bd%2526tpl%253Dtpl_11534_19968_16032%2526l%253D1513812560%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E5%25252587%25252586%252525E5%252525A4%252525B4%252525E9%25252583%252525A8-%252525E6%252525A0%25252587%252525E9%252525A2%25252598-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E3%25252580%25252590%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A751Job%252525E3%25252580%25252591-%25252520%252525E5%252525A5%252525BD%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%2521%252526xp%25253Did%2528%25252522m3279090575_canvas%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D220%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D51job%2526oq%253D51job%2526rqlang%253Dcn; EhireGuid=c0ac2273169c47e3ab7dffab34678ba6; LangType=Lang=&Flag=1; RememberLoginInfo=member_name=42C0E5A4273247A0CA6AD9118CC10153&user_name=42C0E5A4273247A0BE39E05CE3F038B97F346A4FD26D49881290FBC4487FA1C3; ASP.NET_SessionId=023dciai3c5nbdcybq53aym1; AccessKey=5ff3aa3dae5d4b5; HRUSERINFO=CtmID=4371481&DBID=1&MType=02&HRUID=5809286&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=%e4%b8%8a%e6%b5%b7%e4%b8%b0%e8%8d%89%e6%96%87%e5%8c%96%e4%bc%a0%e6%92%ad%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&IsStandard=0&LoginTime=09%2f21%2f2019+14%3a26%3a26&ExpireTime=09%2f21%2f2019+14%3a36%3a26&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=fc01943ccde97937&source=0'
    s = Spider(cookie)
    s.start()
