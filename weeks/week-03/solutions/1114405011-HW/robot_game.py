"""pygame UI for Robot Lost homework.

Controls:
- L / R / F: apply one instruction
- N: spawn a new robot at (0, 0, N) and keep scents
- C: clear all scents
- P: replay latest robot path
- G: export replay.gif from current track
- S: save gameplay screenshot to assets/gameplay.png
- T: save a smaller PNG to assets/gameplay_small.png
- M: export 10x10 matrix snapshot to assets/matrix_snapshot.txt
- Mouse Left: zoom in
- Mouse Right: zoom out
- ESC: quit
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from math import sin
from pathlib import Path
from typing import List, Set, Tuple

import pygame

from robot_core import RobotState, Scent, execute_instruction


WIDTH = 5
HEIGHT = 3
CELL = 88
HEADER_HEIGHT = 92
BOTTOM_PANEL_HEIGHT = 248
PADDING = 30
GAP = 24
MATRIX_SIZE = 10
SIDE_PANEL_WIDTH = 460
BOARD_W = CELL * (WIDTH + 1)
BOARD_H = CELL * (HEIGHT + 1)
BOARD_LEFT = PADDING
BOARD_TOP = PADDING + HEADER_HEIGHT + 12
SIDE_LEFT = BOARD_LEFT + BOARD_W + GAP
SCREEN_W = PADDING * 2 + BOARD_W + GAP + SIDE_PANEL_WIDTH
SCREEN_H = BOARD_TOP + BOARD_H + GAP + BOTTOM_PANEL_HEIGHT + PADDING
FPS = 60
GIF_EXPORT_SCALE = 0.72
PNG_THUMB_SCALE = 0.5
ZOOM_MIN = 0.7
ZOOM_MAX = 2.0
ZOOM_STEP = 0.1

BG = (7, 16, 34)
TEXT = (234, 241, 255)
MUTED = (192, 210, 234)
GRID = (73, 107, 150)
GRID_GLOW = (93, 151, 220)
ROBOT = (115, 226, 255)
ROBOT_LOST = (255, 122, 122)
SCENT = (255, 192, 109)
PANEL = (13, 25, 49)
PANEL_ALT = (18, 33, 62)
PANEL_EDGE = (53, 88, 138)
ACCENT = (169, 204, 255)
STAR = (206, 229, 255)
NEBULA_A = (34, 71, 124)
NEBULA_B = (91, 56, 120)
TRAIL = (98, 160, 224)
GOOD = (131, 223, 184)


@dataclass
class ReplayState:
    x: int
    y: int
    direction: str
    lost: bool


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Robot Lost: Starfall Route")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
        self.canvas = pygame.Surface((SCREEN_W, SCREEN_H))
        self.draw_surface = self.canvas
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("microsoftjhenghei", 34, bold=True)
        self.section_font = pygame.font.SysFont("microsoftjhenghei", 23, bold=True)
        self.font = pygame.font.SysFont("microsoftjhenghei", 20)
        self.small_font = pygame.font.SysFont("microsoftjhenghei", 16)
        self.mono_font = pygame.font.SysFont("consolas", 16)

        self.scents: Set[Scent] = set()
        self.robot = RobotState(0, 0, "N", False)
        self.status = "就緒"
        self.command_history: List[str] = []
        self.event_log: List[str] = ["任務啟動，等待第一個指令"]
        self.event_log_scroll: int = 0

        self.current_track: List[ReplayState] = [
            ReplayState(self.robot.x, self.robot.y, self.robot.direction, self.robot.lost)
        ]
        self.replay_mode = False
        self.replay_index = 0
        self.replay_timer = 0.0
        self.zoom = 1.0
        self.animation_time = 0.0

        self.star_field = [
            (68, 56, 2),
            (138, 132, 1),
            (216, 74, 2),
            (290, 120, 1),
            (348, 58, 2),
            (480, 102, 1),
            (556, 72, 2),
            (752, 116, 2),
            (864, 74, 1),
            (932, 160, 2),
            (1016, 68, 1),
            (1090, 124, 2),
            (92, 222, 1),
            (188, 248, 2),
            (272, 194, 1),
            (624, 226, 2),
            (718, 256, 1),
            (866, 216, 2),
            (1038, 238, 1),
            (1112, 286, 2),
            (76, 418, 1),
            (194, 470, 2),
            (310, 452, 1),
            (408, 394, 2),
            (722, 422, 1),
            (802, 372, 2),
            (916, 466, 1),
            (1026, 420, 2),
            (1096, 382, 1),
            (118, 620, 2),
            (232, 676, 1),
            (366, 640, 2),
            (694, 642, 1),
            (810, 694, 2),
            (980, 666, 1),
            (1086, 628, 2),
        ]
        self.constellations = [
            [(64, 76), (126, 52), (182, 92), (214, 54)],
            [(888, 108), (938, 72), (992, 118), (1034, 86), (1092, 140)],
            [(968, 524), (1032, 484), (1088, 526), (1106, 592), (1040, 612)],
        ]

    def set_status(self, message: str) -> None:
        self.status = message
        self.event_log.append(message)
        self.event_log = self.event_log[-25:]
        self.event_log_scroll = 0  # reset to bottom on new event

    def reset_robot(self) -> None:
        self.robot = RobotState(0, 0, "N", False)
        self.command_history.clear()
        self.current_track = [ReplayState(0, 0, "N", False)]
        self.replay_mode = False
        self.replay_index = 0
        self.replay_timer = 0.0
        self.set_status("已部署新機器人，保留既有 scent")

    def clear_scents(self) -> None:
        self.scents.clear()
        self.set_status("已清除所有 scent，邊界重新恢復危險")

    def apply_command(self, cmd: str) -> None:
        step = execute_instruction(self.robot, cmd, WIDTH, HEIGHT, self.scents)
        self.robot = step.state
        self.command_history.append(cmd)
        self.command_history = self.command_history[-14:]
        self.current_track.append(
            ReplayState(self.robot.x, self.robot.y, self.robot.direction, self.robot.lost)
        )
        event_text = {
            "TURN": "轉向",
            "MOVE": "前進",
            "SCENT_BLOCK": "scent 保護，忽略危險前進",
            "LOST": "掉落 LOST",
            "NOOP_LOST": "已 LOST，忽略指令",
        }
        self.set_status(f"{cmd} -> {event_text.get(step.event, step.event)}")

    def replay_tick(self, dt: float) -> None:
        self.animation_time += dt
        if not self.replay_mode or not self.current_track:
            return

        self.replay_timer += dt
        if self.replay_timer >= 0.4:
            self.replay_timer = 0.0
            self.replay_index += 1
            if self.replay_index >= len(self.current_track):
                self.replay_index = 0

    def get_display_robot(self) -> ReplayState:
        if self.replay_mode and self.current_track:
            return self.current_track[self.replay_index]
        return ReplayState(self.robot.x, self.robot.y, self.robot.direction, self.robot.lost)

    def map_to_screen(self, gx: int, gy: int) -> Tuple[int, int]:
        sx = BOARD_LEFT + gx * CELL
        sy = BOARD_TOP + (HEIGHT - gy) * CELL
        return sx, sy

    def build_matrix_10x10(self, display_robot: ReplayState) -> List[str]:
        matrix = [["." for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

        for x, y, _direction in self.scents:
            if 0 <= x < MATRIX_SIZE and 0 <= y < MATRIX_SIZE:
                matrix[MATRIX_SIZE - 1 - y][x] = "*"

        if 0 <= display_robot.x < MATRIX_SIZE and 0 <= display_robot.y < MATRIX_SIZE:
            marker = {
                "N": "^",
                "E": ">",
                "S": "v",
                "W": "<",
            }[display_robot.direction]
            if display_robot.lost:
                marker = "X"
            matrix[MATRIX_SIZE - 1 - display_robot.y][display_robot.x] = marker

        return ["".join(row) for row in matrix]

    def export_matrix_snapshot(self, display_robot: ReplayState) -> None:
        output_path = Path(__file__).resolve().parent / "assets" / "matrix_snapshot.txt"
        lines = self.build_matrix_10x10(display_robot)

        content_lines = [
            "10x10 Matrix Snapshot",
            f"Robot=({display_robot.x},{display_robot.y},{display_robot.direction}) lost={display_robot.lost}",
            f"Scents={sorted(self.scents)}",
            "",
        ]
        content_lines.extend(lines)
        output_path.write_text("\n".join(content_lines), encoding="utf-8")
        self.set_status(f"已輸出矩陣快照: {output_path.name}")

    def export_replay_gif(self) -> None:
        if len(self.current_track) < 2:
            self.set_status("沒有足夠軌跡可輸出 GIF")
            return

        try:
            from PIL import Image
        except ImportError:
            self.set_status("缺少 Pillow，請安裝: pip install pillow")
            return

        frames = []
        for frame_robot in self.current_track:
            self.render_scene(frame_robot, mode_override="匯出")
            rgb = pygame.image.tostring(self.canvas, "RGB")
            frame = Image.frombytes("RGB", (SCREEN_W, SCREEN_H), rgb)

            # Downscale and quantize for better compatibility across GIF viewers.
            export_size = (
                max(1, int(SCREEN_W * GIF_EXPORT_SCALE)),
                max(1, int(SCREEN_H * GIF_EXPORT_SCALE)),
            )
            frame = frame.resize(export_size, Image.Resampling.LANCZOS)
            frame = frame.convert("P", palette=Image.ADAPTIVE, colors=255)
            frames.append(frame)

        output_path = Path(__file__).resolve().parent / "assets" / "replay.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=[220] + [260] * (len(frames) - 1),
            loop=0,
            optimize=True,
            disposal=2,
        )
        self.set_status(f"已輸出 GIF: {output_path.name}")

    def save_gameplay_screenshot(self) -> None:
        output_path = Path(__file__).resolve().parent / "assets" / "gameplay.png"
        pygame.image.save(self.canvas, str(output_path))
        self.set_status(f"已儲存截圖: {output_path.name}")

    def save_small_gameplay_screenshot(self) -> None:
        output_path = Path(__file__).resolve().parent / "assets" / "gameplay_small.png"
        w = max(1, int(SCREEN_W * PNG_THUMB_SCALE))
        h = max(1, int(SCREEN_H * PNG_THUMB_SCALE))
        scaled = pygame.transform.smoothscale(self.canvas, (w, h))
        pygame.image.save(scaled, str(output_path))
        self.set_status(f"已儲存縮圖: {output_path.name} ({w}x{h})")

    def zoom_in(self) -> None:
        self.zoom = min(ZOOM_MAX, round(self.zoom + ZOOM_STEP, 2))
        self.set_status(f"畫面縮放: {self.zoom:.1f}x")

    def zoom_out(self) -> None:
        self.zoom = max(ZOOM_MIN, round(self.zoom - ZOOM_STEP, 2))
        self.set_status(f"畫面縮放: {self.zoom:.1f}x")

    def draw_background(self) -> None:
        top = (5, 13, 29)
        bottom = (16, 28, 56)
        for y in range(SCREEN_H):
            t = y / max(1, SCREEN_H - 1)
            color = (
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            )
            pygame.draw.line(self.draw_surface, color, (0, y), (SCREEN_W, y))

        for offset in range(10):
            alpha = max(10, 54 - offset * 5)
            nebula = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            pygame.draw.ellipse(
                nebula,
                (*NEBULA_A, alpha),
                (70 - offset * 20, 24 + offset * 8, 560 + offset * 34, 170 + offset * 12),
            )
            pygame.draw.ellipse(
                nebula,
                (*NEBULA_B, alpha),
                (760 - offset * 14, 22 + offset * 10, 360 + offset * 24, 150 + offset * 10),
            )
            pygame.draw.ellipse(
                nebula,
                (36, 92, 168, alpha),
                (-80 - offset * 8, 430 + offset * 6, 520 + offset * 30, 210 + offset * 10),
            )
            self.draw_surface.blit(nebula, (0, 0))

        for index, (x, y, radius) in enumerate(self.star_field):
            pulse = 0.55 + 0.45 * sin(self.animation_time * 1.6 + index * 0.45)
            color = (
                min(255, int(STAR[0] * pulse + 35)),
                min(255, int(STAR[1] * pulse + 20)),
                min(255, int(STAR[2] * pulse + 10)),
            )
            pygame.draw.circle(self.draw_surface, color, (x, y), radius)

        for path in self.constellations:
            pygame.draw.lines(self.draw_surface, (124, 161, 214), False, path, 1)
            for point in path:
                pygame.draw.circle(self.draw_surface, (216, 232, 255), point, 2)

    def draw_card(self, rect: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None:
        x, y, w, h = rect
        shadow_rect = (x + 6, y + 8, w, h)
        pygame.draw.rect(self.draw_surface, (4, 10, 22), shadow_rect, border_radius=20)
        pygame.draw.rect(self.draw_surface, color, rect, border_radius=20)
        pygame.draw.rect(self.draw_surface, PANEL_EDGE, rect, width=1, border_radius=20)

    def draw_header(self) -> None:
        header_rect = (PADDING, PADDING, SCREEN_W - PADDING * 2, HEADER_HEIGHT)
        self.draw_card(header_rect, PANEL)

        title = self.title_font.render("Robot Lost: Starfall Route", True, TEXT)
        subtitle = self.font.render(
            "越界 → LOST；掉落留下 scent，保護下一台機器人",
            True,
            MUTED,
        )

        self.draw_surface.blit(title, (PADDING + 24, PADDING + 14))
        self.draw_surface.blit(subtitle, (PADDING + 24, PADDING + 56))

    def draw_board_panel(self) -> None:
        board_rect = (BOARD_LEFT - 16, BOARD_TOP - 16, BOARD_W + 32, BOARD_H + 32)
        self.draw_card(board_rect, PANEL)

    def draw_grid(self) -> None:
        for gx in range(WIDTH + 1):
            label = self.small_font.render(str(gx), True, MUTED)
            x = BOARD_LEFT + gx * CELL + CELL // 2 - label.get_width() // 2
            self.draw_surface.blit(label, (x, BOARD_TOP + BOARD_H + 10))

        for gy in range(HEIGHT + 1):
            label = self.small_font.render(str(gy), True, MUTED)
            y = BOARD_TOP + (HEIGHT - gy) * CELL + CELL // 2 - label.get_height() // 2
            self.draw_surface.blit(label, (BOARD_LEFT - 20, y))

        for gx in range(WIDTH + 2):
            x = BOARD_LEFT + gx * CELL
            pygame.draw.line(
                self.draw_surface,
                GRID,
                (x, BOARD_TOP),
                (x, BOARD_TOP + BOARD_H),
                2,
            )

        for gy in range(HEIGHT + 2):
            y = BOARD_TOP + gy * CELL
            pygame.draw.line(
                self.draw_surface,
                GRID,
                (BOARD_LEFT, y),
                (BOARD_LEFT + BOARD_W, y),
                2,
            )

        glow = pygame.Surface((BOARD_W + 18, BOARD_H + 18), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*GRID_GLOW, 40), (0, 0, BOARD_W + 18, BOARD_H + 18), width=3, border_radius=18)
        self.draw_surface.blit(glow, (BOARD_LEFT - 9, BOARD_TOP - 9))

    def draw_path(self) -> None:
        if len(self.current_track) < 2:
            return

        points = []
        for state in self.current_track:
            sx, sy = self.map_to_screen(state.x, state.y)
            points.append((sx + CELL // 2, sy + CELL // 2))

        if len(points) >= 2:
            pygame.draw.lines(self.draw_surface, TRAIL, False, points, 3)
            for point in points[:-1]:
                pygame.draw.circle(self.draw_surface, (154, 196, 245), point, 4)

    def draw_scents(self) -> None:
        for x, y, direction in self.scents:
            sx, sy = self.map_to_screen(x, y)
            center = (sx + CELL // 2, sy + CELL // 2)
            halo = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.circle(halo, (*SCENT, 80), (19, 19), 18)
            self.draw_surface.blit(halo, (center[0] - 19, center[1] - 19))
            pygame.draw.circle(self.draw_surface, SCENT, center, 9)
            d_text = self.small_font.render(direction, True, (57, 33, 10))
            self.draw_surface.blit(d_text, (center[0] - d_text.get_width() // 2, center[1] - 8))

    def draw_robot(self, robot: ReplayState) -> None:
        sx, sy = self.map_to_screen(robot.x, robot.y)
        cx = sx + CELL // 2
        cy = sy + CELL // 2

        points = {
            "N": [(cx, cy - 26), (cx - 18, cy + 18), (cx + 18, cy + 18)],
            "E": [(cx + 26, cy), (cx - 18, cy - 18), (cx - 18, cy + 18)],
            "S": [(cx, cy + 26), (cx - 18, cy - 18), (cx + 18, cy - 18)],
            "W": [(cx - 26, cy), (cx + 18, cy - 18), (cx + 18, cy + 18)],
        }
        color = ROBOT_LOST if robot.lost else ROBOT
        aura = pygame.Surface((88, 88), pygame.SRCALPHA)
        aura_alpha = 110 if robot.lost else 78 + int(34 * (0.5 + 0.5 * sin(self.animation_time * 2.6)))
        pygame.draw.circle(aura, (*color, aura_alpha), (44, 44), 28)
        self.draw_surface.blit(aura, (cx - 44, cy - 44))
        pygame.draw.polygon(self.draw_surface, color, points[robot.direction])
        pygame.draw.polygon(self.draw_surface, TEXT, points[robot.direction], 2)

    def draw_side_panel(self, display_robot: ReplayState) -> None:
        panel_top = BOARD_TOP - 16
        hud_bottom = BOARD_TOP + BOARD_H + GAP + BOTTOM_PANEL_HEIGHT
        panel_h = hud_bottom - panel_top
        self.draw_card((SIDE_LEFT, panel_top, SIDE_PANEL_WIDTH, panel_h), PANEL_ALT)

        board_tag = self.small_font.render("棋盤 0..5 × 0..3　△ 機器人　● scent", True, ACCENT)
        self.draw_surface.blit(board_tag, (SIDE_LEFT + 18, panel_top + 14))

        mission_title = self.section_font.render("任務簡報", True, TEXT)
        self.draw_surface.blit(mission_title, (SIDE_LEFT + 18, panel_top + 40))

        mission_lines = [
            "1. 越界 → LOST",
            "2. 掉落 → 留下 scent",
            "3. 同位同向 → 自動忽略危險 F",
        ]
        for index, line in enumerate(mission_lines):
            text = self.small_font.render(line, True, TEXT)
            self.draw_surface.blit(text, (SIDE_LEFT + 22, panel_top + 72 + index * 22))

        controls_title = self.section_font.render("操作與圖例", True, TEXT)
        self.draw_surface.blit(controls_title, (SIDE_LEFT + 18, panel_top + 142))

        control_lines = [
            "L / R / F  左轉 / 右轉 / 前進",
            "N  新機器人　　C  清空 scent",
            "P  回放　G  輸出 GIF　S  截圖",
            "滑鼠滾輪  捲動事件紀錄",
            "拖曳視窗邊框  放大整個畫面",
            "^ > v <  朝向　X  LOST　*  scent",
        ]
        for index, line in enumerate(control_lines):
            color = ACCENT if index == 5 else TEXT
            text = self.small_font.render(line, True, color)
            self.draw_surface.blit(text, (SIDE_LEFT + 22, panel_top + 170 + index * 22))

        matrix_title = self.section_font.render("10×10 監看矩陣", True, TEXT)
        self.draw_surface.blit(matrix_title, (SIDE_LEFT + 18, panel_top + 294))
        matrix_top = panel_top + 328
        matrix_info_y = panel_top + panel_h - 34
        matrix_rect = (
            SIDE_LEFT + 18,
            matrix_top,
            SIDE_PANEL_WIDTH - 36,
            matrix_info_y - matrix_top - 14,
        )
        pygame.draw.rect(self.draw_surface, (9, 19, 40), matrix_rect, border_radius=16)
        pygame.draw.rect(self.draw_surface, PANEL_EDGE, matrix_rect, width=1, border_radius=16)

        lines = self.build_matrix_10x10(display_robot)
        for i, row in enumerate(lines):
            line_text = self.mono_font.render(row, True, TEXT)
            self.draw_surface.blit(line_text, (matrix_rect[0] + 16, matrix_rect[1] + 14 + i * 19))

        robot_text = self.small_font.render(
            f"({display_robot.x}, {display_robot.y}, {display_robot.direction})  {'LOST' if display_robot.lost else 'ALIVE'}  scent×{len(self.scents)}",
            True,
            TEXT,
        )
        self.draw_surface.blit(robot_text, (matrix_rect[0] + 16, matrix_info_y))

    def draw_chip(self, x: int, y: int, text: str, color: Tuple[int, int, int]) -> int:
        label = self.small_font.render(text, True, BG)
        width = label.get_width() + 18
        rect = pygame.Rect(x, y, width, 28)
        pygame.draw.rect(self.draw_surface, color, rect, border_radius=14)
        self.draw_surface.blit(label, (x + 9, y + 6))
        return width

    def draw_hud(self, display_robot: ReplayState | None = None, mode_override: str | None = None) -> None:
        panel_top = BOARD_TOP + BOARD_H + GAP
        panel_width = BOARD_W + 32
        panel_height = BOTTOM_PANEL_HEIGHT
        self.draw_card((PADDING, panel_top, panel_width, panel_height), PANEL)

        if display_robot is None:
            display_robot = self.get_display_robot()

        mode = mode_override if mode_override is not None else ("回放" if self.replay_mode else "即時")
        status = self.section_font.render(
            f"{mode}  |  ({display_robot.x}, {display_robot.y}, {display_robot.direction})  |  {'LOST' if display_robot.lost else 'ALIVE'}",
            True,
            TEXT,
        )
        summary = self.small_font.render(
            f"{self.status}　　scent {len(self.scents)}　軌跡 {len(self.current_track)}",
            True,
            MUTED,
        )

        self.draw_surface.blit(status, (PADDING + 18, panel_top + 12))
        self.draw_surface.blit(summary, (PADDING + 18, panel_top + 46))

        history_title = self.small_font.render("指令歷史", True, ACCENT)
        log_title = self.small_font.render("事件紀錄", True, ACCENT)
        self.draw_surface.blit(history_title, (PADDING + 18, panel_top + 76))
        self.draw_surface.blit(log_title, (PADDING + 18, panel_top + 118))

        x = PADDING + 94
        y = panel_top + 74
        if not self.command_history:
            idle = self.small_font.render("尚未輸入指令", True, MUTED)
            self.draw_surface.blit(idle, (x, y + 7))
        else:
            for command in self.command_history[-12:]:
                x += self.draw_chip(x, y, command, GOOD if command != "F" else ACCENT) + 6

        # Event log with scroll (mousewheel)
        log_left = PADDING + 94
        log_top = panel_top + 116
        log_avail_h = panel_height - 120
        max_lines = max(1, log_avail_h // 22)
        max_scroll = max(0, len(self.event_log) - max_lines)
        self.event_log_scroll = max(0, min(self.event_log_scroll, max_scroll))
        total = len(self.event_log)
        start_idx = max(0, total - max_lines - self.event_log_scroll)
        end_idx = total - self.event_log_scroll
        visible_events = self.event_log[start_idx:end_idx]

        clip_rect = pygame.Rect(PADDING, log_top, panel_width, log_avail_h)
        self.draw_surface.set_clip(clip_rect)
        for index, line in enumerate(visible_events):
            line_text = self.small_font.render(f"- {line}", True, MUTED)
            self.draw_surface.blit(line_text, (log_left, log_top + index * 22))
        self.draw_surface.set_clip(None)

        if max_scroll > 0:
            hint = self.small_font.render(
                f"↑↓ 滾輪捲動  {self.event_log_scroll}/{max_scroll}", True, ACCENT
            )
            self.draw_surface.blit(hint, (PADDING + panel_width - hint.get_width() - 18, panel_top + 120))

    def render_scene(self, display_robot: ReplayState, mode_override: str | None = None) -> None:
        self.draw_surface = self.canvas
        self.draw_background()
        self.draw_header()
        self.draw_board_panel()
        self.draw_grid()
        self.draw_path()
        self.draw_scents()
        self.draw_robot(display_robot)
        self.draw_side_panel(display_robot)
        self.draw_hud(display_robot=display_robot, mode_override=mode_override)

    def present_with_zoom(self) -> None:
        window_w, window_h = self.screen.get_size()
        fit_scale = min(window_w / SCREEN_W, window_h / SCREEN_H)
        display_scale = max(0.1, fit_scale * self.zoom)

        scaled_w = max(1, int(SCREEN_W * display_scale))
        scaled_h = max(1, int(SCREEN_H * display_scale))
        scaled = pygame.transform.smoothscale(self.canvas, (scaled_w, scaled_h))

        self.screen.fill(BG)
        if scaled_w > window_w or scaled_h > window_h:
            # Crop to the intersection of the scaled surface and the window size
            crop_w = min(window_w, scaled_w)
            crop_h = min(window_h, scaled_h)
            crop_x = max(0, (scaled_w - crop_w) // 2)
            crop_y = max(0, (scaled_h - crop_h) // 2)
            cropped = scaled.subsurface((crop_x, crop_y, crop_w, crop_h))
            blit_x = (window_w - crop_w) // 2
            blit_y = (window_h - crop_h) // 2
            self.screen.blit(cropped, (blit_x, blit_y))
        else:
            x = (window_w - scaled_w) // 2
            y = (window_h - scaled_h) // 2
            self.screen.blit(scaled, (x, y))

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.VIDEORESIZE:
                    width = max(960, event.w)
                    height = max(760, event.h)
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)

                    if event.key == pygame.K_n:
                        self.reset_robot()
                    elif event.key == pygame.K_c:
                        self.clear_scents()
                    elif event.key == pygame.K_p:
                        if self.current_track:
                            self.replay_mode = not self.replay_mode
                            self.replay_index = 0
                            self.replay_timer = 0.0
                            self.set_status("已開啟回放" if self.replay_mode else "已關閉回放")
                    elif event.key == pygame.K_g:
                        self.export_replay_gif()
                    elif event.key == pygame.K_s:
                        self.save_gameplay_screenshot()
                    elif event.key == pygame.K_t:
                        self.save_small_gameplay_screenshot()
                    elif event.key == pygame.K_m:
                        self.export_matrix_snapshot(self.get_display_robot())
                    elif event.key in (pygame.K_l, pygame.K_r, pygame.K_f):
                        self.replay_mode = False
                        mapping = {
                            pygame.K_l: "L",
                            pygame.K_r: "R",
                            pygame.K_f: "F",
                        }
                        self.apply_command(mapping[event.key])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.zoom_in()
                    elif event.button == 3:
                        self.zoom_out()

                if event.type == pygame.MOUSEWHEEL:
                    max_scroll = max(0, len(self.event_log) - 1)
                    self.event_log_scroll = max(0, min(
                        self.event_log_scroll - event.y, max_scroll
                    ))

            self.replay_tick(dt)
            self.render_scene(self.get_display_robot())
            self.present_with_zoom()
            pygame.display.flip()


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
