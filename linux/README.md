## auto start settings

NetworkManagerが入ってるのを前提に,

- ログの監視を行って
- イベントが起きたときに
- `auto_auth.py` を起動

してます.

具体的には, [NetworkManager-dispatcher](https://man.archlinux.org/man/NetworkManager-dispatcher.8.en) からスクリプトで `auto_auth.py` を起動します.

ちなみに, `connectivity-change` はもちろん起動時にも効きます. (ネットワーク参加時に効くから)