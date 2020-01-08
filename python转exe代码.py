import requests
import json
import re
import datetime
import hashlib
import os
# cmd ：pyinstaller -F -i D:\PATH\Python\it之家签到\it.ico D:\PATH\Python\it之家签到\main(exe).py

def run(username, password):
    session = requests.session()
    url_login = 'http://my.ruanmei.com/Default.aspx/LoginUser'
    data = {'mail': username, 'psw': password, 'rememberme': 'true'}
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'my.ruanmei.com',
        'Origin': 'http://my.ruanmei.com',
        'Pragma': 'no-cache',
        'Referer': 'http://my.ruanmei.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        response = session.post(url=url_login, data=json.dumps(data), headers=header).headers['Set-Cookie']
        user_hash = re.search(r'user=hash=[a-zA-Z0-9]{160,160}', response).group()[10:]
        md5 = hashlib.md5(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
        url_qiandao = 'http://my.ruanmei.com/api/UserSign/Sign?userHash='
        url_pingbi = 'http://dyn.ithome.com/api/user/getblockuser?userhash=%s' % user_hash
        url_qiandao = 'http://my.ruanmei.com/api/UserSign/Sign?userHash=%s&type=0&endt=%s' % (user_hash,md5)
        # pingbi = session.get(url=url_pingbi).json()
        qiandao = session.get(url=url_qiandao).json()
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()) + ' ' + username + ' ' + str(qiandao['msg']) + '\n')
        print(qiandao)
    except:
        print("用户名或密码错误")
print("作者:喜欢小阔爱")
while True:
    run(str(input("请输入用户名：")), str(input("请输入密码：")))
    os.system("pause")
    os.system('cls')
