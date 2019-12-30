import requests
from lxml import etree
import hashlib
import threading
import json, time, re, random
from copyheaders import headers_raw_to_dict
from config import *
from helper import Helper
from jiemi import Jiemi
import random, sys, os
# from fake_useragent import UserAgent



# ua = UserAgent()
h = Helper()
jm = Jiemi()



with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
with open('user-agent.txt', 'r', encoding='utf-8') as f:
    ua = f.read()


headers = {
    'accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1318',
    'content-type': 'application/json',
    'Cookie': '{0}'.format(cookie),
    'Host': 'live.kuaishou.com',
    'Origin': 'https://live.kuaishou.com',
    'Referer': 'https://live.kuaishou.com/profile/CoCo850427',
    'User-Agent': '{0}'.format(ua)

}



class Kuaishou(object):
    def __init__(self):
        pass

    # 主页信息
    def zhuye(self, uid):

        ajax_url = 'https://live.kuaishou.com/graphql'

        # 主播id去除空格
        uid = uid.strip()
        # print('主播id为：', uid)

        api_data = {"operationName": "publicFeedsQuery"
            , "variables": {"principalId": '{0}'.format(uid), "pcursor": "1.580067134625E12", "count": 120}
            ,"query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      photoId\n      poster\n      viewCount\n      likeCount\n      commentCount\n      timestamp\n    }\n  }\n}\n"}

        api = api_data
        response = requests.post(url=ajax_url, data=json.dumps(api), headers=headers)

        result = response.json()
        res_list = result['data']['publicFeeds']['list']
        # print(len(res_list))
        for res in res_list:
            self.f_time(res, url, id, uid)

    # 视频详细信息
    def f_time(self, res, url, id, uid):
        data = {}
        # 视频发布时间戳
        fabu_time = int(round(res['timestamp'] / 1000))
        # print(fabu_time)
        # 当前时间戳
        tt = time.time()
        # print(tt)
        # 当前时间
        now_time = h.create_time()
        # print(now_time)
        # 时间差
        sjcha = tt - fabu_time
        # print('时间差为：', sjcha)

        # 将时间戳转换成日期
        release_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fabu_time))

        if sjcha < 604800:
            if sjcha < 3600:
                fabu_time = str(int(sjcha / 60)) + '分钟前'
            elif 3600 <= sjcha < 86400:
                fabu_time = str(int(sjcha / 3600)) + '小时前'
            elif 86400 <= sjcha:
                fabu_time = str(int(sjcha / 86400) + 1) + '天前'

            data['uid'] = uid
            data['release_time'] = release_time
            data['create_time'] = now_time
            data['fabu_time'] = fabu_time
            self.lianjie(res, data, url)

        elif 604800 < sjcha < 691200:
            fabu_time = str(int(sjcha / 86400) + 1) + '天前'
            data['uid'] = uid
            data['release_time'] = release_time
            data['create_time'] = now_time
            data['fabu_time'] = fabu_time
            self.lianjie(res, data, url)

        else:
            pass
        # 返回数据并存储，修改任务状态为3
        # Helper.apiRequest(managerUrl['get_data_url'], data)

    # 图片视频链接
    def lianjie(self, res, data, url):
        # url = 'https://live.kuaishou.com/profile/Li18243000300'
        # 图片链接
        img_url = res['poster']
        # print(img_url)
        # 视频链接
        video = res['photoId']
        video_url = url.replace('profile', 'u') + '/' + video
        # print(video)
        # 获取变化的img_url的固定部分用于匹配唯一主键并加密成md5
        pattern = '.a.(.*?).jpg'
        str_img_url = re.findall(pattern, img_url)[0]
        # print('被加密的字段为：', str_img_url)
        # md5加密
        md = hashlib.md5()
        md.update(str_img_url.encode("utf8"))
        jiami = md.hexdigest()
        # print('md5加密字段为：', jiami)
        data['jiami'] = jiami
        data['img_url'] = img_url
        data['video_url'] = video_url
        n = 0
        self.count(res, data, n)

    # 播放量，点赞数，评论数
    def count(self, res, data, n):
        if n >= 5:
            print('未找到正确的解密参数==================================================================')
            return None
            # pass
        else:
            # 播放量
            play_count = res['viewCount']
            # print(play_count)
            # 点赞数
            like_count = res['likeCount']
            # print(like_count)
            # 评论数
            comment_count = res['commentCount']
            # print(comment_count)

            # 调用解密函数
            try:
                self.ks_jm(n, play_count, like_count, comment_count, data)
            except:
                n = n + 1
                self.count(res, data, n)

    def ks_jm(self, n, play_count, like_count, comment_count, data):
        jiemi_key_list = ['h57yip2q', '3jqwe90k', 'yuh4hy4p', 'qw2f1m1o', 'yx77i032']
        play_count = Jiemi.getCnString(play_count, jiemi_key_list[n])
        like_count = Jiemi.getCnString(like_count, jiemi_key_list[n])
        comment_count = Jiemi.getCnString(comment_count, jiemi_key_list[n])
        if 'w' in play_count:
            play_count = float(play_count[0:-1]) * 10000
        else:
            play_count = play_count
        # 点赞比
        if play_count == 0:
            dzrate = 0
        else:
            dzrate = round(((int(like_count) + int(comment_count)) / int(play_count)), 4)
            # print('点赞比：', dzrate)
        data['play_count'] = play_count
        data['like_count'] = like_count
        data['comment_count'] = comment_count
        data['dzrate'] = dzrate

        # 返回数据并存储，修改任务状态为3
        Helper.apiRequest(managerUrl['get_data_url'], data)
        # print(data)
        print('code:', data['code'], 'id:', data['id'], 'play_count:',
              data['play_count'], 'fabu_time:', data['fabu_time'], 'create_time:', data['create_time'])

        return data

    # 启动程序
    def main(self):
        # self.detail()

        while True:
            # 调用接口获取主播uid，uid可以存在数据空中，随用随取
            uid = ''  # 这是获取uid的方法，可以自己定义

            self.zhuye(uid)



if __name__ == '__main__':
    ks = Kuaishou()
    ks.main()










