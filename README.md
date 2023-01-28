# TCT_AutoAuthentication
某高専のネットワーク自動認証です.

- auto_auth.py: 主にこいつで処理<br>
- auto_auth.[xml|plist]: プログラムの自動起動<br>
- パスワード変わったら再インストールする

#### 2023/1/28 追記
センターのページからMacアドレスで自動認証する登録が出来るようになったみたいです。


なので、セキュリティ上の理由でMacアドレスのランダム化をしたままで自動認証したい場合はこちらを使うと便利です。

<br>

## Requirements
Python3が入ってれば多分動きます.

メインファイルの `auto_auth.py` は, 標準ライブラリのみで記述してあります.

<br>

### Raspberry Pi の場合
Raspiは標準では WiFi接続に [dhcpcd](https://wiki.archlinux.jp/index.php/Dhcpcd) を使用してますが,

このままだとTCTのWiFiには接続出来ないのでNetworkManagerに切り替えてください。<br>
(初めからインストールだけはされている)

[具体的なことがわからなかったら,ここをみる](https://arduinobook.stradty.com/accounts/Appendix1-1/#%E5%AD%A6%E6%A0%A1%E3%81%AEwi-fi%E3%81%AB%E6%8E%A5%E7%B6%9A%E3%81%97%E3%81%A6raspi%E3%82%92%E4%BD%BF%E3%81%86%E5%A0%B4%E5%90%88).

<br>

## Install & Usage

ターミナルを開いて ↓ を実行.

<br>

```bash
# くろ～ん
> git clone git@github.com:physics11688/TCT_AutoAuthentication.git

# ↑が出来ない人は ssh とかを調べるとして, ↓ で入る
> git clone https://github.com/physics11688/TCT_AutoAuthentication.git

# 移動
> cd TCT_AutoAuthentication

# セットアップ (Windows)
> python setup.py

# セットアップ (UNIX系)
$ python3 setup.py

```

<br>

## Uninstall
```bash
# Windows
> python uninstall.py

# UNIX系
$ python3 uninstall.py
```

<br>

#### Macのみ
~~Macのみ追加で設定が必要です.~~

~~Pythonにフルディスクアクセスの権限が必要です.~~

~~使用してる最新のPythonにアクセス権を与えましょう.~~

必要なかった.

<br>

![mac](./pic/mac.png)

<br>


<br>

## Auto Start Settings
### Windows

`setup.py` では ↓ を実行してます.
XMLファイルのインポートです.

```powershell
> schtasks.exe /Create /TN TCT_AutoAuth /XML \win\auto_auth.xml
```


<br>

### Linux

NetworkManagerさえ入っていたら, `setup.py` で起動スクリプトを設置してます.

"connectivity-change events" のみ[チェックしてます](https://man.archlinux.org/man/NetworkManager-dispatcher.8.en).

```bash
$ cat /etc/NetworkManager/dispatcher.d/auto_auth
```



<br>

### Mac

`setup.py` で launchd用の起動スクリプトを設置してます.

```bash
# plist
% sudo cat /Library/LaunchDaemons/auto_auth.plist
```
