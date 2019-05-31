import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

#定义一个cookie字典,用于传递获取的cookie到服务器
def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict

#cookie可以首次通过F12 检查源码的方式获取.
cookie = "Xdwuv=5444177068682; _PVXuv=5c0df1a5758f7; bbs_cookietime=31536000; bdshare_firstime=1544417725922; __isshowad=no; _9755xjdesxxd_=32; Hm_lvt_53eb54d089f7b5dd4ae2927686b183e0=1555987037,1556589321,1557885804,1558400320; _fuv=5589189849297; _fwck_www=911b463a524b13fb4c5bfdef763249e1; _appuv_www=5bdc4f5d1d375d4098a222269f9bac9e; _Xdwnewuv=1; fw_slc=1%3A1558919010%3B1%3A1558919012%3B1%3A1558919013%3B1%3A1558919016%3B1%3A1558919017; fw_pvc=1%3A1558918998%3B1%3A1558919021%3B1%3A1558919090%3B1%3A1558919100%3B1%3A1558919119; fw_exc=1%3A1558919040%3B1%3A1558919119%3B1%3A1558919132%3B1%3A1558919144%3B1%3A1558919244; fw_clc=1%3A1558919020%3B1%3A1558919119%3B1%3A1558919173%3B1%3A1558919234%3B1%3A1558919726; _locationInfo_=%7Burl%3A%22http%3A%2F%2Fchengdu.xcar.com.cn%2F%22%2Ccity_id%3A%22386%22%2Cprovince_id%3A%2217%22%2C%20city_name%3A%22%25E6%2588%2590%25E9%2583%25BD%22%7D; _fwck_my=2821ee2d6268236c391a18b95cf27424; _appuv_my=9797e5988f5ce4bbd631ec6e22409d59; bbs_visitedfid=46D1109D91D43D114D1588D44D271D456D120D1783D53D255; NSC_tizu-ydbs-nzydbs-80=ffffffff093c263345525d5f4f58455e445a4a423660; uv_firstv_refers=http%3A//www.xcar.com.cn/bbs/forumdisplay.php%3Ffid%3D46; gdxidpyhxdE=4coGEY3v3tc4Zf4%5C%5Cefrakdy3G3dIcRp2%2BcIZv62h3iRmdDx0%5Ch5ZjHEl%2FgpJBja9VuzXAumhdOl6BNiqVyUD6BXaCcc0atQEljvCApinDp5u85s0hnNtUq2v9MoBrjti64K9C%5CeUei3VdaQet33JIPvYqHM%2FUozRNs8bvM8mPQQycxb%3A1559106478693; xgame_ly=http%3A%2F%2Fmy.xcar.com.cn%2Fmsg%2Freply.php; xgame_currweb=http%3A%2F%2Fmy.xcar.com.cn%2Fthread%2Findex.php; bbs_oldtopics=D90491004D90491135D; bbs_fid46=1559105708; _Xdwstime=1559105859; _discuz_uid=1503476; _discuz_pw=5d7e2da6fae3d9645c95e1f2f0df1455; _xcar_name=object; _discuz_vip=0; bbs_auth=XRrhu1Bxq0oPMCAh7sMUslpgsS7e5xzrOXDTvpLZByoOi2L2t75aq4bRKkemaV5DCQ"

def auto_post_thread(pid):
    #登陆xcar论坛前，首先获取cookie,然后将cookie传进去，并且要注意content-type设置对，可以在F12里面看到header信息,回帖的url具体信息。
    #formhash很重要,这个值在不同的用户下是要变化的。注意替换
    #下面是在浏览器时候抓取的form data
    # tid: 90490892
    # fid: 46
    # action: reply
    # mt: 0.15811883823819106
    # land: lord
    # message: 90490892
    # formhash: 068a1185
    # usesig: 1
    # ssid: 1559108236
    # replysubmit: yes
    #print('开始回复...')
    header = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','X-Request-Id': '1728;r=8304846','X-Requested-With': 'XMLHttpRequest','X-Tingyun-Id': 'WFf2deMYFr8;r=108304846','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    params = {'tid':pid,'fid':'46','action':'reply','mt':'0.8126003607040919','land':'lord','message':'[微笑][微笑][微笑]',
             'formhash':'068a1185','usesig':'1','ssid':'1559095286','replysubmit':'yes'} #注意formhash在每个用户下面是不一样的值

    # respLogin = requests.Session().post(url='http://my.xcar.com.cn/thread/index.php',headers=header, cookies=cookie_to_dict(cookie))
    # respLogin.encoding = 'gb2312'
    # html=respLogin.text
    resp = requests.Session().post(url='http://www.xcar.com.cn/bbs/post.php', data=params, headers=header,
                         cookies=cookie_to_dict(cookie))
    resp.encoding='gb2312'
    html=resp.text
    print(datetime.now(),html)

def get_properties_from_remote():
    webPrefix = "http://www.xcar.com.cn"

    headerBrowse = {'content-type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    resp = requests.post(url='http://www.xcar.com.cn/bbs/forumdisplay.php?fid=46&page=1', headers=headerBrowse, cookies=cookie_to_dict(cookie))
    resp.encoding='utf-8'
    html = resp.text

    soup = BeautifulSoup(html, 'lxml')
    # 通过tag的ID属性查找
    itemList = soup.find_all('dl', class_='list_dl')
    for itemdl in itemList:
            if(itemdl.find('span',class_= 'tdate') == None or (itemdl.find('span', class_='icon icon-lock'))):
                continue
            attrpropa = itemdl.find_all('a', target="_blank", class_="linkblack")
            attrs = itemdl.a['href'] # 获取这个标签下第一个a属性中的href值
            reply = itemdl.find('span', class_='fontblue').string
            if ("viewthread" not in attrs)  :
                continue
            props = attrs.split('=')
            pid = int(props[1])
            replycount = int(reply)
            #print('当前帖子%d回复量:%d' % (pid, replycount))
            if replycount < 2:
                auto_post_thread(pid)

get_properties_from_remote()

scheduler = BackgroundScheduler()
scheduler.add_job(get_properties_from_remote, 'interval', seconds=600)
# 这里的调度任务是独立的一个线程
scheduler.start()

try:
    # 其他任务是独立的线程执行
    while True:
        time.sleep(50)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print('Exit The Job!')
#print(html)


