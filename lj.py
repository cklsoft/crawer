#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import urllib
import urllib2


def getXiaoQuId(name):
    h = re.compile(name + '二手房" href=".{5,500}?class="totalSellCount">')
    baseUrl = 'http://hz.lianjia.com/xiaoqu/rs'
    url = baseUrl + urllib.quote(name)
    p = urllib2.urlopen(url)
    data = p.read()
    x = ''
    list = h.findall(data)
    if len(list) <= 0:
        return None;
    pos = list[0].find('href="')
    if pos < 0:
        return None
    return list[0][pos + 6:-25]


def format(url):
    pos = url.rfind('/', 0, len(url) - 1)
    return url[0:pos + 1] + 'co32|l3a3a4p3p4' + url[pos + 1:]


def analysis(l):
    pos = l.find('href=', l.find('<a class="img " href="'))
    pos2 = l.find('target', pos + 1)
    link = l[pos + 6:pos2 - 2]
    pos = l.find('data-original="')
    pos2 = l.find('alt', pos + 1)
    img = l[pos + 15:pos2 - 2]
    pos = l.find('alt="', pos2)
    pos2 = l.find('>', pos + 1)
    title = l[pos + 5:pos2 - 1]
    pos = l.find('totalPrice"><span>')
    pos2 = l.find('</span>', pos + 1)
    price = l[pos + 18:pos2]
    pos = l.find('unitPrice')
    pos = l.find('span', pos + 1)
    pos2 = l.find('元/平米</span>', pos)
    unitPrice = str(round(int(l[pos + 11:pos2]) / 10000.0, 1))
    pos=l.find('positionIcon',l.find('class="flood"'))
    pos2=l.find('<a',pos)
    flood=l[pos+21:pos2-3]
    pos = l.find('</a>', l.find('houseInfo') + 1)
    pos2 = l.find('</div>', pos + 1)
    info = flood+'|'+l[pos + 7:pos2]
    pos = l.find('</span>', l.find('followInfo') + 1)
    pos2 = l.find('</div>', pos + 1)
    visit = l[pos + 7:pos2]
    return {
        'link': link,
        'img': img,
        'title': title,
        'price': price,
        'unitPrice': unitPrice,
        'info': info,
        'visit': visit
    }


def getList(url):
    url = format(url)
    p = urllib2.urlopen(url)
    data = p.read().replace('\n','')
    h = re.compile("<li class=\"clear\">.{0,5000}?</li>")
    list = h.findall(data)
    if len(list) <= 0:
        return []
    result = []
    for l in list:
        result.append(analysis(l))
    return result


def getAppname():
    basePath = '/home/admin/'
    os.chdir(basePath)
    h = os.listdir(basePath)
    for q in h:
        if os.path.isdir(q):
            t = os.listdir(basePath + q)
            if 'target' in t:
                return q


def render(list):
    res = '''
    <style>
      @font-face {
        font-family: 'iconfont';
        src: url('http://at.alicdn.com/t/font_1471107905_4293606.eot'); /* IE9*/
        src: url('http://at.alicdn.com/t/font_1471107905_4293606.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
        url('http://at.alicdn.com/t/font_1471107905_4293606.woff') format('woff'), /* chrome、firefox */
        url('http://at.alicdn.com/t/font_1471107905_4293606.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
        url('http://at.alicdn.com/t/font_1471107905_4293606.svg#iconfont') format('svg'); /* iOS 4.1- */
      }
    </style>
    <style type="text/css">
    *{
        margin:0;
      }
      .board{
        position: relative;
        margin:0 auto;
        max-width: 90%;
        background-color: #d9d9d9;
      }
      table{
          text-align: center;
      }
      td,th{
          max-width: 25%;
      }
      img{
          max-height: 250px;
      }
      a{
        cursor: pointer;
      }
      .img-box{
        max-height: 500px;
        overflow-y: scroll;
        background: white;
        padding: 3px;
        border-radius: 5px;
        left:0;
        top:0;
        max-width: 700px;
        position: absolute;
        border: 1px solid grey;
        box-shadow: 2px 3px 6px rgba(0,0,0,0.5);
      }
      .img-box > i:after{
        font-family: iconfont;
        content:'\e604';
        font-size:20px;
        color:grey;
        position: absolute;
        right: 5px;
        top: 5px;
        font-style: normal;
      }
      .img-box > i:hover:after{
        color:red;
      }
      .sub-img-box{
        margin: 0 auto;
        max-width: 70%;
        overflow: hidden;
      }
      .msg{
        color:red;
      }
    </style>
    <script src="http://g.alicdn.com/etao/opensearch/0.15.5/scripts/jquery-1.9.1.min.js"></script>

    <script type="text/javascript">
      $(function(){
        $('.imgd').each(function(i,x){
          $(x).on('click',function(e){
            e.stopPropagation()
            let pos=x.id.lastIndexOf('-')
            let box='#img-box-'+x.id.substr(pos+1)
            if($(box).is(':hidden')){
              $('.img-box').hide()
              $(box).css('top',e.pageY-10);
              $(box).show();
            }else{
              $(box).hide();
            }
          })
        })
        $('.img-box > i').each(function(i,x){
          $(x).on('click',function(e){
            e.stopPropagation();
            $(this).parent().hide();
          })
        })
        $('.img-box').mousedown(function(e){
            let abs_x=e.pageX-$(this).offset().left;
            let abs_y=e.pageY-$(this).offset().top;
            let that=$(this)
            $(document).on('mousemove.imgbox',function(e){
              that.css('left',e.pageX-abs_x);
              that.css('top',e.pageY-abs_y);
            }).on('mouseup',function(e){
              $(document).off('mousemove.imgbox')
              e.stopPropagation()
            })
          })
      })
    </script>
    <div class="board">'''
    res+='<div class="msg">更新时间: '+time.strftime('%Y-%m-%d %H:%M:%S')+'</div><table><thead><tr>'
    res += '<th>房源</th>'
    res += '<th>总价(单价)</th>'
    res += '<th>图片</th>'
    res += '<th>信息</th>'
    res += '<th>看房情况</th>'
    res += '</tr></thead>'
    idx=0
    m=''
    for l in list:
        res += '<tr>'
        res += '<td><a target="_blank" style=\"text-decoration: none;\" href="' + l[
            'link'] + '">' + l['title'] + '</a></td>'
        res += '<td style="color:red">' + l['price'] + '/(' + l['unitPrice'] + ')w</td>'
        imgs=getPicList(l['link'])
        m+='<div id="img-box-'+str(idx)+'" class="img-box" style="display:none">'
        for q in imgs:
            m+='<div class="sub-img-box">'
            m+='<img src="'+q['link']+'" alt="'+q['title']+'">'
            m+='</div>'
        m+='<i></i></div>'
        res += '<td class="imgd" id="main-img-'+str(idx)+'"><img src="' + l['img'] + '"></td>'
        res += '<td>' + l['info'] + '</td>'
        res += '<td>' + l['visit'] + '</td>'
        res += '</tr>'
        idx+=1
    res += '</table></div>'
    res+=m
    return res


def save(list):
    appname = getAppname()
    path = '/home/admin/%s/target/%s.war/home/templates/screen/a.vm.bk' % (appname, appname)
    f = open(path, 'w')
    data = render(list)
    f.write(data.decode('utf-8').encode('gb18030'))
    f.close()
    os.remove(path[:-3])
    os.rename(path,path[:-3])
    print 'save success...'


def getTargets(fileName):
    f = open(fileName)
    list = []
    for p in f.readlines():
        list.append(p[:-1])
    f.close()
    return list

def getPicList(url):
    print url
    p=urllib2.urlopen(url)
    data=p.read()
    r=re.compile(" housePic\"((.|\n)+)?\"left_fix\"")
    h=r.findall(data)
    if len(h)<=0:
        return []
    s,pos,list=h[0][0],0,[]
    while pos>=0:
        pos=s.find('<img src="',pos+1)
        if pos<0:
            return list
        pos2=s.find('alt',pos+1)
        if pos2<0:
            return list
        link=s[pos+10:pos2-2]
        pos3=s.find('>',pos2+1)
        if pos3<0:
            return list
        title=s[pos2+5:pos3-1]
        if len(title)>0:
            list.append({'link':link,'title':title})
        pos=pos3
    return list

if __name__ == '__main__':
    while True:
        targets = getTargets('target.txt')
        list = []
        for p in targets:
            url = getXiaoQuId(p)
            if url != None:
                t = getList(url)
                if len(t) > 0:
                    list.extend(t)
        save(list)
        print list
        hour=time.localtime().tm_hour
        time.sleep(120)
