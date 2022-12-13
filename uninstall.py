import platform
import os
import re
import subprocess


def YorN() -> bool:
    user_input = input("Yes or No >> ")

    Yes = re.search(r"/yes/i", user_input)
    Y = re.search(r"[Yy]", user_input)
    if Yes is Y is None:
        return False
    else:
        return True


# ディレクトリの移動
os.chdir(os.path.dirname(__file__))

print("TCT_Auto Authentication をアンインストールしますか?")
if not YorN():
    print("プログラムを終了します")
    exit(1)

OSINFO = platform.system()  # OS判定
HOME = os.path.expanduser("~")  # ホームディレクトリのパス取得

# auto_auth.py のインストールディレクトリ設定
if OSINFO == "Windows":
    if " " in HOME:
        print("\nダウンロードしたフォルダのPATHに 空白 が含まれています.")
        print("出直してきやがれ (別のところにダウンロードしてね♥)")
        exit(0)
    INSTALL_PATH = HOME + "\\local\\bin\\auto_auth.pyw"
else:
    INSTALL_PATH = "/usr/local/bin/auto_auth.py"

if os.path.isfile(INSTALL_PATH):
    if OSINFO == "Windows":
        os.remove(INSTALL_PATH)
    else:
        subprocess.run(["sudo", "rm", INSTALL_PATH])

print(INSTALL_PATH + " を削除しました.")

# ----------------- 自動起動設定の削除 ----------------- #

# Windows: タスクスケジューラの設定
if OSINFO == "Windows":
    # プリインストールの PowerShell
    PATH_TO_POWERSHELL = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    # subprocessはPowerShellで実行
    os.environ['COMSPEC'] = PATH_TO_POWERSHELL

    # 管理者で schtasks の実行
    cmd = ["Start-Process", "schtasks.exe", "-Verb", "RunAs", "-ArgumentList", '"/Delete /TN TCT_AutoAuth"']
    subprocess.run(cmd, shell=True)
    print("タスク: TCT_AutoAuth を削除しました")

# MacOS: launchdの設定
if OSINFO == "Darwin":
    cmds = [["sudo", "launchctl", "unload", "/Library/LaunchDaemons/auto_auth.plist"],
            ["sudo", "rm", "/Library/LaunchDaemons/auto_auth.plist"]]
    for cmd in cmds:
        subprocess.run(cmd)
    print("デーモン: auto_auth を削除しました")

# NetworkManager/dispatcher.d
INSTALL_PATH = "/etc/NetworkManager/dispatcher.d/auto_auth"
if (OSINFO != "Windows") and (OSINFO != "Darwin"):
    if os.path.exists(INSTALL_PATH):  # ファイルチェック
        subprocess.run(["sudo", "rm", INSTALL_PATH])

print("アンインストールが正常に終了しました")
