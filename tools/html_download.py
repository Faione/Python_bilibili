import requests


def download_page(url, para = None):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    if para:
        response = requests.get(url, params=para, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        return response.text
    else:
        return None

