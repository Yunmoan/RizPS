# Riz PS

这是对于 Rizline（律动轨迹）游戏港澳台版本的服务端重实现，不装了摊牌了，从名字就能看出来，PS = Private Server，这其实就是个律动轨迹的私服

## 开发计划

- [x] 完整模拟雷霆SDK
- [x] 账号登陆并去除区域、手机卡限制
- [x] 正常存档/加载歌曲
- [x] 游戏内更新、歌曲下载（因为发现可以直接直连下载，所以resources功能不用做了）
- 内购全解锁因必须修改游戏包体，以及出于对鸽游的支持与尊重，将不打算继续制作，且根据用户反馈，在官方服务器中购买并解锁了的歌曲在RizPS中也同样会解锁

## 已知问题
1. 游戏内资源下载较慢，主要体现在第一次启动游戏、下载歌曲和进入歌曲时（主要流量要经过电脑再到手机，还要在mitmproxy那里卡会儿，但也不会慢多少）
2. 首次下载游戏在没连过官服的情况下可能无法使用RizPS（已修复？）

## 经过测试的设备
- [x] iPhone X (iOS16 + AppStore台服Rizline1.0.2)
- [x] Mumu安卓模拟器 (Android12 + GooglePlay HK版Rizline1.0.2)

## 如何使用

### 克隆仓库并补全依赖及设置proxy

Riz PS 的运行依赖于 npm、node、python3 以及 python3 的库 mitmproxy（可以直接通过 pip 安装），请先安装好这些东西并配置好环境变量

使用以下命令克隆仓库：

```shell
git clone https://github.com/Searchstars/RizPS
```

cd 到克隆出文件夹里，然后用以下命令补全 node_modules：

```shell
npm install
```

最后打开`proxy_config.py`，将里面的REMOTE_HOST改为对于手机来说你电脑的ip

### 在你的设备上信任 mitmproxy 证书

运行这条命令，并且保持开启不要关闭:

```shell
mitmdump -s proxy.py -k --set block_global=false
```

确保你手机跟电脑在同一局域网下，在手机上将 WiFi 代理设置为 [电脑IP:8080]（下载好证书之后请恢复原来的设置，否则会导致无法联网），使用浏览器打开 mitm.it

不出意外的话应该能看到几个系统的图标，若显示 "If you can see this, traffic is not passing through mitmproxy."，请检查你的代理设置是否正确

#### Android

Android 端的配置需要进行证书格式转换，故请事先在电脑上安装 OpenSSL

在刚才的网页中点击 Android 右边的"Get mitmproxy-ca-cert.cer"并将下载好的 .cer 格式证书传到电脑上

运行这条命令

```shell
openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.cer
```

输出的第一行加上 `.0` 就是你的证书名称，比如输出的是 `c8750f0d`，证书就应该被重命名为 `c8750f0d.0`

由于 Google 的限制，高版本 Android 无法直接安装可供系统信任的根证书

- 方法一（需Root）：

    若 /system 分区可写，在获取 Root 权限后将重命名好的证书放入 `/system/etc/security/cacerts` 目录下重启手机即可

    若 /system 分区只读，则需要通过 Magisk 模块的方式安装证书，在 http://mitm.it/cert/magisk 即可获取用于安装的 Magisk 模块

    在安装好证书之后，打开手机的系统设置，此时应该能在 安全 - 更多安全设置 - 加密与凭据 - 信任的凭据(不同手机厂商可能位置不同) 中的系统一栏找到 mitmproxy 的证书

- 方法二：

    使用工具：
    - MT管理器
    - adb

    ## 1.提取或下载安装包
    使用 MT管理器的提取安装包功能提取安装包，你很可能会获得一个 apks 格式的安装包，我们要将其转换成 apk

    解压，里面一般有 base.apk 和 split_config.xxx.apk 两个文件

    将 split_config.xxx.apk 里的 lib 添加到 base.apk 即可

    ## 2.修改 xml 文件
    使用MT管理器的反编译 xml 功能，打开 `res/xml/lt_network_security_config.xml`
    你可能会看到以下内容
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <!--开通会员可提高反编译速度、资源代码自动转名称，以及激活智能编辑和自动补全功能-->
    <network-security-config>
        <base-config cleartextTrafficPermitted="true" />
    </network-security-config>
    ```
    按照以下示例修改
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <!--开通会员可提高反编译速度、资源代码自动转名称，以及激活智能编辑和自动补全功能-->
    <network-security-config>
        <base-config cleartextTrafficPermitted="true" />
        <domain-config>
            <!-- 要信任的域名 -->
            <!-- 跟 proxy.py 代理域名保持一致 -->
            <domain includeSubdomains="true">cfgsdkos.leiting.com</domain>
            <domain includeSubdomains="true">ltgames.aihelp.net</domain>
            <domain includeSubdomains="true">leitsdkosshushu.leiting.com</domain>
            <domain includeSubdomains="true">sdkoverseasrizlinehmt.ltgamesglobal.net</domain>
            <domain includeSubdomains="true">amp-api-edge.apps.apple.com</domain>
            <domain includeSubdomains="true">sdkoverseas.leiting.com</domain>
            <trust-anchors>
                <!-- 信任用户安装证书 -->
                <certificates src="user" />
            </trust-anchors>
        </domain-config>
    </network-security-config>
    ```
    保存，重新签名，上传电脑使用 adb 安装

    要先卸载原版安装包，后续修改如果使用同一个签名则不需要卸载

    ## 可能出现的问题
    1. INSTALL_FAILED_VERIFICATION_FAILURE

        关闭签名校验
        ```sh
        adb shell settings put global verifier_verify_adb_installs 0
        adb shell settings put global package_verifier_enable 0
        ```
    2. 手机直接安装时，出现 `安装失败(-22)`

        使用 adb 安装


#### iOS

在刚才的网页中点击 iOS 右边的"Get mitmproxy-ca-cert.pem"下载并进行安装

在设置 > 通用 > 关于本机 > 证书信任设置 中找到刚才安装的证书，将其信任即可

### 启动 node

```shell
node --tls-min-v1.2 index.js
```

随后，你便能看到服务器输出的日志了，服务器成功启动了！

### Enjoy

在确保 mitmdump 和 node 都正常运行的情况下，在手机上将 WiFi 代理设置为 [电脑IP:8080]，启动Rizline，Enjoy it😊！

游戏安装后第一次启动会下载资源文件，可能需要比较长的时间，超过10分钟再当作问题来反馈哦~

在打开游戏后，请一直使用游客登陆，忽视所有让你绑定账号或重试账号登陆的提示，若弹出请选择与继续游客登陆相关的选项

玩够了记得把手机上的代理设置恢复原状，否则会导致无法正常联网

## 游戏报错解决

### 注意：在遇到任何问题时，都请将游戏完全卸载（安卓直接删除即可，iOS请根据以下步骤删除： 设置 > 通用 > iPhone存储空间 > Rizline > 红色的删除App）后重新安装，并确保RizPS为最新版本（建议每次使用前都git pull一下）若问题仍存在，再根据下方给出的建议进行修复

更新失败（102）

> 自身网络问题，可以尝试打开梯子

登陆失败（200）

> 没连上RizPS，检查proxy_config.py里的内容是否正确

登陆失败（200）并连着用户名或密码错误

> 如果是Android，完全卸载游戏并删除全部相关资源文件后重新安装解决，如果是iOS用户，报错后点击确认（√）按钮，再次点击登陆即可

验证失败（2010）

> 报错原理未知，本人仅使用安卓模拟器复现成功一次，完全卸载游戏并删除全部相关资源文件后重新安装解决

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

## 思路梳理
1. 游戏第一次打开会从官方cdn下载assetbundles，可以理解为热更新，走服务器lvdgjosdl.ltgamesglobal.net（无需转发）
2. 如果游戏是第一次打开，请求guestLogin.do进行账号注册，后续直接请求sdkCheckLogin.do当作正式账号登陆
3. 对应请求收到后发送Fake Return骗过client即可

## 特别感谢

特别感谢开源项目 [Grasscutters/Grasscutter](https://github.com/Grasscutters/Grasscutter) 提供的 `proxy.py` 及 `proxy_config.py`
