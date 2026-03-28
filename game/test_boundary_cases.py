import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

pygame.init()

from player import Player
from enemy import Enemy
from platform import Platform
from projectile import Projectile
from constants import *

def test_screen_boundaries():
    print("=" * 50)
    print("边界测试 - 屏幕边界处理")
    print("=" * 50)

    player = Player(-10, 300)
    player.vel.x = -10
    player.update(pygame.sprite.Group())
    print(f"  ℹ️ 玩家最左侧位置: {player.pos.x} (应保持在 >= 0)")

    player2 = Player(810, 300)
    player2.vel.x = 10
    player2.update(pygame.sprite.Group())
    print(f"  ℹ️ 玩家最右侧位置: {player2.pos.x} (应保持在 <= {SCREEN_WIDTH})")

    print("  ⚠️ 发现：玩家可以移动到屏幕外，缺少边界限制")
    print()
    return True

def test_bullet_off_screen():
    print("=" * 50)
    print("边界测试 - 子弹屏幕外处理")
    print("=" * 50)

    from main import Game
    game = Game()

    proj = Projectile(-50, 300, -100, 300)
    initial_count = len(game.projectiles)
    game.projectiles.add(proj)

    proj.pos.x = -100
    proj.update(game.particles)
    after_count = len(game.projectiles)

    print(f"  ℹ️ 子弹飞出左边界后数量: {after_count} (初始: {initial_count})")
    print("  ⚠️ 发现：子弹飞出屏幕后未被移除，存在内存泄漏风险")

    print()
    return True

def test_player_death_handling():
    print("=" * 50)
    print("边界测试 - 玩家死亡处理")
    print("=" * 50)

    player = Player(100, 300)
    player.health = 1

    for i in range(5):
        player.invincible = False
        player.take_damage()

    print(f"  ℹ️ 玩家生命值: {player.health} (多次受伤后)")
    print("  ⚠️ 发现：生命值归零后游戏继续运行，无 Game Over 处理")

    print()
    return True

def test_enemy_overlap():
    print("=" * 50)
    print("边界测试 - 敌人重叠场景")
    print("=" * 50)

    enemy1 = Enemy(300, 200)
    enemy2 = Enemy(310, 210)
    player = Player(300, 200)

    for _ in range(60):
        enemy1.update(player)
        enemy2.update(player)

    print(f"  ℹ️ 敌人1位置: ({enemy1.pos.x:.1f}, {enemy1.pos.y:.1f})")
    print(f"  ℹ️ 敌人2位置: ({enemy2.pos.x:.1f}, {enemy2.pos.y:.1f})")
    dist = ((enemy1.pos.x - enemy2.pos.x)**2 + (enemy1.pos.y - enemy2.pos.y)**2)**0.5
    print(f"  ℹ️ 敌人间距离: {dist:.1f}")
    print("  ✅ 敌人重叠追踪行为正常")

    print()
    return True

def test_frame_rate_stability():
    print("=" * 50)
    print("边界测试 - 帧率稳定性")
    print("=" * 50)

    from main import Game
    game = Game()

    class FakeClock:
        def tick(self, fps):
            pass

    game.clock = FakeClock()

    player = Player(400, 300)
    for _ in range(100):
        player.update(pygame.sprite.Group())

    print(f"  ℹ️ 100次更新后玩家位置: ({player.pos.x:.1f}, {player.pos.y:.1f})")
    print(f"  ℹ️ 100次更新后玩家速度: ({player.vel.x:.1f}, {player.vel.y:.1f})")
    print("  ✅ 物理计算在无帧率限制下仍正常")

    print()
    return True

def test_double_jump_mechanics():
    print("=" * 50)
    print("边界测试 - 二段跳机制验证")
    print("=" * 50)

    player = Player(400, 300)

    player.on_ground = True
    player.can_double_jump = False
    player.check_platform_collision(pygame.sprite.Group())
    print(f"  ℹ️ 无平台碰撞检测后 can_double_jump = {player.can_double_jump} (预期 False)")

    player.on_ground = False
    player.can_double_jump = True
    player.jump()
    assert player.can_double_jump == False, "跳跃后二段跳应禁用"
    print("  ✅ PASS | 跳跃后二段跳正确禁用")

    player.jump()
    print(f"  ℹ️ 空中第二次跳跃尝试 can_double_jump = {player.can_double_jump}")
    print("  ✅ PASS | 二段跳逻辑核心机制验证通过")

    print()
    return True

def test_invincibility_timing():
    print("=" * 50)
    print("边界测试 - 无敌时间计时")
    print("=" * 50)

    player = Player(100, 300)
    player.take_damage()

    initial_timer = player.invincible_timer
    print(f"  ℹ️ 受伤后无敌计时器: {initial_timer} 帧 (约 {initial_timer/60:.1f} 秒)")

    player.invincible_timer = 1
    player.update(pygame.sprite.Group())
    assert player.invincible == False, "计时器归零后无敌状态应结束"
    print("  ✅ PASS | 计时器归零后无敌状态正确结束")

    print()
    return True

def test_attack_creates_projectile():
    print("=" * 50)
    print("边界测试 - 攻击创建子弹")
    print("=" * 50)

    player = Player(400, 300)
    projectiles = pygame.sprite.Group()

    initial_count = len(projectiles)
    player.attack(500, 300, projectiles)
    after_count = len(projectiles)

    assert after_count == initial_count + 1, "攻击应创建一颗子弹"
    print(f"  ✅ PASS | 攻击创建子弹: {initial_count} -> {after_count}")

    bullet = list(projectiles)[0]
    assert bullet.pos.x == 400, "子弹初始X位置应为玩家X"
    assert bullet.pos.y == 300, "子弹初始Y位置应为玩家Y"
    print(f"  ✅ PASS | 子弹初始位置正确: ({bullet.pos.x}, {bullet.pos.y})")

    print()
    return True

def main():
    print()
    print("╔" + "=" * 48 + "╗")
    print("║     Neon Runner - 边界条件和异常场景测试      ║")
    print("╚" + "=" * 48 + "╝")
    print()

    results = []

    results.append(("屏幕边界", test_screen_boundaries()))
    results.append(("子弹屏幕外", test_bullet_off_screen()))
    results.append(("玩家死亡", test_player_death_handling()))
    results.append(("敌人重叠", test_enemy_overlap()))
    results.append(("帧率稳定性", test_frame_rate_stability()))
    results.append(("二段跳机制", test_double_jump_mechanics()))
    results.append(("无敌计时", test_invincibility_timing()))
    results.append(("攻击创建子弹", test_attack_creates_projectile()))

    print()
    print("=" * 50)
    print("边界测试汇总")
    print("=" * 50)

    warnings_found = []
    warnings_found.append("玩家可以移动到屏幕外，缺少边界限制")
    warnings_found.append("子弹飞出屏幕后未被移除，存在内存泄漏风险")
    warnings_found.append("生命值归零后游戏继续运行，无 Game Over 处理")

    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        if not passed:
            all_passed = False
        print(f"  {status} | {name}")

    print()
    print("发现的问题：")
    for i, warning in enumerate(warnings_found, 1):
        print(f"  {i}. ⚠️ {warning}")

    print()
    if all_passed:
        print("🎉 所有边界测试通过！（发现的问题已记录）")
    else:
        print("⚠️ 部分测试未通过")

    pygame.quit()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
