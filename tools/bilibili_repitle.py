import re
import json
import time
import decoder
import html_download
import mysql_connect
from bs4 import BeautifulSoup


class bilibili_reptile(object):
    err = ["NO HTML", "HTML EMPTY", "DATA ERR", "UNVISIABLE", "UNREVIEWABLE"]
    list_stat = ["title", "date", "coin", "like", "favorite", "view", "owner_id", "owner_name"]

    url_html = "https://www.bilibili.com/video/"  # BV
    url_json_comments = "https://api.bilibili.com/x/v2/reply?" \
                        "jsonp=jsonp&pn={}&type=1&oid={}&sort=2&_=1586400206136"  # page = int, oid = AV
    url_json_tag = "https://api.bilibili.com/x/tag/archive/tags?aid={}&jsonp=jsonp&_=1586415101505"  # aid = AV
    url_json_stat = "https://api.bilibili.com/x/web-interface/view?bvid="  # BV

    def __init__(self):
        self.bv = None
        self.av = None
        self.tag = None
        self.err_tag = []
        self.stat_dict = {}
        self.activity_dict = {}
        self.decoder = decoder.Decoder()
        self.sum_table_3 = 0
        self.sum_table_4 = 0

    def set_bv(self, av):
        bv = self.decoder.get_bvnum(av)
        self.av = av
        self.bv = bv

    def get_origin_url(self):
        htmls = [self.url_html + self.bv, self.url_json_stat + self.bv,
                 self.url_json_tag.format(self.av), self.url_json_comments.format(1, self.av)]
        return htmls

    def html_err(self, html):
        if html is None:
            self.err_tag.append(self.err[0])
            return True

        if "视频去哪了呢" in html:
            self.err_tag.append(self.err[1])
            return True
        else:
            return False

    def data_err(self, html):
        if html is None:
            self.err_tag.append(self.err[0])
            return True
        if "评论区已关闭" in html:
            self.err_tag.append(self.err[3])
            return True
        else:
            return False

    def get_stat(self):
        html = html_download.download_page(self.url_json_stat + self.bv)

        data_json = json.loads(html)
        list_stat_values = []
        dict_data = data_json.get('data')

        dict_stat = dict_data.get("stat")
        dict_owner = dict_data.get("owner")

        time_array = time.localtime(dict_data.get("pubdate"))
        normal_time = time.strftime("%Y-%m-%d", time_array)
        # list_stat_values.append(dict_data.get("pubdate"))  # using data time instead of second time
        list_stat_values.append(dict_data.get("title"))
        list_stat_values.append(normal_time)
        list_stat_values.append(dict_stat.get("coin"))
        list_stat_values.append(dict_stat.get("like"))
        list_stat_values.append(dict_stat.get("favorite"))
        list_stat_values.append(dict_stat.get("view"))
        list_stat_values.append(dict_owner.get("mid"))
        list_stat_values.append(dict_owner.get("name"))

        self.stat_dict = dict(zip(self.list_stat, list_stat_values))

    def get_info(self):
        html = html_download.download_page(self.get_origin_url()[0])
        if self.html_err(html):
            return

        soup = BeautifulSoup(html, 'html.parser')
        class_pattern = re.compile("info open")
        divs = soup.find_all("div", {'class': class_pattern})
        info_div = divs[0]

        return info_div.text

    def get_comments(self):
        html = html_download.download_page(self.url_json_comments.format(1, self.av))
        if self.data_err(html):
            return

        data_json = json.loads(html)
        # if there is data
        if data_json['data'] is None:
            self.err_tag.append(self.err[2])
            return
        # if there are comments
        if data_json['data']['page']['count'] == 0:
            self.err_tag.append(self.err[2])
            return
        total_page = data_json['data']['page']['count'] // data_json['data']['page']['size'] + 1

        comments_message = []
        for page in range(1, total_page + 1):
            comments_html = html_download.download_page(self.url_json_comments.format(page, self.av))
            data_json = json.loads(comments_html)
            if data_json['data']['replies'] is None:
                break
            for i in data_json['data']['replies']:
                # 主评
                if i is not None:
                    comments_message.append(i['content']['message'])
                    # 追评
                    if i['replies'] is not None:
                        for j in i['replies']:
                            comments_message.append(j['content']['message'])
        return comments_message

    def set_activity_dict(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            activities = file.read().split("\n\n")
            activity_names = []
            activity_time = []

            for activity in activities:
                activity = activity.split("\n")
                data = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", activity[1])

                activity_names.append(activity[0])
                activity_time.append(data)

        self.activity_dict = dict(zip(activity_names, activity_time))

    def get_activity_tag(self):
        html = html_download.download_page(self.url_json_tag.format(self.av))
        path = "activities.txt"
        if self.data_err(html):
            return

        self.set_activity_dict(path)
        html_json = json.loads(html)
        tag_list = html_json['data']

        if tag_list is None:
            self.err_tag.append(self.err[2])
            return
        else:
            for i in tag_list:
                if i['tag_name'] in self.activity_dict.keys():
                    self.tag = i['tag_name']
                else:
                    self.tag = "No Tag"
            return self.tag

    def to_table(self):
        self.err_tag = []
        # if info is None, means that the html is useless
        info = self.get_info()
        if info is None:
            return

        self.get_stat()
        self.get_activity_tag()
        comments = self.get_comments()

        if len(self.err_tag) == 0:
            for i in comments:
                try:
                    mysql_connect.insert_to_b3_qgfx(self.stat_dict['date'], self.bv, self.stat_dict['title'], info, i)
                except Exception as e:
                    print(e)
                self.sum_table_3 += 1
            if self.tag != "No Tag":
                try:
                    mysql_connect.insert_to_hd_cyfx(self.tag, self.stat_dict['owner_id'], self.stat_dict['coin'],
                                                    self.stat_dict['like'], self.stat_dict['favorite'],
                                                    self.stat_dict['view'])
                except Exception as e:
                    print(e)
                self.sum_table_4 += 1
            return "SUCCESSFUL!"
        else:
            return self.err_tag
