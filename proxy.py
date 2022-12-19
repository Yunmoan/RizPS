##
#
#   Copyright (C) 2002-2022 MlgmXyysd All Rights Reserved.
#
##

##
#
#   Animation Company script for mitmproxy
#
#   https://github.com/MlgmXyysd/
#
#   *Original fiddler script from https://github.lunatic.moe/fiddlerscript
#
#   Environment requirement:
#     - mitmdump from mitmproxy
#
#   @author MlgmXyysd
#   @version 1.1
#
##

import collections
import random
from mitmproxy import http, connection, ctx, tls, connection
from abc import ABC, abstractmethod
from enum import Enum
from mitmproxy.utils import human
from proxy_config import USE_SSL
from proxy_config import REMOTE_HOST
from proxy_config import REMOTE_PORT
from proxy_config import PROXY_MODE

newfile = open("mitmdump-capturedata.txt","w+")
newfile.close()

class MlgmXyysd_Animation_Company_Proxy:

    LIST_ALLOW_DOMAINS = [
        "lvdgjosdl.ltgamesglobal.net",
    ]#ALLOW模式下允许直连的域名列表

    LIST_RESEND_DOMAINS = [
        "cfgsdkos.leiting.com",
        #"ltgames.aihelp.net",
        "leitsdkosshushu.leiting.com",
        #"lvdgjosdl.ltgamesglobal.net",
        "sdkoverseasrizlinehmt.ltgamesglobal.net",
        "amp-api-edge.apps.apple.com",
        "sdkoverseas.leiting.com",
        "graph.facebook.com",
        "location.services.mozilla.com",
        "www.google.com",
        "google.com",
        "www.baidu.com",
        "baidu.com",
        "lvdgjosgame.ltgamesglobal.net",
        "updateos.leiting.com"
        #"skadsdk.appsflyer.com"
    ]#RESEND模式下需要转发的域名列表
    def request(self, flow: http.HTTPFlow) -> None:
        print("原请求URL：" + flow.request.url)
        if PROXY_MODE == "ALLOW":
            if flow.request.host in self.LIST_ALLOW_DOMAINS:#ALLOW模式下，如果访问的域名是允许的，则什么都不干，否则替换Host和Port
                pass
            else:
                if USE_SSL:
                    flow.request.scheme = "https"
                else:
                    flow.request.scheme = "http"
                flow.request.host = REMOTE_HOST
                flow.request.port = REMOTE_PORT
        elif PROXY_MODE == "RESEND":
            if flow.request.host in self.LIST_RESEND_DOMAINS:#RESEND模式下，如果访问的域名是需要转发的，则替换Host和Port
                if USE_SSL:
                    flow.request.scheme = "https"
                else:
                    flow.request.scheme = "http"
                flow.request.host = REMOTE_HOST
                flow.request.port = REMOTE_PORT

    def http_connect(self, flow: http.HTTPFlow) -> None:
        if "graph.facebook.com" in flow.request.host:
            if USE_SSL:
                    flow.request.scheme = "https"
            else:
                flow.request.scheme = "http"
            flow.request.host = REMOTE_HOST
            flow.request.port = REMOTE_PORT
            print("CONNECT " + str(flow.request.host) + ":" + str(flow.request.port))
        elif "leitsdkosshushu.leiting.com" in flow.request.host:
            if USE_SSL:
                    flow.request.scheme = "https"
            else:
                flow.request.scheme = "http"
            flow.request.host = REMOTE_HOST
            flow.request.port = REMOTE_PORT
            print("CONNECT " + str(flow.request.host) + ":" + str(flow.request.port))
        else:
            pass
    
class InterceptionResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    SKIPPED = 3


class TlsStrategy(ABC):
    def __init__(self):
        self.history = collections.defaultdict(lambda: collections.deque(maxlen=200))

    @abstractmethod
    def should_intercept(self, server_address: connection.Address) -> bool:
        raise NotImplementedError()

    def record_success(self, server_address):
        self.history[server_address].append(InterceptionResult.SUCCESS)

    def record_failure(self, server_address):
        self.history[server_address].append(InterceptionResult.FAILURE)

    def record_skipped(self, server_address):
        self.history[server_address].append(InterceptionResult.SKIPPED)


class ConservativeStrategy(TlsStrategy):
    def should_intercept(self, server_address: connection.Address) -> bool:
        return InterceptionResult.FAILURE not in self.history[server_address]


class ProbabilisticStrategy(TlsStrategy):
    def __init__(self, p: float):
        self.p = p
        super().__init__()

    def should_intercept(self, server_address: connection.Address) -> bool:
        return random.uniform(0, 1) < self.p


class MaybeTls:
    strategy: TlsStrategy

    def load(self, l):
        l.add_option(
            "tls_strategy", int, 0,
            "TLS passthrough strategy. If set to 0, connections will be passed through after the first unsuccessful "
            "handshake. If set to 0 < p <= 100, connections with be passed through with probability p.",
        )

    def configure(self, updated):
        if "tls_strategy" not in updated:
            return
        if ctx.options.tls_strategy > 0:
            self.strategy = ProbabilisticStrategy(ctx.options.tls_strategy / 100)
        else:
            self.strategy = ConservativeStrategy()

    def tls_clienthello(self, data: tls.ClientHelloData):
        server_address = data.context.server.peername
        if not self.strategy.should_intercept(server_address):
            ctx.log(f"TLS passthrough: {human.format_address(server_address)}.")
            data.ignore_connection = True
            self.strategy.record_skipped(server_address)

    def tls_established_client(self, data: tls.TlsData):
        server_address = data.context.server.peername
        ctx.log(f"TLS handshake successful: {human.format_address(server_address)}")
        self.strategy.record_success(server_address)

    def tls_failed_client(self, data: tls.TlsData):
        server_address = data.context.server.peername
        ctx.log(f"TLS handshake failed: {human.format_address(server_address)}")
        self.strategy.record_failure(server_address)
        
addons = [
	MlgmXyysd_Animation_Company_Proxy(),
    MaybeTls()
]