import requests

#baseinfo
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
region_url = 'https://bbs.hupu.com/'
response = requests.request('GET',region_url,headers={"User-Agent":ua})

with response:
    print(response.url)
    print(response.status_code)
    print(response.request.headers)
    print(response.headers)
    print(response.text[:200])
    with open('movie.html','w',encoding='utf-8') as f:
        f.write(response.text)
