# -*- coding: utf-8 -*-
"""
IT之家独立客户端协议实现（基于 com.ruanmei.ithome v9.55 DEX / H5 分析）。

功能：
1. 软媒通行证登录（手机号/邮箱+密码 -> JWT token，或旧版 userHash 换取 token）
2. 每日签到（H5 领金币页接口 + 原生自动签到签名接口兜底）
3. 金币任务状态查询、微信金币码绑定、每日文章阅读经验任务自动化
4. 签到结果与金币到账验证（金币余额、今日已领金币、金币收入流水）
"""

from __future__ import annotations

import hashlib
import hmac
import re
import time
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any
from urllib.parse import quote_plus

import requests

APP_VER = "955"
RAW_APP_VER = "9.55"
PLATFORM = "ithome_android"
CLIENT_EXTRA = "4|1"  # RmApp.ITHOME(4) + "|1"
SIGN_KEY = "cfb79201c3d20f4d8e1b26a0535ea3d4877de1f76f22afaa93468a2507d65d23"
AUTO_SIGN_SALT = "!QW@12wq"
JAVA_URLENCODER_SAFE = "-_.*"

DEFAULT_UA = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Build/TQ3A.230901.001; wv) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
    "Chrome/116.0.0.0 Mobile Safari/537.36 ithome/rmsdklevel2/day/9.55"
)

# Passport APIs (assets/passportapi_ithome.json)
URL_LOGIN_BY_PASSWORD = "https://myapi.ruanmei.com/api/user/loginbypassword"
URL_LOGIN_BY_USERHASH = "https://myapi.ruanmei.com/api/user/loginbyuserhash"
URL_REFRESH_TOKEN = "https://myapi.ruanmei.com/api/user/refreshtoken"

# Check-in & Coin APIs (signin.min.js / AutoCheckInHelper.java / coindetail)
URL_GET_SIGN_INFO = "https://napi.ithome.com/api/usersign/getsigninfo"
URL_SIGN_H5 = "https://napi.ithome.com/api/usersign/sign"
URL_SIGN_AUTO = "https://napi.ithome.com/api/usersign/autosign"
URL_GET_IT_USER_INFO = "https://napi.ithome.com/api/user/getuserinfo"
URL_COIN_HISTORY = "https://napi.ithome.com/api/fund/getusercoinshistorys"
URL_BIND_WECHAT_COIN_KEY = "https://napi.ithome.com/api/wechat/BindCoinTask"

# Daily Level / News Read Task APIs (mylevel.html / NewsInfoV8Activity.java)
URL_MY_LEVEL_INFO = "https://napi.ithome.com/api/User/MyLeveInfo"
URL_NEWS_LIST = "https://api.ithome.com/json/newslist/news"
URL_USER_TASK_NEWS_READ = "https://qapi.ithome.com/api/usertask/newsread"

CST_TZ = timezone(timedelta(hours=8))


class ITHomeError(RuntimeError):
    """IT之家接口请求或业务错误。"""


def normalize_username(username: str, default_country_code: str = "+86") -> str:
    """按 RmLoginActivity 规则格式化登录账号（纯手机号自动补国码前缀）。"""
    account = username.strip()
    if not account:
        raise ValueError("用户名不能为空")
    if "@" not in account and not re.search(r"[a-zA-Z]", account) and not account.startswith("+"):
        if "-" not in account:
            account = f"{default_country_code}-{account}"
    return account


def generate_api_sign(headers: dict[str, Any], query_params: dict[str, Any]) -> str:
    """复刻 com.ruanmei.rmkit.util.SignGenerator.getSign 的 HMAC-SHA256 签名。"""
    sign_map: dict[str, str] = {str(k): str(v) for k, v in query_params.items()}
    if "timestamp" in headers:
        sign_map["timestamp"] = str(headers["timestamp"])
    if "x-guid" in headers:
        sign_map["deviceid"] = str(headers["x-guid"])

    parts = [
        f"{k}^{quote_plus(sign_map[k], safe=JAVA_URLENCODER_SAFE)}"
        for k in sorted(sign_map.keys())
    ]
    payload = "$".join(parts).lower()
    return hmac.new(
        SIGN_KEY.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def generate_auto_sign_md5(token: str, timestamp_ms: int, sign_type: int = 0) -> str:
    """复刻 AutoCheckInHelper.checkIn 的 MD5 签名。"""
    raw = f"{token}_{timestamp_ms}_{AUTO_SIGN_SALT}_{sign_type}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def sanitize_sensitive_text(text: str, extra_secrets: list[str] | None = None) -> str:
    """脱敏错误文本中的 token、userHash、coinKey、sign 等敏感信息，避免日志泄漏。"""
    cleaned = str(text)
    if extra_secrets:
        for secret in extra_secrets:
            if secret and len(secret) >= 4:
                cleaned = cleaned.replace(secret, "***")
    cleaned = re.sub(
        r"(?i)(userhash|token|coinkey|authorization|password|psw|sign)=([^&\s'\"}\]]+)",
        r"\1=***",
        cleaned,
    )
    cleaned = re.sub(
        r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
        "***JWT***",
        cleaned,
    )
    return cleaned


def _today_cst_str() -> str:
    return datetime.now(CST_TZ).strftime("%Y-%m-%d")


class ITHomeClient:
    """IT之家独立 API 客户端。"""

    def __init__(
        self,
        token: str | None = None,
        timeout: int = 15,
        session: requests.Session | None = None,
    ) -> None:
        self.token: str = (token or "").strip()
        self.timeout: int = timeout
        self.user_info: dict[str, Any] = {}
        self.session: requests.Session = session or requests.Session()
        self.session.headers.update({"User-Agent": DEFAULT_UA})

    # ------------------------------------------------------------------
    # 请求头构造
    # ------------------------------------------------------------------
    def _passport_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": DEFAULT_UA,
            "x-extra": CLIENT_EXTRA,
            "extra": CLIENT_EXTRA,
            "appver": RAW_APP_VER,
            "Content-Type": "application/json; charset=utf-8",
        }
        if self.token:
            headers["Authorization"] = self.token
        return headers

    def _signed_headers(self, query_params: dict[str, Any]) -> dict[str, str]:
        if not self.token:
            raise ITHomeError("尚未登录，缺少 token")
        ts = str(int(time.time() * 1000))
        guid = str(uuid.uuid4())
        headers: dict[str, str] = {
            "User-Agent": DEFAULT_UA,
            "appver": APP_VER,
            "rawappver": RAW_APP_VER,
            "platform": PLATFORM,
            "x-webp": "1",
            "x-heic": "1",
            "userhash": self.token,
            "x-model": "Pixel%207",
            "x-brand": "Google",
            "timestamp": ts,
            "x-guid": guid,
        }
        headers["token"] = generate_api_sign(headers, query_params)
        return headers

    def _require_token(self) -> str:
        if not self.token:
            raise ITHomeError("尚未登录，请先调用 login_by_password 或提供有效的 USERHASH/TOKEN")
        return self.token

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        allow_empty_204: bool = False,
    ) -> requests.Response:
        """统一 HTTP 请求封装，确保异常和状态码报错不会泄漏 query 中的 token/userHash。"""
        base_url = url.split("?", 1)[0]
        secrets = [self.token] if self.token else []
        try:
            resp = self.session.request(
                method,
                url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            safe_msg = sanitize_sensitive_text(str(exc), secrets)
            raise ITHomeError(f"网络请求失败 ({base_url}): {safe_msg}") from None

        if resp.status_code >= 400:
            raise ITHomeError(f"HTTP {resp.status_code} ({base_url})")
        if not allow_empty_204 and resp.status_code == 204:
            raise ITHomeError(f"HTTP 204 空响应 ({base_url})")
        return resp

    # ------------------------------------------------------------------
    # 认证登录
    # ------------------------------------------------------------------
    def login_by_password(self, username: str, password: str) -> dict[str, Any]:
        """使用手机号或邮箱+密码登录软媒通行证，获取新版 JWT token。"""
        formatted_user = normalize_username(username)
        resp = self._request(
            "POST",
            URL_LOGIN_BY_PASSWORD,
            json_body={"userName": formatted_user, "password": password},
            headers=self._passport_headers(),
        )
        data = resp.json()
        if not data.get("success") or not isinstance(data.get("content"), dict):
            msg = data.get("message") or "登录失败"
            raise ITHomeError(f"密码登录失败: {msg}")
        content = data["content"]
        token = (content.get("token") or "").strip()
        if not token:
            raise ITHomeError("密码登录成功但未返回 token")
        self.token = token
        self.user_info = content.get("userInfo") or {}
        return {
            "userId": self.user_info.get("userId"),
            "userNick": self.user_info.get("userNick"),
            "tokenLength": len(token),
        }

    def login_by_userhash(self, user_hash: str) -> dict[str, Any]:
        """
        支持直接传入新版 JWT token 或旧版 userHash：
        - 若直接作为 token 能通过 napi/user/getuserinfo 鉴权，则直接使用；
        - 否则调用 loginbyuserhash 换取新版 JWT token。
        """
        candidate = user_hash.strip()
        if not candidate:
            raise ValueError("USERHASH/TOKEN 不能为空")

        # 先尝试直接当作新版 JWT token 校验
        self.token = candidate
        try:
            info = self.get_it_user_info()
            if info.get("userId"):
                self.user_info = info
                return {
                    "mode": "direct_token",
                    "userId": info.get("userId"),
                    "userNick": info.get("userNick"),
                }
        except Exception:
            pass

        # 回退：调用 passport loginbyuserhash 换取新版 token
        self.token = ""
        resp = self._request(
            "POST",
            URL_LOGIN_BY_USERHASH,
            json_body={"userHash": candidate},
            headers=self._passport_headers(),
        )
        data = resp.json()
        if not data.get("success") or not isinstance(data.get("content"), dict):
            msg = data.get("message") or "userHash 换取 token 失败"
            raise ITHomeError(f"USERHASH 鉴权失败: {msg}")
        content = data["content"]
        token = (content.get("token") or "").strip()
        if not token:
            raise ITHomeError("loginbyuserhash 未返回有效 token")
        self.token = token
        self.user_info = content.get("userInfo") or {}
        return {
            "mode": "exchanged_userhash",
            "userId": self.user_info.get("userId"),
            "userNick": self.user_info.get("userNick"),
        }

    def refresh_token(self) -> str:
        """刷新当前 passport token。"""
        self._require_token()
        resp = self._request(
            "GET",
            URL_REFRESH_TOKEN,
            headers=self._passport_headers(),
        )
        data = resp.json()
        new_token = (data.get("content") or "").strip()
        if data.get("success") and new_token:
            self.token = new_token
            return new_token
        raise ITHomeError(f"刷新 token 失败: {data.get('message')}")

    # ------------------------------------------------------------------
    # 状态与账本查询
    # ------------------------------------------------------------------
    def get_sign_info(self) -> dict[str, Any]:
        """查询签到状态、金币余额、连签天数及微信公众号任务状态（H5 领金币页接口）。"""
        token = self._require_token()
        resp = self._request(
            "GET",
            URL_GET_SIGN_INFO,
            params={"userHash": token},
            headers={"User-Agent": DEFAULT_UA},
            allow_empty_204=True,
        )
        if resp.status_code == 204 or not resp.text.strip():
            raise ITHomeError("获取签到信息返回空内容（token 可能无效或已过期）")
        return resp.json()

    def get_it_user_info(self) -> dict[str, Any]:
        """查询原生用户信息（金币余额、是否已签、今日可领/已领金币、等级等）。"""
        params = {
            "appver": APP_VER,
            "rawappver": RAW_APP_VER,
            "platform": PLATFORM,
        }
        resp = self._request(
            "GET",
            URL_GET_IT_USER_INFO,
            params=params,
            headers=self._signed_headers(params),
        )
        body = resp.json()
        if not body.get("success") or not isinstance(body.get("data"), dict):
            raise ITHomeError(f"获取用户信息失败: {body.get('errorMessage') or 'unknown error'}")
        return body["data"]

    def get_level_info(self) -> dict[str, Any]:
        """查询等级与每日经验任务进度（登录、文章阅读、评论等）。"""
        token = self._require_token()
        resp = self._request(
            "GET",
            URL_MY_LEVEL_INFO,
            params={"userHash": token},
            headers={"User-Agent": DEFAULT_UA},
        )
        body = resp.json()
        if not body.get("success") or not isinstance(body.get("data"), dict):
            raise ITHomeError(f"获取等级任务信息失败: {body.get('errorMessage') or 'unknown error'}")
        return body["data"]

    def get_coin_history(self, record_type: str = "income", max_id: int = 0) -> list[dict[str, Any]]:
        """查询金币收支流水（type: '' 全部 / 'income' 收入 / 'expenditure' 支出）。"""
        token = self._require_token()
        resp = self._request(
            "GET",
            URL_COIN_HISTORY,
            params={"type": record_type, "maxId": max_id, "userhash": token},
            headers={"User-Agent": DEFAULT_UA},
        )
        body = resp.json()
        if not body.get("success"):
            return []
        return body.get("data") or []

    # ------------------------------------------------------------------
    # 签到执行
    # ------------------------------------------------------------------
    def sign_h5(self) -> dict[str, Any]:
        """路径 A：H5 领金币页签到接口（signin.min.js）。"""
        token = self._require_token()
        resp = self._request(
            "GET",
            URL_SIGN_H5,
            params={"userHash": token},
            headers={"User-Agent": DEFAULT_UA},
        )
        return resp.json()

    def sign_auto(self, sign_type: int = 0) -> dict[str, Any]:
        """路径 B：原生自动签到接口（AutoCheckInHelper.java，带 MD5 + HMAC 双重签名）。"""
        token = self._require_token()
        ts_ms = int(time.time() * 1000)
        md5_sign = generate_auto_sign_md5(token, ts_ms, sign_type=sign_type)
        params = {
            "userHash": token,
            "time": str(ts_ms),
            "type": str(sign_type),
            "sign": md5_sign,
            "appver": APP_VER,
            "rawappver": RAW_APP_VER,
            "platform": PLATFORM,
        }
        resp = self._request(
            "GET",
            URL_SIGN_AUTO,
            params=params,
            headers=self._signed_headers(params),
        )
        return resp.json()

    def check_in(self, verify_already_signed: bool = False) -> dict[str, Any]:
        """
        执行完整签到与到账核验流程：
        1. 签到前读取 getsigninfo + getuserinfo 快照；
        2. 若未签到，先走 H5 签到接口，失败时回退原生 autosign 接口；
        3. 签到后重新拉取 getsigninfo、getuserinfo 与金币收入流水验证到账。
        """
        before_sign = self.get_sign_info()
        before_user = self.get_it_user_info()

        already_signed = bool(before_sign.get("issign") or before_user.get("isSigned"))
        method_used = "already_signed"
        sign_response: dict[str, Any] | None = None
        auto_fallback_response: dict[str, Any] | None = None

        if not already_signed or verify_already_signed:
            sign_response = self.sign_h5()
            ok = sign_response.get("ok") == 1
            msg = str(sign_response.get("msg") or "")
            if ok:
                method_used = "h5_sign"
            elif "已签到" in msg or already_signed:
                method_used = "already_signed_verified"
            else:
                # 兜底尝试原生 autosign 接口
                auto_fallback_response = self.sign_auto(sign_type=0)
                if auto_fallback_response.get("success"):
                    method_used = "native_autosign"
                else:
                    raise ITHomeError(
                        f"签到失败: h5={sign_response}, autosign={auto_fallback_response}"
                    )

        after_sign = self.get_sign_info()
        after_user = self.get_it_user_info()
        income_history = self.get_coin_history(record_type="income", max_id=0)

        today_str = _today_cst_str()
        today_sign_records = [
            rec
            for rec in income_history
            if str(rec.get("addTime", "")).startswith(today_str)
            and ("签到" in str(rec.get("typeName", "")))
        ]

        coin_before = before_sign.get("totalcoin", before_user.get("coin", 0))
        coin_after = after_sign.get("totalcoin", after_user.get("coin", 0))
        signed_now = bool(after_sign.get("issign") and after_user.get("isSigned"))
        credited_today = bool(today_sign_records) or (coin_after > coin_before)

        return {
            "signed": signed_now,
            "alreadySignedBeforeRun": already_signed,
            "methodUsed": method_used,
            "coinBefore": coin_before,
            "coinAfter": coin_after,
            "coinDelta": coin_after - coin_before,
            "todayGainedCoin": after_user.get("todayGainedCoin", 0),
            "todayCanGainCoin": after_user.get("todayCanGainCoin", 0),
            "signCoin": after_user.get("signCoin", after_sign.get("coin", 0)),
            "continueDays": after_sign.get("cdays", 0),
            "totalDays": after_sign.get("mdays", 0),
            "retroactiveCards": after_sign.get("recount", 0),
            "signResponse": sign_response,
            "autoFallbackResponse": auto_fallback_response,
            "todaySignRecords": today_sign_records,
            "creditedVerified": signed_now and credited_today,
            "followIthomeInfo": after_sign.get("followIthomeInfo"),
            "followRuanmeiInfo": after_sign.get("followRuanmeiInfo"),
        }

    # ------------------------------------------------------------------
    # 金币任务 & 每日阅读任务
    # ------------------------------------------------------------------
    def bind_wechat_coin_key(self, coin_key: str) -> dict[str, Any]:
        """绑定微信公众号回复「金币」获得的金币码（ruanmeitaskrule / ithometaskrule）。"""
        token = self._require_token()
        resp = self._request(
            "POST",
            URL_BIND_WECHAT_COIN_KEY,
            params={"coinKey": coin_key.strip(), "userhash": token},
            headers={"User-Agent": DEFAULT_UA},
        )
        return resp.json()

    def get_recent_news_ids(self, limit: int = 20) -> list[int]:
        """拉取最新资讯列表中的 newsid，用于每日阅读任务。"""
        resp = self._request(
            "GET",
            URL_NEWS_LIST,
            headers={"User-Agent": DEFAULT_UA},
        )
        data = resp.json()
        ids: list[int] = []
        seen: set[int] = set()
        for bucket in ("newslist", "toplist"):
            for item in data.get(bucket) or []:
                nid = item.get("newsid")
                if isinstance(nid, int) and nid not in seen:
                    seen.add(nid)
                    ids.append(nid)
                    if len(ids) >= limit:
                        return ids
        return ids

    def report_news_read(self, news_id: int) -> dict[str, Any]:
        """上报文章阅读任务（NewsInfoV8Activity.L4 -> qapi.ithome.com/api/usertask/newsread）。"""
        token = self._require_token()
        params = {
            "newsId": str(news_id),
            "appver": APP_VER,
            "rawappver": RAW_APP_VER,
            "platform": PLATFORM,
            "userhash": token,
        }
        resp = self._request(
            "GET",
            URL_USER_TASK_NEWS_READ,
            params=params,
            headers=self._signed_headers(params),
        )
        return resp.json()

    def run_news_read_task(self, max_articles: int = 15, delay: float = 0.5) -> dict[str, Any]:
        """自动完成每日「IT之家文章阅读」经验任务（达到今日上限即停）。"""
        before_level = self.get_level_info()
        getted_before = int(before_level.get("gettedReadExp", 0))
        total_read = int(before_level.get("totalReadExp", 0))
        exp_before = int(before_level.get("exp", 0))

        result: dict[str, Any] = {
            "expBefore": exp_before,
            "expAfter": exp_before,
            "readExpBefore": getted_before,
            "readExpAfter": getted_before,
            "readExpCap": total_read,
            "articlesReported": 0,
            "gainedReadExp": 0,
            "completed": total_read > 0 and getted_before >= total_read,
            "details": [],
        }

        if result["completed"] or total_read <= 0:
            return result

        news_ids = self.get_recent_news_ids(limit=max(max_articles, total_read * 3))
        for nid in news_ids[:max_articles]:
            res = self.report_news_read(nid)
            content = res.get("content") if isinstance(res, dict) else None
            if not isinstance(content, dict):
                content = res.get("data") if isinstance(res, dict) else None
            add_exp = int(content.get("addExp", 0)) if isinstance(content, dict) else 0
            completed = bool(content.get("completed")) if isinstance(content, dict) else False
            exp_tip = str(content.get("expTip", "")) if isinstance(content, dict) else ""

            result["articlesReported"] += 1
            result["gainedReadExp"] += add_exp
            result["details"].append(
                {
                    "newsId": nid,
                    "success": bool(res.get("success")) if isinstance(res, dict) else False,
                    "addExp": add_exp,
                    "completed": completed,
                    "expTip": exp_tip,
                }
            )
            if completed or (getted_before + result["gainedReadExp"] >= total_read):
                break
            if delay > 0:
                time.sleep(delay)

        after_level = self.get_level_info()
        result["expAfter"] = int(after_level.get("exp", exp_before))
        result["readExpAfter"] = int(after_level.get("gettedReadExp", getted_before))
        result["completed"] = result["readExpAfter"] >= total_read
        return result


# 兼容旧版导入名称
ITHomeSign = ITHomeClient
