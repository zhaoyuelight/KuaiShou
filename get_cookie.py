from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, json, os
import requests
from pprint import pprint


class Cookie(object):
    def __init__(self):
        pass

    def shuaxin(self):


        url = 'https://live.kuaishou.com/profile/3xbg5arpphry7mc'
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        browser = webdriver.Chrome(options=option)
        browser.get(url)

        while True:
            # time.sleep(3)
            if 'work-card-info-data' in browser.page_source:
                browser.refresh()
                time.sleep(1)
                print('可以获取页面')
                cookie_list = browser.get_cookies()
                cookie = {}
                for i in cookie_list:
                    cookie[i['name']] = i['value']

                # 退出selenium的浏览器窗 # print('====================cookie的值为：', cookie)
                browser.quit()
                # 返回cookie
                return cookie
                # self.detail(cookie)
            else:
                browser.refresh()
                time.sleep(2)
                print('获取cookie失败，网页重新刷新')

    def detail(self,cookie=None):

        headers = {
            'accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1318',
            'content-type': 'application/json',
            'Host': 'live.kuaishou.com',
            'Origin': 'https://live.kuaishou.com',
            'Referer': 'https://live.kuaishou.com/profile/CoCo850427',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

        }

        url1 = 'https://live.kuaishou.com/graphql'
        uid = 'CoCo850427'
        api_data = {"operationName": "publicFeedsQuery"
            , "variables": {"principalId": '{0}'.format(uid), "pcursor": "1.580067134625E12", "count": 120}
            ,"query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      photoId\n      poster\n      viewCount\n      likeCount\n      commentCount\n      timestamp\n    }\n  }\n}\n"}

        r = requests.post(url=url1,headers=headers,cookies=cookie,data=json.dumps(api_data))

        list = r.json()['data']['publicFeeds']['list']

        if r.status_code == 200 and len( list )>0:
            for item in list:
                pprint( item )
            return True
        else:
            print('账号被封禁,尝试递归调用')
            return False


    def main(self):
        # 刷新cookie
        cookies = self.shuaxin()
        while True:
            # 传入cookie
            res = self.detail( cookies )
            if not res:
                self.main()




if __name__ == '__main__':
    c = Cookie()
    c.main()










