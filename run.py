import requests
from os import environ as ENV


def getUserHash(username: str, password: str):
    session = requests.session()
    session.trust_env = False
    response = session.post(
        "https://myapi.ruanmei.com/api/user/loginbypassword",
        json={"userName": username, "password": password},
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    response.raise_for_status()
    result = response.json()
    if not isinstance(result, dict):
        raise ValueError("登录响应格式无效")
    if result.get("success") is not True:
        raise ValueError(f"登录失败：{result.get("message") or "未知错误"}")
    content = result.get("content")
    if not isinstance(content, dict):
        raise ValueError("登录响应中未找到内容")
    user_hash = content.get("userHash")
    if not isinstance(user_hash, str) or not user_hash:
        raise ValueError("登录响应中未找到 UserHash")
    return user_hash


def getSingInfo(user_hash: str):
    session = requests.session()
    session.trust_env = False
    try:
        response = session.get(
            "https://napi.ithome.com/api/usersign/getsigninfo",
            params={"userHash": user_hash},
        )
        response.raise_for_status()
        info = response.json()
        if not isinstance(info, dict):
            raise Exception(f"获取签到信息失败：{info.get('msg') or info}")
        return bool(info.get("issign"))
    except Exception as e:
        raise e
    finally:
        session.close()


def signWithHash(user_hash: str):
    session = requests.session()
    session.trust_env = False
    try:
        response = session.get(
            "https://napi.ithome.com/api/usersign/sign", params={"userHash": user_hash}
        )
        response.raise_for_status()
        qiandao = response.json()
        print(f"签到：{qiandao}")
        if not isinstance(qiandao, dict) or qiandao.get("ok") != 1:
            raise Exception(f"签到失败：{qiandao.get("msg") or qiandao}")
    except Exception as e:
        raise e
    finally:
        session.close()
    return None


def getUserHashFromEnv():
    if "USERHASH" in ENV and ENV["USERHASH"]:
        print("通过 UserHash 签到")
        return ENV["USERHASH"]
    elif "USERNAME" in ENV and "PASSWORD" in ENV:
        print(f"登录 {ENV["USERNAME"]}")
        user_hash = getUserHash(ENV["USERNAME"], ENV["PASSWORD"])
        print("登录成功，开始签到")
        return user_hash
    else:
        raise Exception("请配置环境变量 USERNAME 与 PASSWORD，或 USERHASH")


if __name__ == "__main__":
    user_hash = getUserHashFromEnv()
    isSign = getSingInfo(user_hash)
    if isSign:
        print("已经签到过了")
    else:
        error = signWithHash(user_hash)
        if error:
            raise ExceptionGroup("签到失败", error)
        else:
            print("签到成功")
