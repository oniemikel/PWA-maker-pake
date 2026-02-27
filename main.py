import os
import subprocess
import requests
from pathlib import Path


def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default


def download_icon(url, save_path):
    # GoogleのS2サービスを利用して、URLから最高精度のアイコン(128px)を抽出
    icon_url = f"https://www.google.com/s2/favicons?domain={url}&sz=128"
    print(f"🎨 アイコンを自動取得中: {icon_url}")
    try:
        response = requests.get(icon_url, timeout=10)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"⚠️ アイコン取得失敗: {e}")
        return False


def run_build():
    print("=== 🚀 Pake MSI Maker: Auto-Icon & Internal-Login ===")

    url = get_input("URL", "http://example.com/")
    app_name = get_input("App Name", "Example")

    downloads_dir = Path(os.path.expanduser("~")) / "Downloads"
    icon_path = downloads_dir / f"{app_name}_icon.png"

    # 1. アイコンを自動取得して保存
    has_icon = download_icon(url, icon_path)

    # 2. Chrome偽装UA
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    # 3. コマンド構成
    # --new-window を外すことで、ログイン画面を別窓で開かせない
    cmd = [
        "pake",url,
        "--name",app_name,
        "--user-agent",ua,
        "--enable-drag-drop",
        "--multi-instance",
        "--show-system-tray",
        "--force-internal-navigation",
        "--wasm",
        "--targets",
        "x64",
    ]

    if has_icon:
        cmd.extend(["--icon", str(icon_path)])

    print(f"\n🛠️ {app_name} をビルド中...")

    try:
        # MSI生成のために実行（iterative-buildは使用しない）
        subprocess.run(cmd, cwd=downloads_dir, shell=True, check=True)
        print(f"\n✅ 完了！Downloads フォルダを確認してください。")

        # アイコン用の一時ファイルを掃除
        if icon_path.exists():
            os.remove(icon_path)

    except Exception as e:
        print(f"❌ ビルドエラー: {e}")


if __name__ == "__main__":
    run_build()
