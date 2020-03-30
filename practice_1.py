import tools
from bs4 import BeautifulSoup

url = "https://www.bilibili.com/video/"
av_num = 99999999

# get bv_num
d = tools.decoder.Decoder()
bv_num = d.get_bvnum(av_num)

# download_page
url_bv = url + bv_num
html_text = tools.html_download.download_page(url_bv)

# get video title
soup = BeautifulSoup(html_text, 'html.parser')
title = soup.body.h1.text
print(title)
