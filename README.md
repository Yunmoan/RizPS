# Riz PS

这是对于 Rizline（律动轨迹）游戏港澳台版本的服务端重实现，使用nodejs进行编写，并使用mitmproxy + python脚本进行流量转发

### 注意：本项目目前还很不稳定且未经充分测试，因此问题较多且会经常更新，获取最新状态及询问问题请移步discord服务器

## 首先，LT Games，Fuck You

我们很清楚的知道本次Rizline只在港澳台上线，也完全能够接受不开放国内下载渠道

但是，凭什么，一款音游，必须要求全程联网？

但是，凭什么，1.0.1版本ban掉大陆sim卡，1.0.2版本锁ip？

别家锁区使劲露缝把钱赚，你家锁区不仅不漏还针对，笑死我了🤭

## 开发计划

- [x] 完整模拟雷霆SDK
- [x] 账号登陆并去除手机卡限制
- [x] 去除区域（IP）限制
- [x] 正常存档/加载歌曲
- [x] 游戏内更新、歌曲下载（因为发现可以直接直连下载，所以resources功能不用做了）
- [x] 分数修改（static_contents/SDKLogin.json）
- [x] 内购歌曲全解锁（static_contents/SDKLogin.json）

## 已知问题
1. 游戏内资源下载较慢，主要体现在第一次启动游戏、下载歌曲和进入歌曲时（主要流量要经过电脑再到手机，还要在mitmproxy那里卡会儿，但也不会慢多少）
2. 在点击探索 > “一起，开始旅途吧”常驻活动 后，会导致游戏卡在“通讯中”（其实歌曲本身就全解锁，完全没必要进入这个常驻活动）
3. iOS用户在打完歌后会出现“内部错误，请尝试重新安装游戏”，随后游戏强制退出，重启游戏恢复正常

## 经过测试的设备
- [x] iPhone X (iOS16 + AppStore台服-RizPS定制版)
- [x] iPad Air 2 (iOS15 + AppStore港服-RizPS定制版)
- [x] Mumu安卓模拟器 (Android12 + Rizline1.0.2 TaptapIO-RizPS定制版)
- [x] 小米10 (Android12 + MIUI13 + Rizline1.0.2 TaptapIO-RizPS定制版)

## 如何使用

查看Wiki [https://github.com/Searchstars/RizPS/wiki](https://github.com/Searchstars/RizPS/wiki)

## 游戏报错解决

### 注意：在遇到任何问题时，请都仔细检查index.js与proxy_config.py是否已按wiki中的说明设置正确，最好是仔细重看一遍wiki，再根据下面推荐的方案去解决，若实在不行，再尝试卸载游戏重装

Rizline尚未在你所在的地区提供服务，敬请期待！

> 未使用Rizline For RizPS定制客户端而是直接使用官方客户端进入游戏导致的（一定要使用定制客户端才可以进入RizPS！！！详细原理wiki中有解释）

无法连接到服务器，是否重试？（003-404）

> 手机代理设置不正确，没连上RizPS，请检查Shadowrocket或ProxyDroid中的配置是否已按wiki中的说明进行调整

更新失败（102）

> 自身网络问题，可以尝试打开梯子

登陆失败（200）

> 没连上RizPS，检查proxy_config.py里的内容是否正确，或Shadowrocket/ProxyDroid配置是否正确

登陆失败（200）并连着用户名或密码错误

> 如果是Android，完全卸载游戏并删除全部相关资源文件后重新安装解决，如果是iOS用户，报错后点击确认（√）按钮，再次点击登陆即可

验证失败（2010）

> RizPS版本不对，请升级到最新2.0，或是没使用Rizline For RizPS定制客户端而是直接使用官方客户端进入游戏导致的

游戏在转圈尝试登陆后崩溃

> 原理未知，概率性问题，能够多次复现，完全卸载游戏并删除全部相关资源文件后重新安装解决

## 疑难解答

mitmdump 输出正常，node 没反应，进 Rizline 更新错误100，网络错误10

> 在当前版本中，RizPS已支持游戏内资源下载，请将RizPS更新到最新版本，若问题仍存在，请在安装完成后进入首次 Rizline 时先不要在手机上开 HTTP 代理，裸连下载更新后，登陆账号时会弹出网络错误，这是正常的，退出游戏然后再打开 HTTP 代理，重开 Rizline

无法下载歌曲，进入歌曲点击开始一直未下载完成或卡加载

> 目前RizPS已支持直连官方服务器下载内容，请更新RizPS后再试，若问题仍然存在，可以打开梯子试试

能用 Fiddler Classic 代替 mitmproxy 吗？

> 不行，因为 fiddler.network.https> HTTPS handshake to 192.168.1.247 (for #96) failed. System.Security.Authentication.AuthenticationException 调用 SSPI 失败，请参见内部异常。 < 接收到的消息异常，或格式不正确。Win32 (SChannel) Native Error Code: 0x8009032615

## 社区
加入Discord：[https://discord.gg/G64wHgqfUK](https://discord.gg/G64wHgqfUK)

## 特别感谢

特别感谢开源项目 [Grasscutters/Grasscutter](https://github.com/Grasscutters/Grasscutter) 提供的 `proxy.py` 及 `proxy_config.py`

感谢kbk#4878提供逆向技术支持