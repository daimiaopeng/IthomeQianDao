# IthomeQianDao - IT之家自动签到与每日任务脚本

基于 IT之家 Android 客户端（`com.ruanmei.ithome` v9.55）协议实现的独立 Python 自动化脚本，无需浏览器或 ADB 模拟点击，仅依赖 `requests` 即可独立运行，支持本地执行、Docker 及 GitHub Actions 定时运行。

## 功能说明

1. **软媒通行证登录鉴权**：
   - 支持手机号/邮箱 + 密码调用 `POST https://myapi.ruanmei.com/api/user/loginbypassword` 获取新版 JWT `token`。
   - 兼容通过 `TOKEN` 或旧版 `USERHASH`（自动检测或调用 `loginbyuserhash` 换取新版 `token`）鉴权。
2. **每日签到与双路径兜底**：
   - 优先调用「领金币」H5 签到接口 `GET https://napi.ithome.com/api/usersign/sign`。
   - 异常时自动回退至客户端原生自动签到接口 `GET https://napi.ithome.com/api/usersign/autosign`（携带 MD5 签名与 HMAC-SHA256 请求头签名）。
3. **金币到账核验**：
   - 签到前后校验 `getsigninfo`、`getuserinfo`（金币余额、`todayGainedCoin`/`todayCanGainCoin`、连签天数）与金币收入流水 `getusercoinshistorys`。
4. **金币任务 & 每日文章阅读任务**：
   - 检查「领金币」页任务状态（每日签到、关注 IT之家公众号 / 软媒服务号；可选通过 `WECHAT_COIN_KEY` 绑定微信公众号金币码）。
   - 自动完成每日「IT之家文章阅读」经验任务（`qapi.ithome.com/api/usertask/newsread`），达到每日上限自动停止。

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置环境变量并运行

支持以下两种鉴权方式（优先使用 `TOKEN` / `USERHASH`，其次 `USERNAME` + `PASSWORD`）：

```bash
# 方式一：账号密码（手机号或邮箱）
export USERNAME="你的手机号或邮箱"
export PASSWORD="你的密码"

# 方式二：直接提供新版 JWT TOKEN 或旧版 USERHASH
# export USERHASH="你的userhash或token"

# 可选：关闭每日文章阅读任务（默认开启）
# export ENABLE_READ_TASK="false"

# 可选：绑定微信公众号回复「金币」获得的金币码
# export WECHAT_COIN_KEY="你的金币码"

python run.py
```

常用命令行参数：

- `python run.py --check-only`：仅查询当前签到、金币余额、流水和阅读任务进度，不执行写操作
- `python run.py --no-read-task`：仅执行签到，不执行每日阅读任务
- `python run.py --verify-already-signed`：即便今日已签，也再次调用签到接口验证幂等返回
- `python run.py --json`：打印完整 JSON 执行摘要

### 3. GitHub Actions 定时运行

Fork 本仓库后，在仓库 `Settings -> Secrets and variables -> Actions` 中添加以下 Secrets：

- `USERNAME`：IT之家登录手机号或邮箱
- `PASSWORD`：对应密码
- 或单独添加 `USERHASH` / `TOKEN`

工作流定义位于 `.github/workflows/python-package-conda.yml`，默认每天北京时间凌晨 1 点（UTC 17:00）自动运行。
