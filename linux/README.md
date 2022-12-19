## auto start settings

[NetworkManager](https://networkmanager.dev/docs/)が入ってるのを前提に,

- ログの監視を行って
- イベントが起きたときに
- `auto_auth.py` を起動

してます.

[NetworkManagerの設定で具体的なことがわからなかったら, ここをみる](https://arduinobook.stradty.com/accounts/Appendix1-1/#%E5%AD%A6%E6%A0%A1%E3%81%AEwi-fi%E3%81%AB%E6%8E%A5%E7%B6%9A%E3%81%97%E3%81%A6raspi%E3%82%92%E4%BD%BF%E3%81%86%E5%A0%B4%E5%90%88).

具体的には, [NetworkManager-dispatcher](https://man.archlinux.org/man/NetworkManager-dispatcher.8.en) からスクリプトで `auto_auth.py` を起動します.

ちなみに, `connectivity-change` はもちろん起動時にも効きます. (ネットワーク参加時に効くから)

```bash
# ログ. とうか man journalctl すれ.
$ journalctl -u NetworkManager-dispatcher.service -e
```


