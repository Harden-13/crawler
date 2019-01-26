import requests

#baseinfo
#requests默认使用session对象，是为了在多次和服务器端交互中保留绘画的信息，例如cookies
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
region_url = ['https://bbs.hupu.com/','https://nba.hupu.com/']
session = requests.Session()

with session:
    for url in region_url:
        response = session.get(url,headers={'User-Agent':ua})
        with response:
            print(type(response))
            print(response.url)
            print(response.status_code)
            print(response.request.headers)
            print(response.cookies)

