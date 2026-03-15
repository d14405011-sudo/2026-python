# TEST_CASES

| # | 輸入（初始狀態 + 指令） | 預期結果 | 實際結果 | PASS/FAIL | 對應測試函式 |
|---|---|---|---|---|---|
| 1 | N + L | W | W | PASS | test_turn_left_from_north |
| 2 | N + R | E | E | PASS | test_turn_right_from_north |
| 3 | (1,1,E) + RFRFRFRF | (1,1,E) ALIVE | (1,1,E) ALIVE | PASS | test_typical_uva_sequence_sample_1 |
| 4 | (5,3,N) + F | (5,3,N) LOST + 留 scent | (5,3,N) LOST + 留 scent | PASS | test_first_robot_leaves_scent_when_lost |
| 5 | (5,3,N) + F（前提已有 scent=(5,3,N)） | 忽略 F，不 LOST | 忽略 F，不 LOST | PASS | test_second_robot_ignores_dangerous_move_with_same_scent |
| 6 | (5,3,E) + F（前提已有 scent=(5,3,N)） | 會 LOST（方向不同） | 會 LOST（方向不同） | PASS | test_same_cell_different_direction_does_not_share_scent |
| 7 | N 連續 RRRR | 回到 N | 回到 N | PASS | test_four_right_turns_back_to_origin_direction |
| 8 | (0,3,N) + FRF | 第一個 F 就 LOST，後面不執行 | 第一個 F 就 LOST，後面不執行 | PASS | test_lost_stops_following_commands |
| 9 | (1,1,N) + F | 變成 (1,2,N) ALIVE | 變成 (1,2,N) ALIVE | PASS | test_move_inside_boundary |
| 10 | (0,0,N) + X | 非法指令，丟出 ValueError | 非法指令，丟出 ValueError | PASS | test_invalid_instruction_raises |
| 11 | (5,3,N) + FR（前提已有 scent=(5,3,N)） | F 被忽略後仍可執行 R，結果朝向 E | F 被忽略後仍可執行 R，結果朝向 E | PASS | test_scent_block_still_continues_next_instruction |

備註：

- 類型覆蓋：正常（#3, #9）、邊界（#4, #8）、反例（#10）、scent 方向差異（#6）、LOST 後仍有後續指令（#8）。
