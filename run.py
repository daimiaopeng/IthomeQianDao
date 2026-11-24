# -*- coding: utf-8 -*-
"""
IT之家自动签到与每日任务独立脚本入口。

环境变量：
- USERNAME + PASSWORD: 软媒账号（手机号/邮箱）与密码（推荐）
- USERHASH 或 TOKEN: 直接传入新版 JWT token 或旧版 userHash
- ENABLE_READ_TASK: 是否执行每日文章阅读任务（默认 true，设为 0/false 关闭）
- WECHAT_COIN_KEY: 可选，微信公众号回复「金币」获取的金币码
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from ithomesign import ITHomeClient, ITHomeError, sanitize_sensitive_text


def _env_bool(name: str, default: bool = True) -> bool:
    val = os.environ.get(name)
    if val is None or val == "":
        return default
    return val.strip().lower() not in {"0", "false", "no", "off"}


def _is_github_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS", "").lower() == "true"


def _add_github_mask(secret: str | None) -> None:
    """在 GitHub Actions 中注册动态敏感值掩码，防止动态 token 意外出现在日志中。"""
    if secret and _is_github_actions():
        print(f"::add-mask::{secret}", flush=True)


def run_workflow(
    *,
    username: str | None = None,
    password: str | None = None,
    userhash: str | None = None,
    enable_read_task: bool = True,
    wechat_coin_key: str | None = None,
    verify_already_signed: bool = False,
    check_only: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    client = ITHomeClient()
    _add_github_mask(wechat_coin_key)

    # 1. 登录鉴权（若同时配置了 USERHASH/TOKEN 与 USERNAME+PASSWORD，前者失效时自动回退密码登录）
    if userhash:
        print("[1/4] 使用 USERHASH / TOKEN 鉴权...")
        try:
            auth_info = client.login_by_userhash(userhash)
        except Exception as exc:
            if username and password:
                safe_err = sanitize_sensitive_text(str(exc), [userhash, password])
                print(f"      USERHASH / TOKEN 鉴权失败（{safe_err}），自动回退账号密码登录...")
                auth_info = client.login_by_password(username, password)
            else:
                raise
    elif username and password:
        print("[1/4] 使用账号密码登录...")
        auth_info = client.login_by_password(username, password)
    else:
        raise ITHomeError("请配置环境变量 USERNAME 与 PASSWORD，或 USERHASH / TOKEN")

    # 登录拿到动态 JWT token 后立即向 GitHub Actions 注册掩码
    _add_github_mask(client.token)

    if verbose and not _is_github_actions():
        print(
            f"      登录成功: userId={auth_info.get('userId')}, "
            f"userNick={auth_info.get('userNick')}"
        )
    else:
        print("      登录成功")

    if check_only:
        sign_info = client.get_sign_info()
        user_info = client.get_it_user_info()
        level_info = client.get_level_info()
        history = client.get_coin_history(record_type="income", max_id=0)[:5]
        return {
            "auth": auth_info,
            "signInfo": sign_info,
            "userInfo": user_info,
            "levelInfo": level_info,
            "recentIncome": history,
        }

    # 2. 每日签到与金币到账验证
    print("[2/4] 执行每日签到与金币到账核验...")
    checkin_result = client.check_in(verify_already_signed=verify_already_signed)
    if verbose and not _is_github_actions():
        print(
            f"      签到状态: {'已签到' if checkin_result['signed'] else '未签到'} "
            f"(方式={checkin_result['methodUsed']}, 连签={checkin_result['continueDays']}天, "
            f"累计={checkin_result['totalDays']}天)"
        )
        print(
            f"      金币余额: {checkin_result['coinBefore']} -> {checkin_result['coinAfter']} "
            f"(本次变动 {checkin_result['coinDelta']:+d}, "
            f"今日金币 {checkin_result['todayGainedCoin']}/{checkin_result['todayCanGainCoin']})"
        )
        if checkin_result["todaySignRecords"]:
            for rec in checkin_result["todaySignRecords"]:
                print(
                    f"      今日签到入账流水: [{rec.get('addTime')}] "
                    f"{rec.get('typeName')} +{rec.get('coin')} 金币 (id={rec.get('id')})"
                )
        else:
            print("      今日签到入账流水: 暂未查到今日签到入账记录")
    else:
        print(
            f"      签到状态: {'已签到' if checkin_result['signed'] else '未签到'} "
            f"(方式={checkin_result['methodUsed']}, "
            f"今日金币={checkin_result['todayGainedCoin']}/{checkin_result['todayCanGainCoin']}, "
            f"本次变动={checkin_result['coinDelta']:+d}, "
            f"入账核验={'通过' if checkin_result['creditedVerified'] else '未通过'})"
        )

    # 3. 金币任务状态 & 可选微信金币码绑定
    print("[3/4] 检查「领金币」页金币任务状态...")
    gold_tasks: dict[str, Any] = {
        "dailyCheckIn": {
            "gained": checkin_result["todayGainedCoin"],
            "cap": checkin_result["todayCanGainCoin"],
            "completed": checkin_result["todayGainedCoin"] >= checkin_result["todayCanGainCoin"]
            and checkin_result["todayCanGainCoin"] > 0,
        },
        "followIthome": checkin_result.get("followIthomeInfo"),
        "followRuanmei": checkin_result.get("followRuanmeiInfo"),
        "manualTasks": [
            "投递有效新闻线索（采纳得500金币，需人工投稿）",
            "参与产品百科共建（需人工编辑词条）",
            "文章勘误/错别字纠错（采纳得100金币，需人工提交）",
        ],
    }
    for label, key in (("关注IT之家公众号", "followIthome"), ("关注软媒服务号", "followRuanmei")):
        info = gold_tasks.get(key)
        if isinstance(info, dict):
            status = "已达成" if info.get("isAchieve") else "未达成"
            print(f"      {label}: {status}")

    if wechat_coin_key:
        bind_res = client.bind_wechat_coin_key(wechat_coin_key)
        gold_tasks["wechatCoinKeyBind"] = bind_res
        print(f"      微信金币码绑定: {'成功' if bind_res.get('success') else '失败'}")

    # 4. 每日文章阅读经验任务
    read_task_result: dict[str, Any] | None = None
    if enable_read_task:
        print("[4/4] 执行每日文章阅读任务...")
        read_task_result = client.run_news_read_task()
        print(
            f"      阅读经验: {read_task_result['readExpBefore']}/{read_task_result['readExpCap']} "
            f"-> {read_task_result['readExpAfter']}/{read_task_result['readExpCap']} "
            f"(上报 {read_task_result['articlesReported']} 篇)"
        )
    else:
        print("[4/4] 已跳过每日文章阅读任务 (ENABLE_READ_TASK=false)")

    if not checkin_result["creditedVerified"]:
        raise ITHomeError("签到或金币到账核验未通过")

    return {
        "auth": auth_info,
        "checkin": checkin_result,
        "goldTasks": gold_tasks,
        "readTask": read_task_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="IT之家独立自动签到与任务脚本")
    parser.add_argument("--no-read-task", action="store_true", help="不执行每日文章阅读任务")
    parser.add_argument(
        "--verify-already-signed",
        action="store_true",
        help="即便今日已签，也再次请求签到接口验证幂等返回",
    )
    parser.add_argument("--check-only", action="store_true", help="仅查询状态，不执行写操作")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="在本地输出详细账号信息（在 GitHub Actions 环境中自动禁用以防泄漏隐私）",
    )
    parser.add_argument("--json", action="store_true", help="输出完整 JSON 摘要（含账号详情，仅建议本地使用）")
    args = parser.parse_args()

    username = os.environ.get("USERNAME", "").strip()
    password = os.environ.get("PASSWORD", "").strip()
    userhash = (os.environ.get("TOKEN") or os.environ.get("USERHASH") or "").strip()
    wechat_coin_key = os.environ.get("WECHAT_COIN_KEY", "").strip() or None
    enable_read_task = (not args.no_read_task) and _env_bool("ENABLE_READ_TASK", True)

    summary = run_workflow(
        username=username or None,
        password=password or None,
        userhash=userhash or None,
        enable_read_task=enable_read_task,
        wechat_coin_key=wechat_coin_key,
        verify_already_signed=args.verify_already_signed,
        check_only=args.check_only,
        verbose=args.verbose,
    )

    if args.json and not _is_github_actions():
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("全部任务完成并验证通过。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        extra = [
            os.environ.get("USERNAME", ""),
            os.environ.get("PASSWORD", ""),
            os.environ.get("USERHASH", ""),
            os.environ.get("TOKEN", ""),
            os.environ.get("WECHAT_COIN_KEY", ""),
        ]
        print(f"执行失败: {sanitize_sensitive_text(str(exc), extra)}", file=sys.stderr)
        sys.exit(1)
