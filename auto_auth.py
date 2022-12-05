""" 某高専のネットワーク自動認証スクリプト

Usage:
    ・19,20行目のUSER_NAME, PASSWORDを自分のものに変える
    https://github.com/physics11688/TCT_AutoAuthentication

Author:
    physics11688 - 3.12.2022
"""

from time import sleep
import urllib.request
import urllib.parse
import ssl
from socket import gethostname
from platform import system

# ユーザー名やら何やら
USER_NAME = "m23ozaki"
PASSWORD = "trumpet117"
TEST_URL = "https://yahoo.com/"

# HTTPS用
ssl._create_default_https_context = ssl._create_unverified_context

for i in range(10):  # これ以上待ってもだめならなんかおかしい
    try:
        # リダイレクト先のURLとクエリパラメータを取得 (ホントはリダイレクトはされてない)
        with urllib.request.urlopen(TEST_URL) as response:
            # 認証前ならなんか変だけど ↓ される
            # window.location="https://captive4.tokuyama.ac.jp:1003/fgtauth?0502d9c9db86581d"
            body = response.read().decode()
    except:  # 例外が起きたら
        sleep(1)
    else:  # 例外が起きなかったら
        if "tokuyama.ac.jp" in body:
            break
        else:
            if "Darwin" == system():  # Macだけstdoutにlogを吐く
                import datetime
                print(f"already authenticated {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
            exit(0)

# パースしてURL取得
redirect_URL = ""
for line in body.split("\""):
    if "https://captive4.tokuyama.ac.jp" in line:
        # ex. https://captive4.tokuyama.ac.jp:1003/fgtauth?0502d9c9db86581d
        redirect_URL = line

# ex. 0104ca641fdaa162
parameter_Magic = redirect_URL[redirect_URL.find("?") + 1:]  # クエリパラメータ取得
print(redirect_URL)
print(parameter_Magic)

# 一回アクセスしないと認証ページを作成しないようだ. ここえらいハマった.
# そのままPOSTの処理をすると curl: (52) Empty reply from server
with urllib.request.urlopen(redirect_URL, timeout=1) as response:
    body = response.read().decode()

# POSTの処理
values = {'username': USER_NAME, 'password': PASSWORD, '4Tredir': TEST_URL, 'magic': parameter_Magic}
data = urllib.parse.urlencode(values)
data = data.encode('utf-8')  # data should be bytes
req = urllib.request.Request(url=redirect_URL, data=data)
with urllib.request.urlopen(req) as response:
    print(f"status code: {response.geturl()}")

# Raspi?
# 時計合わせ. やらないとaptが使えない可能性あり.
if "raspberrypi" == gethostname():
    from subprocess import run
    run(["systemctl", "restart", "systemd-timesyncd.service"])

# Macだけstdoutにlogを吐く
if "Darwin" == system():
    import datetime
    print(f"Authentication succeeded {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")