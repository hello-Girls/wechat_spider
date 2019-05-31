#coding=utf-8
import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from googletrans import Translator
import asyncio
from pyppeteer import launch
import requests
import json
from bs4 import BeautifulSoup
import execjs #必须，需要先用pip 安装，用来执行js脚本
import pymysql

keyword='穿衣风格'

proxy_pool_url='http://127.0.0.1:5000/get'

proxy=None

max_count=5

page_start=45
page_end=101

cookies='SUV=00879A3A1B26FA495CC571EF9BF2F712; SUID=4C9722902320940A000000005CE3D8B5; ABTEST=1|1558942350|v1; IPLOC=CN4403; pgv_pvi=6971604992; weixinIndexVisited=1; ppinf=5|1559095971|1560305571|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0Nzp3byVFNSU5NiU5QyVFNiVBQyVBMiVFNyU4NSU4RSVFOCU5QiU4QiVFNSU4RCVCN3xjcnQ6MTA6MTU1OTA5NTk3MXxyZWZuaWNrOjQ3OndvJUU1JTk2JTlDJUU2JUFDJUEyJUU3JTg1JThFJUU4JTlCJThCJUU1JThEJUI3fHVzZXJpZDo0NDpvOXQybHVHVG53LUVpd3Y1WGpyNkxjU250MEV3QHdlaXhpbi5zb2h1LmNvbXw; pprdig=iMq4vTYwhC8wCNyaHUKhKz5h5Yakp_HzbI_SLatwS-cTQKoKcqEue6EfsZjs1E79upvSH9XHiGBfWDJQfkr44_8AWtm4qjbiZZ0YMES7B1Lfo-8Hvs82GH-1mThzWn0ZXIzYqJC2LNeRmV1J2moL5lQQgZhpkdn-tjp2Bxy24bw; sgid=25-40905565-AVzt6qPMyw6ecbQpMITVRAA; JSESSIONID=aaaxNIxnPqtYB5bHepgRw; pgv_si=s9350193152; PHPSESSID=3nq7lbj4u8l5hqaum7uhlblov4; ssuid=1370381117; clientId=16CDDC060F616FEF2D92D16B0EA96E9E; ad=rlllllllll2tDaBDlllllV8ZHXZlllllphbf$kllll9lllll4Zlll5@@@@@@@@@@; CXID=9F9CC1EFD9570D6C504849E947D87CD5; sg_uuid=9481418272; sw_uuid=7847128577; sct=42; ld=gkllllllll2tfi3VlllllV8ZiJ1lllllphbfHklllRylllll4Zlll5@@@@@@@@@@; LSTMV=391%2C302; LCLKINT=9263; ppmdig=15592933370000004511712bad64095d73eea7745ded1e30; SNUID=88DB043A2227AB0A67DDA86C22EEACB8; seccodeRight=success; successCount=1|Fri, 31 May 2019 09:07:28 GMT; refresh=1'
class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 

        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)
def yourgoogleisgood(content):
    '''实现谷歌的翻译'''
    content = content
   # 一个参照
   # if len(content) > 2200:
   #      pass

   # else:
    js = Py4Js()
    tk = js.getTk(content)

    if len(content) > 4891:
            print("翻译的长度超过限制！！！")
            return

    param = {'tk': tk, 'q': content}
    #q不能太大造成请求头过大
    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=zh-CN 
                &tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
                &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

    # 返回的结果为Json，解析为一个嵌套列表
    try:
     trans = result.json()[0]
     ret = ''
     for i in range(len(trans)):
            line = trans[i][0]
            if line != None:
                ret += trans[i][0]
    except:
     ret=None

    return ret

base_url='https://weixin.sogou.com/weixin?'

headers={
      'Cookie': cookies,
      'Host':'weixin.sogou.com',
      'Referer': 'https://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3d%E5%87%8F%E8%82%A5%26type%3d2%26page%3d1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}



def get_proxy():
    try:
        responce=requests.get(proxy_pool_url)
        if responce.status_code==200:
            return responce.text
        return None
    except ConnectionError:
        return None

def get_html(url,count=1):
    print('Crawling',url)
    print('Trying Count',count)
    global proxy
    if count>=max_count:
        print('请求次数太多')
        return None

    try:
        if proxy:
               proxies={
              'http':'http://'+proxy
          }
               response = requests.get(url, allow_redirects=False,
                                       headers=headers,proxies=proxies)  # allow_redirects=False防止页面跳转，出现请求失败返回302

        else:
          response = requests.get(url, allow_redirects=False,
                                    headers=headers)  # allow_redirects=False防止页面跳转，出现请求失败返回302
        if response.status_code == 200:
            #print(response.text)
            return response.text
        if response.status_code == 302:
            print('302')
            proxy=get_proxy()
            if proxy:
                print('使用代理',proxy)
                return get_html(url)
            else:
                print('获取代理失败')
                return get_html(url)
    except ConnectionError as e:
        print('gethtml错误',e.args)
        count+=1
        proxy=get_proxy()
        return get_html(url,count)

def get_index(keyword,page):
    data={
        'query':keyword,#搜索的关键字
        'type':2,       #这里的2表示搜索文章1表示搜索公众号
        'page':page
    }
    queries=urlencode(data)
    url=base_url+queries
    html=get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('data-share')

def save_to_mysql(data):
    if data:
     con = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd="jiangfuhua321"

                               )
     cursor = con.cursor(pymysql.cursors.DictCursor)
     con.select_db("wechat")
     try:
        sql = """

                    create table style(
                           Id INT NOT NULL AUTO_INCREMENT primary key,
                           Text text
                           
                           )
"""

        cursor.execute(sql)
     except:
        #print("已经存在数据库")
        pass
     cursor.execute("insert into style(Id,Text) values (%s,%s)",(0,data))
     con.commit()


def main():
    for page in range(page_start,page_end):
        html = get_index(keyword,page)
        if html:
            article_urls=parse_index(html)
            for article_url in article_urls:
                print(article_url)
                article_html=requests.get(article_url)
                #print(article_html.text)
                doc=pq(article_html.text)
                content=doc('.rich_media_content ').text()
                #print(content)
                content=content.replace("\n","")
                print(content)
                english=yourgoogleisgood(content)
                print(english)
                try:
                 save_to_mysql(english)
                except:
                 pass


if __name__ == '__main__':
    main()


