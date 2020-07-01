import requests
import json
import re
import datetime
import Crypto.Cipher.DES
requests.packages.urllib3.disable_warnings()

# 更新时间 2020年7月1日16:48:46
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
        endt = getHash(str(datetime.date.today()))
        session = requests.session()
        session.verify=False
        for fuck in range(0, 400):
            url_qiandao = 'https://my.ruanmei.com/api/usersign/yunrilisign?userHash=%s&coinHistoryType=%s&endt=%s' % (user_hash, fuck, endt)
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
