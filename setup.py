import getpass
import platform
import os
import subprocess
from shutil import move

# ディレクトリの移動
os.chdir(os.path.dirname(__file__))

print("TCT_Auto Authentication のインストールを開始します.")
USER_NAME = input("学校での Web認証時のユーザー名 を入力してください.\nex. m23ozaki\n>> ")
print()
while True:
    PASSWORD = getpass.getpass("パスワードを入力してください\n>> ")
    print()
    PASSWORD1 = getpass.getpass("確認のため,もう一度パスワードを入力してください\n>> ")
    if PASSWORD1 == PASSWORD:
        break
    else:
        print("パスワードが一致しません")

with open("auto_auth.py", 'r', encoding='utf-8') as f:
    text = f.read()

FILE_NAME = "auto_auth_cp.py"
with open(FILE_NAME, 'w+', encoding='utf-8') as f:
    body = text.replace("m23ozaki", USER_NAME).replace("trumpet117", PASSWORD)
    f.write(body)

OSINFO = platform.system()  # OS判定
HOME = os.path.expanduser("~")  # ホームディレクトリのパス取得

# auto_auth.py のインストールディレクトリ設定
if OSINFO == "Windows":
    if " " in HOME:
        print("\nダウンロードしたフォルダのPATHに 空白 が含まれています.")
        print("出直してきやがれ (別のところにダウンロードしてね♥)")
        exit(0)
    INSTALL_PATH = HOME + "\\local\\bin\\"
    os.makedirs(INSTALL_PATH, exist_ok=True)
else:
    # /usr/local/bin にはPATHが通ってるはず
    INSTALL_PATH = "/usr/local/bin/"

# auto_auth.py のコピー
print(f"auto_auth.py コピー先: {INSTALL_PATH}")
if OSINFO == "Windows":
    targetPATH = INSTALL_PATH + "auto_auth.py" + "w"
    move(FILE_NAME, targetPATH)
else:
    print("\n以降パスワードを聞かれたら,【自分のパソコンの】パスワードを入力してください.")
    subprocess.run(["sudo", "mv", FILE_NAME, INSTALL_PATH + "auto_auth.py"])
    subprocess.run(["sudo", "chmod", "+x", INSTALL_PATH + "auto_auth.py"])

#################### 自動起動設定 ########################

# Windows: タスクスケジューラの設定
if OSINFO == "Windows":
    from socket import gethostname
    # ホスト名取得
    HOSTNAME = gethostname()

    # 現在のユーザーのSIDを取得
    cmd = f'wmic useraccount where name="{getpass.getuser()}" get sid'
    output_str = subprocess.run(cmd, capture_output=True, text=True).stdout
    SID = output_str.replace("SID", "").replace(" ", "").replace("\n", "")

    with open(".\\win\\auto_auth.xml", 'r', encoding='utf-16-le') as f:
        text = f.read()

    with open(".\\win\\auto_auth_cp.xml", 'w+', encoding='utf-16-le') as f:
        body = text.replace("<Author></Author>", f"<Author>{HOSTNAME}</Author>")
        body = body.replace("<UserId></UserId>", f"<UserId>{SID}</UserId>")
        body = body.replace("<Command></Command>", f"<Command>{targetPATH}</Command>")
        f.write(body)
    # プリインストールの PowerShell
    PATH_TO_POWERSHELL = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    # subprocessはPowerShellで実行
    os.environ['COMSPEC'] = PATH_TO_POWERSHELL

    # 管理者で schtasks の実行
    path_to_XML = os.path.dirname(__file__) + "\\win\\auto_auth_cp.xml"
    cmd = [
        "Start-Process",
        "schtasks.exe",
        "-Verb",
        "RunAs",
        "-ArgumentList",
        f'"/Create /TN TCT_AutoAuth /XML {path_to_XML}"'  # 新しくプロセス起動してるので絶対パス
    ]
    subprocess.run(cmd, shell=True)

# MacOS: launchdの設定
if OSINFO == "Darwin":
    cmds = [
        ["sudo", "chown", "root", "./mac/auto_auth.plist"],
        ["sudo", "chmod", "+x", "./mac/auto_auth.plist"],
        ["sudo", "cp", "./mac/auto_auth.plist", "/Library/LaunchDaemons/"],
        ["sudo", "launchctl", "load", "/Library/LaunchDaemons/auto_auth.plist"],
    ]
    for cmd in cmds:
        subprocess.run(cmd)
    print("Pythonにフルディスクアクセス権限を与えてください.")
    print("")

# Linux: NetworkManagerがある場合 (Ubuntuとかの場合は事前に入れてくれ)
# 起動スクリプトのコピー
DISPATH = "/etc/NetworkManager/dispatcher.d/"
SCRIPT_NAME = "./linux/auto_auth"
if (OSINFO != "Windows") and (OSINFO != "Darwin"):
    if os.path.exists(DISPATH):  # フォルダチェック
        subprocess.run(["sudo", "chmod", "+x", SCRIPT_NAME])
        subprocess.run(["sudo", "cp", SCRIPT_NAME, DISPATH])
        print(f"auto_authコピー先: {DISPATH}")
    else:
        print("NetworkManagerがインストールされていません.\nプログラムを終了します.")
        exit(1)

print("インストールが正常に終了しました")
