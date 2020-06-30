import requests
import json
import re
import datetime
import Crypto.Cipher.DES

# 更新时间 2020年6月30日14:48:58
# 使用说明：安装python3，再在cmd里输入pip install requests 然后改动下面数据就可以了日志文件保存
# 在同目录下的log.txt
def auto_fill(x):
    if len(x) > 24:
        raise "密钥长度不能大于等于24位！"
    else:
        while len(x) < 32:
            x += "\0"
        return x.encode()


def getHash(text):
    key = "(#i@x*l%"
    x = Crypto.Cipher.DES.new(key.encode(), Crypto.Cipher.DES.MODE_ECB)
    a = x.encrypt(auto_fill(str(text))).hex()
    return str(a)


def run(username, password):
    session = requests.session()
    url_login = 'https://my.ruanmei.com/Default.aspx/LoginUser'
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
        md5 = getHash(str(datetime.date.today()))
        url_qiandao = 'https://my.ruanmei.com/api/UserSign/Sign?userHash=%s&type=0&endt=%s' % (user_hash, md5)
        qiandao = session.get(url=url_qiandao).json()
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()) + ' ' + username + ' ' + str(qiandao['msg']) + '\n')
        print(qiandao)
    except:
        print("用户名或密码错误")


my_list = [
    {
        'username': '用户名',
        'password': '密码',
    }
]
for i in my_list:
    code = run(i['username'], i['password'])
