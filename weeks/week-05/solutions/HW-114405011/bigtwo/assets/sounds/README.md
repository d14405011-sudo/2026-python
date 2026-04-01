# 遊戲音效資源目錄

本目錄用於存放大老二遊戲的所有音效檔案。

## 預期音效檔案清單

根據 `ui/sound.py` 的 `SoundManager`，以下音效檔案應放在此目錄：

| 檔案名稱 | 說明 | 建議格式 |
|---------|------|--------|
| `play_card.wav` | 玩家出牌時播放 | WAV/MP3 (0.3-0.8秒) |
| `pass_turn.wav` | 玩家過牌時播放 | WAV/MP3 (0.2-0.5秒) |
| `win_game.wav` | 遊戲獲勝時播放 | WAV/MP3 (1-3秒) |
| `turn_start.wav` | 輪次開始時播放 | WAV/MP3 (0.2-0.5秒) |
| `round_over.wav` | 輪次結束時播放 | WAV/MP3 (0.5-1.5秒) |
| `card_flip.wav` | 翻牌時播放 | WAV/MP3 (0.1-0.3秒) |
| `countdown.wav` | 倒計時警告時播放 | WAV/MP3 (0.2-0.5秒) |

## 使用方式

### 在遊戲中播放音效

```python
from ui.sound import get_sound_manager

sound_manager = get_sound_manager()

# 出牌時
sound_manager.on_play_card()

# 過牌時
sound_manager.on_pass_turn()

# 獲勝時
sound_manager.on_win_game()
```

### 控制音量

```python
# 設定全局音量 (0.0 - 1.0)
sound_manager.set_volume(0.8)

# 啟用/禁用音效
sound_manager.set_enabled(True)

# 切換音效狀態
is_enabled = sound_manager.toggle()
```

## 音效整合點

- **出牌事件** (`on_play_card`) - 在 `BigTwoApp.play()` 時調用
- **過牌事件** (`on_pass_turn`) - 在玩家選擇過牌時調用
- **獲勝事件** (`on_win_game`) - 在遊戲結束宣布獲勝者時調用
- **輪次管理** - 可在輪次開始/結束時調用相應方法

## 技術細節

- 音效系統基於 `pygame.mixer`
- 所有音效檔案會在 `SoundManager` 初始化時預加載
- 如果找不到音效檔案，遊戲會繼續正常運作（不會崩潰）
- 支援同時播放多個音效

## 推薦工具

- **音效編輯** - Audacity (免費)
- **格式轉換** - FFmpeg, MediaInfo
- **搜尋免費音效** - Freesound.org, Zapsplat

---

**說明**: 未來若需新增音效，請更新 `SoundManager.SOUND_FILES` 字典並放置對應檔案於此目錄。
