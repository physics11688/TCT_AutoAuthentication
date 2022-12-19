## auto start settings

`setup.py`で [launchd](https://www.launchd.info/) を設定してあります。

- ネットワーク参加時
- ログイン時

とかに `auto_auth.py` を実行します。

<br>

```bash
# ログ
% ls /tmp/auto_aut*

# ログ見る
% cat /tmp/auto_auth.out
already authenticated 2022年12月05日 21:13:00  # みたいになる

# plist
% sudo cat /Library/LaunchDaemons/auto_auth.plist

# 情報見れる
% sudo launchctl list TCT.auto_authentication 

# 詳細
% sudo launchctl print system/TCT.auto_authentication
```