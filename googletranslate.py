#coding: utf-8
import requests
import json
from bs4 import BeautifulSoup
import execjs #必须，需要先用pip 安装，用来执行js脚本
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
  def getTk(self,text):
      return self.ctx.call("TL",text)
def buildUrl(text,tk):
  baseUrl='https://translate.google.cn/translate_a/single'
  baseUrl+='?client=t&'
  #baseUrl+='s1=auto&'
  baseUrl += 'sl=zh-CN&'  #源语言
  #baseUrl+='t1=zh-CN&'
  baseUrl += 'tl=en&'     #目标语言
  baseUrl+='hl=zh-CN&'

  baseUrl+='dt=at&'
  baseUrl+='dt=bd&'
  baseUrl+='dt=ex&'
  baseUrl+='dt=ld&'
  baseUrl+='dt=md&'
  baseUrl+='dt=qca&'
  baseUrl+='dt=rw&'
  baseUrl+='dt=rm&'
  baseUrl+='dt=ss&'
  baseUrl+='dt=t&'
  baseUrl+='ie=UTF-8&'
  baseUrl+='oe=UTF-8&'
  baseUrl+='otf=1&'
  baseUrl+='pc=1&'
  baseUrl+='ssel=0&'
  baseUrl+='tsel=0&'
  baseUrl+='kc=2&'
  baseUrl+='tk='+str(tk)+'&'
  baseUrl+='q='+text
  return baseUrl
def translate(text):
  header={
    'authority':'translate.google.cn',
    'method':'GET',
    'path':'',
    'scheme':'https',
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
'x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
  }
  url=buildUrl(text,js.getTk(text))
  res=''
  try:
      r=requests.get(url)
      result=json.loads(r.text)
      if result[7]!=None:
      # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
          try:
              correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
              print(correctText)
              correctUrl=buildUrl(correctText,js.getTk(correctText))
              correctR=requests.get(correctUrl)
              newResult=json.loads(correctR.text)
              res=newResult[0][0][0]
          except Exception as e:
              print(e)
              res=result[0][0][0]
      else:
          res=result[0][0][0]
  except Exception as e:
      res=''
      print(url)
      print("翻译"+text+"失败")
      print("错误信息:")
      print(e)
  finally:
      return res
if __name__ == '__main__':
  js=Py4Js()
  res=translate('翻译继亚马逊宣布退出中国半个月后，甲骨文也启动了撤离倒计时。5月7日，甲骨文中国区突然宣布大规模裁员，研发中心1600人裁掉900人，比例高达60%!更为恐怖的是，这可能只是刚刚开始，第二批名单或将在6、7月份进行裁撤。内部人士还透露，整个甲骨文中国研发中心都要关闭。这意味着这个一度称霸全球的美国科技巨头，大有败走中国的势头。大家可能不太了解甲骨文，我在这里简单介绍一下：甲骨文是仅次于微软的全球第二大软件系统公司，市值将近2000亿美元，约等于3.5个百度，5个京东。自1989年进入中国后，甲骨文曾一度占据着中国企业一半以上的数据库市场，其创始人埃里森更是在多个场合呛声中国企业，扬言不能让中国培养太多工程师。那么，狂妄的埃里森是怎样在中国一步步沦落到今天的?答案是他碰到了一个强劲对手，这个对手像赶走eBay、亚马逊一样，用一种超强的战略眼光与执行魄力，一手埋葬了又一个美国巨头的中国梦。01最早看到云计算的人时间倒回到2008年。随着奥运会声势越来越大，淘宝网的用户也与日俱增。体量变大，意味着财富，但同时也意味着危机。这场危机就像暗流般在阿里巴巴这艘大船下涌动，每天上午，服务器的使用率就会飙升到 98%，离爆棚仅差两个点。此外，淘宝页面上的各种问题也已危如累卵，如果再不解决，后果会不堪设想。当时，全球企业普遍使用的是IOE架构的服务器，阿里巴巴也不外如是，其中“O”是“Oracle”的缩写，正是甲骨文公司。随着用户量越来越大，这种数据库架构开始暴露问题，无法满足大企业的需要。最早看到这个陈弊的是亚马逊、微软，以及阿里巴巴。早在2007年底，马云就召集了阿里高层开会，针对服务器问题吵了两天两夜。最终，马云力排众议决定要做一个数据的大一统，并由他拍板项目命名为阿里“登月计划”。战略出来了，找什么人落地?马云从微软挖来了亚洲研究院副院长王坚博士。2009年，王坚带着一支30多人组成的“飞天团队”正式挂出了阿里云的项目牌。这是阿里云这个名字历史上第一次对外公布，这支团队将在十年后成为甲骨文中国的掘墓人。02孤独的行者虽然中国云计算目前排名世界第二，但在十年前几乎没有任何人看好马云，即使是十八罗汉也部分持怀疑态度。这一点，我们稍后再讲，眼下，马云面对的将是互联网大佬的嗤之以鼻。阿里云开干一年后，中国IT领袖峰会在深圳举办，BAT掌门人齐齐亮相，论剑云计算。首先亮剑的是李彦宏。他说道：“云计算这个东西，不客气一点讲，它是新瓶装旧酒，没有新东西。早期的时候，15年前大家讲客户端跟服务器这个关系，再往后大家讲基于互联网web界面的服务，现在讲云计算。实际上，本质上都是一样。”过了几分钟，马化腾接过话题：“云计算这个话题比较技术性，它是一个比较超前的概念。我觉得这个事可能你过几百年、一千年后，到‘阿凡达’那时确实有可能。但现在还是过于早了。”李彦宏和马化腾都是技术出身，对云计算肯定有过很多了解，代表了互联网界对云计算的普遍态度。可偏偏不懂技术的马云却在这时候和公众“唱起了反调”，他拿起话筒说出了一段时代最强音：“我的理解，云计算最后是一种分享，数据的处理、存储并分享的机制。我们自己公司对云计算是充满信心，也充满了希望!”话音落下，在场的人有的轻笑，有的诧异，议论纷纷。马化腾和李彦宏的话虽然只有短短几分钟，却埋下了后来阿里内部“逼宫”的炸弹，让阿里云这个新生儿差点夭折。03不做云计算，阿里会死!白驹过隙，3年时间一晃而过。到了2012年，阿里云还是起色不大，内部不成体系，面对5K瓶颈，王坚始终没办法突破。又烧钱又消耗人力，3年时间没搞出什么名堂，阿里内部对阿里云的质疑声越来越大。还有的人把马化腾和李彦宏的话搬出来，指责王坚就是来阿里骗钱的，更有甚者直接捏造了马云要解散阿里云的谣言。由于没有成绩没有进展，连续几年阿里云都在阿里集团拿的是最低分。离职的人越来越多，来来去去走了80%，很多离去的人走前都说了一句：云计算不可能完成。此刻的马云犹豫吗?肯定犹豫。深谙历史的他不会没看过袁崇焕立下五年复辽誓言的典故，最后辽东没收成，大明被李自成抄了底。他在2012年的年会上说：“我没有想过公司内部对阿里云有那么大的意见，我真没想到。”可云计算这事要做吗?一定要做!为什么?因为马云看到云计算的第一反应不是能不能完成，而是我需要它!在分歧面前，马云几乎是拍着桌子喊道：“不做云计算，阿里会死!”“我每年投10亿，投个10年，做不出来再说!”马云的咆哮是有深刻依据的。自2009年推出双11以来，人们洪水般的“买买买”已让淘宝天猫服务器的压和')
  print(res)