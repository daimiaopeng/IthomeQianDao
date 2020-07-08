import time
import requests
import json
import re
import Crypto.Cipher.DES

requests.packages.urllib3.disable_warnings()


# 项目链连接：https://github.com/daimiaopeng/IthomeQianDao
# 使用说明：安装python3，再在cmd里输入pip install requests 然后改动下面数据就可以了日志文件保存
# 在同目录下的log.txt

def auto_fill(x):
    if len(x) > 24:
        raise "密钥长度不能大于等于24位！"
    else:
        while len(x) < 24:
            x += "\0"
        return x.encode()


def getHash(text):
    key = "HCa%Y|7#"
    x = Crypto.Cipher.DES.new(key.encode(), Crypto.Cipher.DES.MODE_ECB)
    a = x.encrypt(auto_fill(str(text))).hex()
    return str(a)


def run(username, password):
    qiandaocode = [0, 1, 2, 3, 256, 257, 258, 259, 512, 513, 514, 515, 768, 769, 770, 771]
    url_login = 'https://my.ruanmei.com/Default.aspx/LoginUser'
    data = {'mail': username, 'psw': password, 'rememberme': 'true'}
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'my.ruanmei.com',
        'Origin': 'http://my.ruanmei.com',
        'Referer': 'http://my.ruanmei.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        response = requests.post(url=url_login, data=json.dumps(data), headers=header).headers['Set-Cookie']
        user_hash = re.search(r'user=hash=[a-zA-Z0-9]{160,160}', response).group()[10:]
        endt = getHash(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        session = requests.session()
        session.verify = False
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36 ithome/rmsdklevel2/night/7.26',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'x-requested-with': 'com.ruanmei.ithome',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://my.ruanmei.com/app/user/signin.html?hidemenu=1&appver=2',
        }
        for fuck in qiandaocode:
            url_qiandao = 'https://my.ruanmei.com/api/usersign/sign?userHash=%s&type=%s&endt=%s' % (user_hash, fuck, endt)
            try:
                qiandao = session.get(url=url_qiandao).json()
                print(qiandao)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
        print("可能密码错误")



my_list = [
    {
        'username': '用户名',
        'password': '密码',
    }
]
for i in my_list:
    code = run(i['username'], i['password'])
