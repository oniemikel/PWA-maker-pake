import os
import subprocess
import glob
from pathlib import Path

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def run_build():
    print("=== 🚀 Pake MSI Maker (Internal Login Mode) ===")
    
    url = get_input("URL", "https://calendar.google.com/")
    app_name = get_input("App Name", "GoogleCalendar")
    
    # Chromeに偽装してGoogleログインをアプリ内で完結させる
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    downloads_dir = Path(os.path.expanduser("~")) / "Downloads"

    # --iterative-build を外して MSI を生成
    cmd = [
        "pake", url,
        "--name", app_name,
        "--user-agent", ua,
        "--new-window",
        "--enable-drag-drop",
        "--multi-instance",
        "--show-system-tray",
        "--force-internal-navigation",
        "--wasm",
        "--targets", "x64"
    ]

    print(f"\n🛠️ {app_name} の MSI インストーラーを鋳造中...")
    print("※ MSIのパッキング工程を含めるため、数分かかります。完了までお待ちください。")
    
    try:
        # ビルド実行
        process = subprocess.run(cmd, cwd=downloads_dir, shell=True)
        
        if process.returncode == 0:
            print(f"\n✅ ビルド成功！後片付けを開始します...")
            
            # .msi 以外の生成ファイル（.exe単体や中間ファイル）を削除する
            # PakeはDownloads直下にファイルを生成するため、msi以外を掃除
            all_files = glob.glob(str(downloads_dir / f"*{app_name}*"))
            for f in all_files:
                if not f.endswith(".msi"):
                    try:
                        if os.path.isfile(f):
                            os.remove(f)
                        elif os.path.isdir(f):
                            import shutil
                            shutil.rmtree(f)
                    except Exception as e:
                        print(f"掃除失敗: {f} ({e})")
            
            print(f"✨ Downloads フォルダに '{app_name}' の MSI だけを残しました。")
        else:
            print(f"\n❌ ビルドに失敗しました。")
            
    except Exception as e:
        print(f"実行エラー: {e}")

if __name__ == "__main__":
    run_build()