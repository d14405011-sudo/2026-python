# -*- coding: utf-8 -*-
# ui/sound.py
"""
音效管理系統
預留架構用於遊戲音效播放

支援功能：
- 遊戲音效：出牌聲、過牌聲、獲勝音樂
- 音量控制
- 音效啟用/禁用切換
"""

import pygame
from pathlib import Path
from typing import Optional, Dict


class SoundManager:
    """遊戲音效管理器
    
    統一管理所有遊戲音效資源和播放邏輯
    """
    
    # 音效資源目錄
    SOUNDS_DIR = Path(__file__).parent.parent / "assets" / "sounds"
    
    # 預設音效檔案清單
    SOUND_FILES = {
        'play_card': 'play_card.wav',           # 出牌聲
        'pass_turn': 'pass_turn.wav',           # 過牌聲
        'win_game': 'win_game.wav',             # 獲勝音樂
        'turn_start': 'turn_start.wav',         # 輪次開始
        'round_over': 'round_over.wav',         # 輪次結束
        'card_flip': 'card_flip.wav',           # 翻牌聲
        'countdown': 'countdown.wav',           # 倒計時警告
    }
    
    def __init__(self, enabled: bool = True, volume: float = 0.7):
        """初始化音效管理器
        
        Args:
            enabled: 音效是否啟用
            volume: 全局音量 (0.0 - 1.0)
        """
        self.enabled = enabled
        self.volume = max(0.0, min(1.0, volume))
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self._load_sounds()
    
    def _ensure_mixer(self) -> bool:
        """確保 pygame mixer 已初始化"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return True
        except Exception:
            return False
    
    def _load_sounds(self) -> None:
        """預加載所有可用的音效檔案
        
        如果音效檔案不存在，會記錄為 None，但不會中斷遊戲
        """
        if not self._ensure_mixer():
            return
        
        # 確保音效目錄存在
        if not self.SOUNDS_DIR.exists():
            self.SOUNDS_DIR.mkdir(parents=True, exist_ok=True)
        
        for sound_key, sound_file in self.SOUND_FILES.items():
            sound_path = self.SOUNDS_DIR / sound_file
            try:
                if sound_path.exists():
                    self.sounds[sound_key] = pygame.mixer.Sound(str(sound_path))
                    self.sounds[sound_key].set_volume(self.volume)
                else:
                    self.sounds[sound_key] = None
                    # 可選：記錄日誌
                    # print(f"[WARNING] 音效檔案未找到: {sound_path}")
            except Exception:
                self.sounds[sound_key] = None
                # 可選：記錄日誌
                # print(f"[ERROR] 無法加載音效: {sound_path}")
    
    def play(self, sound_key: str, loops: int = 0, max_time: int = 0) -> None:
        """播放指定的音效
        
        Args:
            sound_key: 音效關鍵字 (如 'play_card', 'pass_turn', 'win_game')
            loops: 重複次數 (0 = 播放一次, -1 = 無限迴圈)
            max_time: 最大播放時間 (毫秒，0 = 無限制)
        """
        if not self.enabled or not self._ensure_mixer():
            return
        
        sound = self.sounds.get(sound_key)
        if sound is None:
            return
        
        try:
            sound.play(loops=loops, maxtime=max_time)
        except Exception:
            pass
    
    def stop(self, sound_key: Optional[str] = None) -> None:
        """停止指定的音效，或停止所有播放
        
        Args:
            sound_key: 音效關鍵字。若為 None，停止所有音效
        """
        if not self._ensure_mixer():
            return
        
        if sound_key is None:
            pygame.mixer.stop()
        else:
            sound = self.sounds.get(sound_key)
            if sound is not None:
                sound.stop()
    
    def set_volume(self, volume: float) -> None:
        """設定全局音量
        
        Args:
            volume: 音量 (0.0 - 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.volume)
    
    def set_enabled(self, enabled: bool) -> None:
        """啟用或禁用音效
        
        Args:
            enabled: True = 啟用，False = 禁用
        """
        self.enabled = enabled
        if not enabled:
            self.stop()
    
    def toggle(self) -> bool:
        """切換音效啟用狀態
        
        Returns:
            新的啟用狀態
        """
        self.set_enabled(not self.enabled)
        return self.enabled
    
    # ═══════════════════════════════════════════════════════
    # 遊戲事件快捷方法
    # ═══════════════════════════════════════════════════════
    
    def on_play_card(self) -> None:
        """玩家出牌時播放聲音"""
        self.play('play_card')
    
    def on_pass_turn(self) -> None:
        """玩家過牌時播放聲音"""
        self.play('pass_turn')
    
    def on_win_game(self) -> None:
        """獲勝時播放音樂"""
        self.play('win_game')
    
    def on_round_over(self) -> None:
        """輪次結束時播放聲音"""
        self.play('round_over')
    
    def on_turn_start(self) -> None:
        """輪次開始時播放聲音"""
        self.play('turn_start')
    
    def on_card_flip(self) -> None:
        """翻牌時播放聲音"""
        self.play('card_flip')
    
    def on_countdown_warning(self) -> None:
        """倒計時警告時播放聲音"""
        self.play('countdown')


# 全局音效管理器實例
_sound_manager = None


def get_sound_manager() -> SoundManager:
    """取得全局音效管理器實例"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager


def init_sound_manager(enabled: bool = True, volume: float = 0.7) -> SoundManager:
    """初始化並取得音效管理器"""
    global _sound_manager
    _sound_manager = SoundManager(enabled=enabled, volume=volume)
    return _sound_manager
