import requests
import json
import re
import datetime
import time
from pyDes import des, ECB
import binascii
import os
ENV = os.environ
requests.packages.urllib3.disable_warnings()

# 项目链连接：https://github.com/daimiaopeng/IthomeQianDao
# 使用说明：安装python3，再在cmd里输入pip install requests 然后改动下面数据就可以了日志文件保存
# 在同目录下的log.txt
def make_up_data(data, mode='PAD_ZERO'):
    pad = 8 - len(data) % 8
    pad_str = ""
    if mode == "PAD_PKCS5":
        for i in range(pad):
            pad_str += chr(pad)
    elif mode == "PAD_ZERO":
        for i in range(pad):
            pad_str += chr(0)
    return data + pad_str


def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    s = make_up_data(s)
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None)
    en = k.encrypt(s)
    return binascii.b2a_hex(en)


def des_encrypt2(s, key):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    s = make_up_data(s)
    secret_key = key
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None)
    en = k.encrypt(s)
    return binascii.b2a_hex(en).decode()


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None)
    de = k.decrypt(binascii.a2b_hex(s))
    return de


# print(des_descrypt('b1d5d07310f93d040d19ee09ce9edfc106da4ace88148d05'))

def cn(x):
    return x.decode("u8")


def getNowTime13():
    return str(int(round(time.time() * 1000)))


def getNowTime132(dtime):
    print((str(int(time.mktime(dtime.timetuple()) * 1000))))
    return str(int(time.mktime(dtime.timetuple()) * 1000))


def getTime(dtime):
    return int(time.mktime(dtime.timetuple())) * 1000


def getDate(dtime):
    return dtime.day


def getDate2(dtime):
    dtime = datetime.datetime.fromtimestamp(dtime / 1000)
    return dtime.day


def parseInt(data):
    return int(data)


def geKK(_0x249526, _0x2fce26):
    _0x17c13c = "hd7%b4f8p9)*fd4h5l6|)123/*-+!#$@%^*()_+?>?njidfds[]rfbcvnb3rz/ird|opqqyh487874515/%90hggigadfihklhkopjj`b3hsdfdsf84215456fi15451%q(#@Fzd795hn^Ccl$vK^L%#w$^yr%ETvX#0TaPSRm5)OeG)^fQnn6^%^UTtJI#3EZ@p6^Rf$^!O$(jnkOiBjn3#inhOQQ!aTX8R)9O%#o3zCVxo3tLyVorwYwA^$%^b9Yy$opSEAOOlFBsS^5d^HoF%tJ$dx%3)^q^c^$al%b4I)QHq^#^AlcK^KZFYf81#bL$n@$%j^H(%m^"
    _0x5c548d = getTime(_0x249526)  # 时间戳
    _0x5c59ee = getDate(_0x249526)  # 当月第几日
    _0x5c548d = round(_0x5c548d / 0xc350) * _0x5c59ee * 0x3
    if (_0x2fce26 == 3):
        return _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3e8) * _0x5c59ee] + _0x17c13c[
            parseInt(_0x5c548d % 0x3e8 / 0x64) * _0x5c59ee] + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xa) * _0x5c59ee];
    elif (_0x2fce26 == 8):
        return _0x17c13c[parseInt(_0x5c548d % 0x5f5e100 / 0x989680) * _0x5c59ee] + _0x17c13c[
            parseInt(_0x5c548d % 0x989680 / 0xf4240) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0xf4240 / 0x186a0) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x186a0 / 0x2710) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x2710 / 0x3e8) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x3e8 / 0x64) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x64 / 0xa) * _0x5c59ee] + _0x17c13c[parseInt(_0x5c548d % 0xa) * _0x5c59ee];
    else:
        return None


def geKK2(_0x249526, _0x2fce26):
    _0x17c13c = "hd7%b4f8p9)*fd4h5l6|)123/*-+!#$@%^*()_+?>?njidfds[]rfbcvnb3rz/ird|opqqyh487874515/%90hggigadfihklhkopjj`b3hsdfdsf84215456fi15451%q(#@Fzd795hn^Ccl$vK^L%#w$^yr%ETvX#0TaPSRm5)OeG)^fQnn6^%^UTtJI#3EZ@p6^Rf$^!O$(jnkOiBjn3#inhOQQ!aTX8R)9O%#o3zCVxo3tLyVorwYwA^$%^b9Yy$opSEAOOlFBsS^5d^HoF%tJ$dx%3)^q^c^$al%b4I)QHq^#^AlcK^KZFYf81#bL$n@$%j^H(%m^"
    _0x5c548d = _0x249526  # 时间戳
    _0x5c59ee = getDate2(_0x249526)  # 当月第几日
    _0x5c548d = round(_0x5c548d / 0xc350) * _0x5c59ee * 0x3
    if (_0x2fce26 == 3):
        return _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3e8) * _0x5c59ee] + _0x17c13c[
            parseInt(_0x5c548d % 0x3e8 / 0x64) * _0x5c59ee] + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xa) * _0x5c59ee];
    elif (_0x2fce26 == 8):
        return _0x17c13c[parseInt(_0x5c548d % 0x5f5e100 / 0x989680) * _0x5c59ee] + _0x17c13c[
            parseInt(_0x5c548d % 0x989680 / 0xf4240) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0xf4240 / 0x186a0) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x186a0 / 0x2710) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x2710 / 0x3e8) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x3e8 / 0x64) * _0x5c59ee] + _0x17c13c[
                   parseInt(_0x5c548d % 0x64 / 0xa) * _0x5c59ee] + _0x17c13c[parseInt(_0x5c548d % 0xa) * _0x5c59ee];
    else:
        return None


def gneKK(_0x4060f6):
    return 'k' + des_encrypt2(geKK(_0x4060f6, 3), geKK(_0x4060f6, 8))


def geKsK(_0x101b3e):
    return des_encrypt2(_0x101b3e.strftime('%Y-%m-%d %H:%M:%S'), geKK(_0x101b3e, 8))


def gneKK2(_0x4060f6):
    return 'k' + des_encrypt2(geKK2(_0x4060f6, 3), geKK2(_0x4060f6, 8))


def geKsK2(_0x101b3e):
    return des_encrypt2(datetime.datetime.fromtimestamp(_0x101b3e / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                        geKK2(_0x101b3e, 8))


def getSign():
    now = int(time.time() * 1000)
    return "&timestamp=" + str(now) + "&" + gneKK2(now) + "=" + geKsK2(now)


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

        if 'USERNAME'  in ENV or 'PASSWORD'  in ENV :
            # 云函数时间可能早8个小时，应该使用下面时间
            time =  (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            time = current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("tiem:"+time)
        endt = getSign()
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
            url_qiandao = 'https://my.ruanmei.com/api/usersign/sign?userHash=%s&type=%s&endt=%s' % (
                user_hash, fuck, endt)
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
    if 'USERNAME' not in ENV or 'PASSWORD' not in ENV :
        print("未配置环境变量USERNAME和PASSWORD")
    else:
        i['username'] = ENV['USERNAME']
        i['password'] = ENV['PASSWORD']
        code = run(i['username'], i['password'])
    
