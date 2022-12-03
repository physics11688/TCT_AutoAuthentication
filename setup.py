import platform
import os
import subprocess
from shutil import copy, move

os.chdir(os.path.dirname(__file__))

print("TCT_Auto Authentication のインストールを開始sます.")
USER_NAME = input("Web認証時のユーザー名を入力してください.\nex. m23ozaki\n>> ")
PASSWORD = input("パスワードを入力してください\n>> ")

FILE_NAME = "auto_auth.py"
with open(FILE_NAME, 'r', encoding='utf-8') as f:
    text = f.read()

with open(FILE_NAME, 'w', encoding='utf-8') as f:
    body = text.replace("m23ozaki", USER_NAME).replace("trumpet117", PASSWORD)
    f.write(body)

OSINFO = platform.system()  # OS判定
HOME = os.path.expanduser("~")  # ホームディレクトリのパス取得

# インストールディレクトリ設定
if OSINFO == "Windows":
    INSTALL_PATH = HOME + "\\local\\bin\\"
    os.makedirs(INSTALL_PATH, exist_ok=True)
else:
    # /usr/local/bin にはPATHが通ってるはず
    INSTALL_PATH = "/usr/local/bin/"

# pythonファイルのコピー
print(f"auto_auth.py コピー先: {INSTALL_PATH}")
if OSINFO == "Windows":
    copy(FILE_NAME, INSTALL_PATH + FILE_NAME + "w")
else:
    subprocess.run(["sudo", "cp", FILE_NAME, INSTALL_PATH])
    subprocess.run(["sudo", "chmod", "+x", INSTALL_PATH + FILE_NAME])

# NetworkManagerがある場合 (Ubuntuとかの場合は事前に入れてくれ)
# 起動スクリプトのコピー
DISPATH = "/etc/NetworkManager/dispatcher.d/"
SCRIPT_NAME = "auto_auth"
if os.path.exists(DISPATH):
    subprocess.run(["sudo", "cp", SCRIPT_NAME, DISPATH])
    subprocess.run(["sudo", "chmod", "+x", DISPATH + SCRIPT_NAME])
    print(f"auto_authコピー先: {DISPATH}")

print("インストールが正常に終了しました")
