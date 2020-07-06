# 更新 2020年7月6日17:57:26

最新破解步骤有时间会更新一下，尽请关注。

IT之家签到程序，~~可多次请求api获取上百金币，api链接中coinHistoryType字段为添加金币途径，设置为不同值就可以添加不同途径金币收入，具体收入明细可以去app中查看。(暂且失效)~~

安装python3，再在cmd里输入`pip install requests` `pip install Crypto` 然后改动代码里用户名和密码就可以了。

# it之家加密分析

除了签到加密方式，其它的加密方式都一样。

## 加密方法

DES加密，密钥为：`qs$^w<4!`，填充方式：`zeropadding`，输出方式： `hex`，加密代码见run.py中的getHash函数(长字符串会失效，因为没有填充到合适的位数，以后更新)

其它加密的密钥为：`(#i@x*l%`

## 在线解密

网站http://tool.chacuo.net/cryptdes

测试字符串为https://dyn.ithome.com/api/comment/getnewscomment?sn=1a84e1bfdc2ec68d 中的`1a84e1bfdc2ec68d`
[![NTvJTU.png](https://s1.ax1x.com/2020/07/01/NTvJTU.png)](https://imgchr.com/i/NTvJTU)

解密结果482628，上面的链接是评论api，482628是新闻id，所以原始新闻为https://www.ithome.com/0/482/628.htm

## 常见的加密字符串

userHash为getHash(用户名+md5(密码))
其它的一般直接加密

## 最后

加密算法破解方式：反编译app，~~其实之家一直都是这个加密方式，以前的app没有加壳，所以很容易得到。~~
