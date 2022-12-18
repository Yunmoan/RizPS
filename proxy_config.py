import os

# This can also be replaced with another IP address.
USE_SSL = True
REMOTE_HOST = "192.168.1.247"
REMOTE_PORT = 443
PROXY_MODE = "RESEND"#RESEND：按需转发模式 ALLOW：按需允许模式   目前经过测试建议使用RESEND，ALLOW可用性未知，甚至可能连游戏都进不去

if os.getenv('MITM_REMOTE_HOST') != None:
    REMOTE_HOST = os.getenv('MITM_REMOTE_HOST')
if os.getenv('MITM_REMOTE_PORT') != None:
    REMOTE_PORT = int(os.getenv('MITM_REMOTE_PORT'))
if os.getenv('MITM_USE_SSL') != None:
    USE_SSL = bool(os.getenv('MITM_USE_SSL'))

print('MITM Remote Host: ' + REMOTE_HOST)
print('MITM Remote Port: ' + str(REMOTE_PORT))
print('MITM Use SSL ' + str(USE_SSL))