# encoding:utf-8
"""
@author:zixing
@email:zixing131@qq.com
@date:2018-08-28 11:37
#2020-03-08 添加云日历windows客户端签到
"""

# import EmailHelper
import binascii
import requests
import time

from datetime import datetime
from pyDes import des, ECB

# 秘钥
# KEY = "(#i@x*l%"
# KEY = "qs$^w<4!"
# KEY = "HCa%Y|7#"
KEY = "+f/1+hfh"


def make_up_data(data: str, mode="PAD_ZERO"):
    pad = 8 - len(data) % 8
    pad_str = ''
    if mode == "PAD_PKCS5":
        for _ in range(pad):
            pad_str += chr(pad)
    elif mode == "PAD_ZERO":
        for _ in range(pad):
            pad_str += chr(0)
    return data + pad_str


def des_encrypt(s: str):
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


def des_descrypt(s: str) -> str:
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


# print(des_descrypt("b1d5d07310f93d040d19ee09ce9edfc106da4ace88148d05"))


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
    return 'k' + des_encrypt2(geKK(_0x4060f6, 3), geKK(_0x4060f6, 8))


def geKsK(_0x101b3e: datetime):
    return des_encrypt2(_0x101b3e.strftime("%Y-%m-%d %H:%M:%S"), geKK(_0x101b3e, 8))


def gneKK2(_0x4060f6: int):
    return 'k' + des_encrypt2(geKK2(_0x4060f6, 3), geKK2(_0x4060f6, 8))


def geKsK2(_0x101b3e: float):
    return des_encrypt2(
        datetime.fromtimestamp(_0x101b3e / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        geKK2(_0x101b3e, 8),
    )


# now = datetime.now()
# now = 1599095410
# now = datetime.fromtimestamp(now)
# print(now)
# print(geKK(now,3))
# print(geKK(now,8))
# print(gneKK(now))
# print(geKsK(now))


class ITHomeSign:
    def __init__(self, userhash: str):
        self.urlhead = "http://my.ruanmei.com/"
        self.userhash = userhash
        self.UA = "Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 ithome/rmsdklevel2/day/7.37"

    def getSign(self):
        now = int(time.time() * 1000)
        return "&timestamp=" + str(now) + "&" + gneKK2(now) + "=" + geKsK2(now)

    def sign(self):
        # endt = des_encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        headers = {
            "Referer": "https://my.ruanmei.com/app/user/signin.html?hidemenu=1&appver=2"
        }
        url = (
            self.urlhead
            + "api/usersign/sign?userHash="
            + self.userhash
            + "&type=0"
            + self.getSign()
        )
        result = requests.get(url, headers=headers)
        return result.content

    def signlapin(self):
        # endt = des_encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        url = (
            self.urlhead
            + "/api/usersign/sign?userHash="
            + self.userhash
            + "&type=1&platform=lapinapp_android&channel=official"
            + self.getSign()
        )
        headers = {
            "Referer": "https://my.ruanmei.com/app/user/signin.html?hidemenu=1&appver=2"
        }
        result = requests.get(url, headers=headers)
        return result.content

    def signyunrili(self):
        # endt = des_encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        url = (
            self.urlhead
            + "api/usersign/yunrilisign?userHash="
            + self.userhash
            + "&coinHistoryType=160&appver=3.03&platform=windows"
            + self.getSign()
        )
        headers = {
            "Referer": "https://my.ruanmei.com/app/user/signin.html?hidemenu=1&appver=2"
        }
        result = requests.get(url, headers=headers)
        return result.content

    def signyunriliAndroid(self):
        # endt = des_encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        url = (
            self.urlhead
            + "api/usersign/yunrilisign?userHash="
            + self.userhash
            + "&coinHistoryType=159"
            + self.getSign()
        )
        headers = {
            "Referer": "https://my.ruanmei.com/app/user/signinyunrili.html?from=mytime_android"
        }
        result = requests.get(url, headers=headers)
        return result.content


if __name__ == "__main__":
    print("Start IThome sign.")
    ithome = ITHomeSign("sign")
    signresult = ithome.sign()
    print((cn(signresult)))

    print((cn(ithome.signlapin())))
    print((cn(ithome.signyunrili())))
    print((cn(ithome.signyunriliAndroid())))
    if signresult.find("失败".encode()) > -1:
        print("签到失败")
        # EmailHelper.sendEmailByZixing163("IT之家签到反馈", signresult)
    else:
        print("签到成功")
