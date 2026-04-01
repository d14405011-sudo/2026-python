# -*- coding: utf-8 -*-
"""
大老二遊戲 - 主程式
支持命令行參數和GUI啟動 
"""
__version__ = "2.0.0"

import sys
import os
import locale

# ═══════════════════════════════════════════════════════
# 1. 設定編碼（Windows 中文支持）
# ═══════════════════════════════════════════════════════
def _setup_encoding():
    """自動偵測並設置系統語系編碼"""
    if sys.platform == 'win32':
        import io
        
        # 嘗試檢測系統語言
        try:
            system_locale = locale.getdefaultlocale()[0]
            is_taiwan = system_locale and ('zh_TW' in system_locale or 'Taiwan' in system_locale)
        except:
            is_taiwan = False

        def _reconfigure_or_wrap(stream):
            if stream is None:
                return open(os.devnull, 'w', encoding='utf-8')
            if hasattr(stream, 'reconfigure'):
                try:
                    stream.reconfigure(encoding='utf-8')
                    return stream
                except Exception:
                    pass
            buffer = getattr(stream, 'buffer', None)
            if buffer is None:
                return open(os.devnull, 'w', encoding='utf-8')
            try:
                return io.TextIOWrapper(buffer, encoding='utf-8')
            except Exception:
                return open(os.devnull, 'w', encoding='utf-8')

        # 設置 sys.stdout 和 sys.stderr 為 UTF-8
        sys.stdout = _reconfigure_or_wrap(sys.stdout)
        sys.stderr = _reconfigure_or_wrap(sys.stderr)
        
        # 設置環境變數以確保 Python 子進程也使用 UTF-8
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        if is_taiwan:
            print("[INFO] 偵測到繁體中文環境，已啟用 UTF-8 編碼支持")

_setup_encoding()

# ═══════════════════════════════════════════════════════
# 2. 設定 Python 路徑（避免重複搜尋）
# ═══════════════════════════════════════════════════════
_GAME_ROOT = os.path.dirname(os.path.abspath(__file__))
if _GAME_ROOT not in sys.path:
    sys.path.insert(0, _GAME_ROOT)

# ═══════════════════════════════════════════════════════
# 3. 依賴檢查與遊戲啟動
# ═══════════════════════════════════════════════════════
def main():
    """遊戲主進入點"""
    print(f"大老二遊戲 v{__version__} 啟動中...")
    
    # 檢查必要的依賴
    try:
        import pygame
        if not hasattr(pygame, '__version__'):
            raise ImportError("pygame 版本檢測失敗")
    except ImportError:
        print("[ERROR] 缺少 pygame 模組")
        print("請執行：pip install pygame-ce")
        return 1
    
    try:
        # 載入遊戲 UI
        from ui.app import BigTwoApp
        
        # 初始化遊戲應用
        app = BigTwoApp()
        
        # 運行遊戲循環
        app.run()
        
    except ImportError as e:
        print(f"[ERROR] 缺少必要的模組")
        print(f"詳情：{e}")
        print()
        print("解決方案：")
        print("1. 確認虛擬環境已激活")
        print("2. 運行：pip install -r requirements.txt")
        print("3. 或：pip install pygame-ce")
        return 1
    except pygame.error as e:
        print(f"[ERROR] pygame 初始化失敗：{e}")
        print()
        print("解決方案：")
        print("1. 檢查顯示卡驅動是否正常")
        print("2. 嘗試更新或重裝 pygame-ce")
        print("3. 確保系統有足夠的 GPU 內存")
        return 1
    except Exception as e:
        print(f"[ERROR] 遊戲啟動失敗：{e}")
        print()
        import traceback
        print("詳細錯誤信息：")
        traceback.print_exc()
        return 1
    
    return 0

# ═══════════════════════════════════════════════════════
if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

