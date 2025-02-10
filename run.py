import json
import binascii
import re
import requests
import time
from os import environ as ENV
from datetime import datetime
from pyDes import des, ECB

requests.packages.urllib3.disable_warnings()


# 项目链连接：https://github.com/daimiaopeng/IthomeQianDao
# 使用说明：安装python3，再在cmd里输入pip install requests 然后改动下面数据就可以了日志文件保存
# 在同目录下的log.txt
def make_up_data(data: str, mode="PAD_ZERO"):
    pad = 8 - len(data) % 8
    pad_str = ""
    if mode == "PAD_PKCS5":
        for _ in range(pad):
            pad_str += chr(pad)
    elif mode == "PAD_ZERO":
        for _ in range(pad):
            pad_str += chr(0)
    return data + pad_str


def des_encrypt2(s: str, key: str):
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


def cn(x: bytes):
    return x.decode("u8")


def getNowTime13():
    return str(int(round(time.time() * 1000)))


def getNowTime132(dtime: datetime):
    print((str(int(time.mktime(dtime.timetuple()) * 1000))))
    return str(int(time.mktime(dtime.timetuple()) * 1000))


def getTime(dtime: datetime):
    return int(time.mktime(dtime.timetuple())) * 1000


def getDate(dtime: datetime):
    return dtime.day


def getDate2(dtime: int):
    dtime: datetime = datetime.fromtimestamp(dtime / 1000)
    return dtime.day


def parseInt(data: float):
    return int(data)


def geKK(_0x249526: datetime, _0x2fce26: int):
    _0x17c13c = "hd7%b4f8p9)*fd4h5l6|)123/*-+!#$@%^*()_+?>?njidfds[]rfbcvnb3rz/ird|opqqyh487874515/%90hggigadfihklhkopjj`b3hsdfdsf84215456fi15451%q(#@Fzd795hn^Ccl$vK^L%#w$^yr%ETvX#0TaPSRm5)OeG)^fQnn6^%^UTtJI#3EZ@p6^Rf$^!O$(jnkOiBjn3#inhOQQ!aTX8R)9O%#o3zCVxo3tLyVorwYwA^$%^b9Yy$opSEAOOlFBsS^5d^HoF%tJ$dx%3)^q^c^$al%b4I)QHq^#^AlcK^KZFYf81#bL$n@$%j^H(%m^"
    _0x5c548d = getTime(_0x249526)  # 时间戳
    _0x5c59ee = getDate(_0x249526)  # 当月第几日
    _0x5c548d = round(_0x5c548d / 0xC350) * _0x5c59ee * 0x3
    if _0x2fce26 == 3:
        return (
            _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3E8) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x3E8 / 0x64) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xA) * _0x5c59ee]
        )
    elif _0x2fce26 == 8:
        return (
            _0x17c13c[parseInt(_0x5c548d % 0x5F5E100 / 0x989680) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x989680 / 0xF4240) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0xF4240 / 0x186A0) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x186A0 / 0x2710) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3E8) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x3E8 / 0x64) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xA) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0xA) * _0x5c59ee]
        )
    else:
        return None


def geKK2(_0x249526: int, _0x2fce26: int):
    _0x17c13c = "hd7%b4f8p9)*fd4h5l6|)123/*-+!#$@%^*()_+?>?njidfds[]rfbcvnb3rz/ird|opqqyh487874515/%90hggigadfihklhkopjj`b3hsdfdsf84215456fi15451%q(#@Fzd795hn^Ccl$vK^L%#w$^yr%ETvX#0TaPSRm5)OeG)^fQnn6^%^UTtJI#3EZ@p6^Rf$^!O$(jnkOiBjn3#inhOQQ!aTX8R)9O%#o3zCVxo3tLyVorwYwA^$%^b9Yy$opSEAOOlFBsS^5d^HoF%tJ$dx%3)^q^c^$al%b4I)QHq^#^AlcK^KZFYf81#bL$n@$%j^H(%m^"
    _0x5c548d = _0x249526  # 时间戳
    _0x5c59ee = getDate2(_0x249526)  # 当月第几日
    _0x5c548d = round(_0x5c548d / 0xC350) * _0x5c59ee * 0x3
    if _0x2fce26 == 3:
        return (
            _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3E8) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x3E8 / 0x64) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xA) * _0x5c59ee]
        )
    elif _0x2fce26 == 8:
        return (
            _0x17c13c[parseInt(_0x5c548d % 0x5F5E100 / 0x989680) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x989680 / 0xF4240) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0xF4240 / 0x186A0) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x186A0 / 0x2710) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x2710 / 0x3E8) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x3E8 / 0x64) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0x64 / 0xA) * _0x5c59ee]
            + _0x17c13c[parseInt(_0x5c548d % 0xA) * _0x5c59ee]
        )
    else:
        return None


def gneKK(_0x4060f6: datetime):
    return "k" + des_encrypt2(geKK(_0x4060f6, 3), geKK(_0x4060f6, 8))


def geKsK(_0x101b3e: datetime):
    return des_encrypt2(_0x101b3e.strftime("%Y-%m-%d %H:%M:%S"), geKK(_0x101b3e, 8))


def gneKK2(_0x4060f6: int):
    return "k" + des_encrypt2(geKK2(_0x4060f6, 3), geKK2(_0x4060f6, 8))


def geKsK2(_0x101b3e: float):
    return des_encrypt2(
        datetime.fromtimestamp(_0x101b3e / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        geKK2(_0x101b3e, 8),
    )


def getSign():
    now = int(time.time() * 1000)
    return "&timestamp=" + str(now) + "&" + gneKK2(now) + "=" + geKsK2(now)


def getUserHash(username: str, password: str):
    try:
        url_login = "https://my.ruanmei.com/Default.aspx/LoginUser"
        data = {"mail": username, "psw": password, "rememberme": "true"}
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "my.ruanmei.com",
            "Origin": "http://my.ruanmei.com",
            "Referer": "http://my.ruanmei.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = requests.post(
            url=url_login, data=json.dumps(data), headers=header
        ).headers["Set-Cookie"]
        return re.search(r"user=hash=[a-zA-Z0-9]+", response).group()[10:]
    except Exception as e:
        raise ExceptionGroup("可能密码错误", [e])


def signWithHash(user_hash: str):
    qiandaocode = [
        0,
        # 1,
        # 2,
        # 3,
        # 256,
        # 257,
        # 258,
        # 259,
        # 512,
        # 513,
        # 514,
        # 515,
        # 768,
        # 769,
        # 770,
        # 771
    ]
    endt = getSign()
    session = requests.session()
    session.verify = False
    session.headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36 ithome/rmsdklevel2/night/7.26",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "x-requested-with": "com.ruanmei.ithome",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://my.ruanmei.com/app/user/signin.html?hidemenu=1&appver=2",
    }
    error: list[Exception] = []
    for fuck in qiandaocode:
        try:
            url_qiandao = f"https://my.ruanmei.com/api/usersign/sign?userHash={user_hash}&type={fuck}&endt={endt}"
            qiandao = session.get(url=url_qiandao).json()
            print(f"签到 (type {fuck})：{qiandao}")
            if "msg" in qiandao:
                msg: str = qiandao["msg"]
                if msg.find("失败") != -1:
                    error.append(Exception(qiandao))
            elif "ok" not in qiandao:
                error.append(Exception("签到失败，可能是 UserHash 错误"))
        except Exception as e:
            error.append(e)
    return error


if __name__ == "__main__":
    if "USERHASH" in ENV and ENV["USERHASH"]:
        print("通过 UserHash 签到")
        error = signWithHash(ENV["USERHASH"])
        if len(error):
            raise ExceptionGroup("签到失败", error)
        else:
            print("签到成功")
    elif "USERNAME" in ENV and "PASSWORD" in ENV:
        print(f"登录 {ENV["USERNAME"]}")
        user_hash = getUserHash(ENV["USERNAME"], ENV["PASSWORD"])
        print("登录成功，开始签到")
        error = signWithHash(user_hash)
        if len(error):
            raise ExceptionGroup("签到失败", error)
        else:
            print("签到成功")
    else:
        raise Exception("请配置环境变量 USERNAME 与 PASSWORD，或 USERHASH")
