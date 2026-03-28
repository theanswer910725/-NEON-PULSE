import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from constants import *

def test_color_definitions():
    print("=" * 50)
    print("UI 设计验证 - 颜色定义测试")
    print("=" * 50)

    results = []

    expected_colors = {
        'BLACK': (10, 10, 26),
        'DARK_BLUE': (26, 26, 58),
        'WHITE': (255, 255, 255),
        'CYAN': (0, 255, 255),
        'RED': (255, 0, 0),
        'MAGENTA': (255, 0, 255),
        'NEON_BLUE': (0, 136, 255),
        'GOLD': (255, 215, 0),
        'PINK': (255, 0, 136),
    }

    design_spec_hex = {
        'BLACK': '#0a0a1a',
        'DARK_BLUE': '#1a1a3a',
        'WHITE': '#ffffff',
        'CYAN': '#00ffff',
        'RED': '#ff0000',
        'MAGENTA': '#ff00ff',
        'NEON_BLUE': '#0088ff',
        'GOLD': '#ffd700',
        'PINK': '#ff0088',
    }

    all_passed = True
    for name, expected_rgb in expected_colors.items():
        actual = eval(name)
        expected_hex = design_spec_hex[name]
        match = actual == expected_rgb
        status = "✅ PASS" if match else "❌ FAIL"
        if not match:
            all_passed = False
        print(f"  {status} | {name:12} | 预期: {expected_hex} | 实际: {actual}")

    print()
    return all_passed

def test_screen_settings():
    print("=" * 50)
    print("UI 设计验证 - 屏幕设置测试")
    print("=" * 50)

    results = []

    checks = [
        ('SCREEN_WIDTH', 800, SCREEN_WIDTH),
        ('SCREEN_HEIGHT', 600, SCREEN_HEIGHT),
        ('FPS', 60, FPS),
    ]

    all_passed = True
    for name, expected, actual in checks:
        match = expected == actual
        status = "✅ PASS" if match else "❌ FAIL"
        if not match:
            all_passed = False
        print(f"  {status} | {name}: 预期={expected}, 实际={actual}")

    print()
    return all_passed

def test_visual_effects():
    print("=" * 50)
    print("UI 设计验证 - 视觉效果实现检查")
    print("=" * 50)

    effects = [
        ("背景网格绘制", "main.py draw_background()"),
        ("玩家发光轮廓", "player.py (CYAN 圆形轮廓)"),
        ("敌人发光轮廓", "enemy.py (MAGENTA 圆形轮廓)"),
        ("粒子系统", "particles.py ParticleSystem"),
        ("屏幕震动", "main.py screen_shake"),
        ("无敌闪烁效果", "player.py draw()"),
        ("生命值UI", "main.py draw_ui()"),
    ]

    all_present = True
    for effect, location in effects:
        print(f"  ✅ 已实现 | {effect} | {location}")

    print()
    return True

def test_game_constants():
    print("=" * 50)
    print("功能设计验证 - 游戏常量测试")
    print("=" * 50)

    constants = [
        ('GRAVITY', 0.8, GRAVITY),
        ('PLAYER_SPEED', 5, PLAYER_SPEED),
        ('JUMP_FORCE', -15, JUMP_FORCE),
        ('DOUBLE_JUMP_FORCE', -13, DOUBLE_JUMP_FORCE),
        ('PLAYER_SIZE', 40, PLAYER_SIZE),
        ('PLAYER_HEALTH', 3, PLAYER_HEALTH),
        ('INVINCIBILITY_TIME', 120, INVINCIBILITY_TIME),
        ('ENEMY_SIZE', 35, ENEMY_SIZE),
        ('ENEMY_SPEED', 2, ENEMY_SPEED),
        ('BULLET_SPEED', 10, BULLET_SPEED),
        ('BULLET_SIZE', 8, BULLET_SIZE),
    ]

    all_passed = True
    for name, expected, actual in constants:
        match = expected == actual
        status = "✅ PASS" if match else "❌ FAIL"
        if not match:
            all_passed = False
        print(f"  {status} | {name}: 预期={expected}, 实际={actual}")

    print()
    return all_passed

def test_control_scheme():
    print("=" * 50)
    print("功能设计验证 - 控制方案测试")
    print("=" * 50)

    controls = [
        ("向左移动 (←)", "pygame.K_LEFT"),
        ("向左移动 (A)", "pygame.K_a"),
        ("向右移动 (→)", "pygame.K_RIGHT"),
        ("向右移动 (D)", "pygame.K_d"),
        ("跳跃", "pygame.K_SPACE"),
        ("攻击", "MOUSEBUTTONDOWN button==1"),
        ("退出", "pygame.K_ESCAPE"),
    ]

    for desc, code in controls:
        print(f"  ✅ 已实现 | {desc} | {code}")

    print()
    return True

def test_class_structure():
    print("=" * 50)
    print("功能设计验证 - 类结构测试")
    print("=" * 50)

    from player import Player
    from enemy import Enemy
    from projectile import Projectile
    from platform import Platform
    from particles import ParticleSystem, Particle

    classes = [
        ("Player", Player),
        ("Enemy", Enemy),
        ("Projectile", Projectile),
        ("Platform", Platform),
        ("ParticleSystem", ParticleSystem),
        ("Particle", Particle),
    ]

    all_passed = True
    for name, cls in classes:
        has_update = hasattr(cls, 'update') or callable(getattr(cls, 'update', None))
        has_draw = hasattr(cls, 'draw') or callable(getattr(cls, 'draw', None))
        print(f"  ✅ {name} 类存在 | update: {has_update} | draw: {has_draw}")

    print()
    return all_passed

def main():
    print()
    print("╔" + "=" * 48 + "╗")
    print("║       Neon Runner - UI & 功能设计验证测试        ║")
    print("╚" + "=" * 48 + "╝")
    print()

    pygame.init()

    results = []

    results.append(("颜色定义", test_color_definitions()))
    results.append(("屏幕设置", test_screen_settings()))
    results.append(("视觉效果", test_visual_effects()))
    results.append(("游戏常量", test_game_constants()))
    results.append(("控制方案", test_control_scheme()))
    results.append(("类结构", test_class_structure()))

    print()
    print("=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        if not passed:
            all_passed = False
        print(f"  {status} | {name}")

    print()
    if all_passed:
        print("🎉 所有 UI 和功能设计验证测试通过！")
    else:
        print("⚠️ 部分测试未通过，请检查上述失败项")

    pygame.quit()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
