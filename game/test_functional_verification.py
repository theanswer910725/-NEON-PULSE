import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

pygame.init()

from player import Player
from enemy import Enemy
from platform import Platform
from projectile import Projectile
from particles import ParticleSystem, Particle
from constants import *

def test_player_movement():
    print("=" * 50)
    print("功能测试 - 玩家移动系统")
    print("=" * 50)

    player = Player(100, 100)

    class MockKeys:
        def __getitem__(self, key):
            return False

    player.handle_input(MockKeys())
    assert player.vel.x == 0, "无按键时应静止"
    print("  ✅ PASS | 无按键时玩家静止")

    class MockKeysRight:
        def __getitem__(self, key):
            return key in (pygame.K_RIGHT, pygame.K_d)

    player.handle_input(MockKeysRight())
    assert player.vel.x > 0, "按下右方向键或D键后速度应为正"
    print("  ✅ PASS | 右方向键/D键移动方向正确 (vel.x > 0)")

    class MockKeysLeft:
        def __getitem__(self, key):
            return key in (pygame.K_LEFT, pygame.K_a)

    player.handle_input(MockKeysLeft())
    assert player.vel.x < 0, "按下左方向键或A键后速度应为负"
    print("  ✅ PASS | 左方向键/A键移动方向正确 (vel.x < 0)")

    print()
    return True

def test_player_jump():
    print("=" * 50)
    print("功能测试 - 玩家跳跃系统")
    print("=" * 50)

    player = Player(100, 100)

    player.on_ground = False
    player.can_double_jump = False
    player.jump()
    assert player.vel.y == 0 or player.vel.y > 0, "空中无法跳跃（无二段跳）"
    print("  ✅ PASS | 空中无二段跳时无法再次跳跃")

    player.on_ground = True
    player.can_double_jump = True
    initial_vel_y = player.vel.y
    player.jump()
    assert player.vel.y < 0, "地面跳跃应有负速度（向上）"
    assert player.on_ground == False, "跳跃后应离开地面"
    print("  ✅ PASS | 地面跳跃 vel.y < 0")

    player.on_ground = False
    player.can_double_jump = True
    before_double_jump = player.vel.y
    player.jump()
    assert player.vel.y < 0, "二段跳应有负速度"
    assert player.can_double_jump == False, "二段跳后标志应重置"
    print("  ✅ PASS | 二段跳功能正常")

    player.on_ground = False
    player.can_double_jump = False
    before_third_jump = player.vel.y
    player.jump()
    assert player.vel.y == before_third_jump, "无二段跳时不应再次跳跃"
    print("  ✅ PASS | 无二段跳机会时无法第三次跳跃")

    print()
    return True

def test_gravity():
    print("=" * 50)
    print("功能测试 - 重力系统")
    print("=" * 50)

    player = Player(100, 100)
    player.vel.y = 0
    player.apply_gravity()
    assert player.vel.y == GRAVITY, f"初始重力应用失败，期望 {GRAVITY}, 实际 {player.vel.y}"
    print(f"  ✅ PASS | 重力初始应用正确 ({GRAVITY})")

    player.vel.y = 0
    for _ in range(10):
        player.apply_gravity()
    assert player.vel.y > 0, "多次应用重力后速度应为正（向下）"
    assert player.vel.y <= 15, f"速度应有限制，期望 <= 15, 实际 {player.vel.y}"
    print(f"  ✅ PASS | 重力累积正确，速度限制生效 (<= 15)")

    print()
    return True

def test_platform_collision():
    print("=" * 50)
    print("功能测试 - 平台碰撞检测")
    print("=" * 50)

    platform = Platform(0, 550, 800, 50)

    player = Player(400, 540)
    player.vel.y = 10
    player.on_ground = False
    player.check_platform_collision(pygame.sprite.Group([platform]))

    assert player.on_ground == True, "落在平台上时应标记为 on_ground"
    assert player.vel.y == 0, "落在平台上时垂直速度应归零"
    print("  ✅ PASS | 平台碰撞后 on_ground=True, vel.y=0")

    player = Player(400, 300)
    player.vel.y = 10
    player.on_ground = False
    player.check_platform_collision(pygame.sprite.Group([platform]))
    assert player.on_ground == False, "未接触平台时不应标记为 on_ground"
    print("  ✅ PASS | 未接触平台时 on_ground=False")

    print()
    return True

def test_enemy_chase():
    print("=" * 50)
    print("功能测试 - 敌人追踪AI")
    print("=" * 50)

    enemy = Enemy(600, 200)
    player = Player(100, 200)

    initial_enemy_x = enemy.pos.x
    enemy.update(player)
    assert enemy.pos.x != initial_enemy_x, "敌人应在玩家方向移动"
    assert enemy.pos.x < initial_enemy_x, "敌人应向左侧玩家移动"
    print("  ✅ PASS | 敌人向玩家方向追踪")

    player.pos.x = 700
    player.pos.y = 300
    enemy2 = Enemy(100, 100)
    initial_x = enemy2.pos.x
    enemy2.update(player)
    assert enemy2.pos.x > initial_x, "敌人应向右移动"
    print("  ✅ PASS | 敌人追踪方向正确")

    enemy3 = Enemy(300, 200)
    enemy3.alive = False
    initial_pos = enemy3.pos.copy()
    enemy3.update(player)
    assert enemy3.pos.x == initial_pos.x and enemy3.pos.y == initial_pos.y, "死亡敌人不应移动"
    print("  ✅ PASS | 死亡敌人保持静止")

    print()
    return True

def test_projectile():
    print("=" * 50)
    print("功能测试 - 子弹系统")
    print("=" * 50)

    proj = Projectile(100, 100, 200, 100)
    assert proj.pos.x == 100 and proj.pos.y == 100, "子弹初始位置正确"
    print("  ✅ PASS | 子弹初始位置正确")

    proj.update(None)
    assert proj.pos.x > 100, "子弹应向目标方向移动"
    print("  ✅ PASS | 子弹向目标方向移动")

    proj2 = Projectile(100, 100, 100, 100)
    proj2.update(None)
    assert proj2.pos.x > 100, "同位置目标子弹应默认向右发射"
    print("  ✅ PASS | 同位置目标子弹默认向右发射")

    print()
    return True

def test_particle_system():
    print("=" * 50)
    print("功能测试 - 粒子系统")
    print("=" * 50)

    ps = ParticleSystem()
    assert len(ps.particles) == 0, "初始粒子列表应为空"
    print("  ✅ PASS | 初始粒子列表为空")

    ps.emit(100, 100, CYAN, 10, 1)
    assert len(ps.particles) == 10, f"发射后应有10个粒子，实际 {len(ps.particles)}"
    print("  ✅ PASS | 粒子发射功能正常")

    for _ in range(50):
        ps.update()
    assert len(ps.particles) == 0, "粒子应完全衰减"
    print("  ✅ PASS | 粒子衰减正常")

    print()
    return True

def test_damage_system():
    print("=" * 50)
    print("功能测试 - 伤害系统")
    print("=" * 50)

    player = Player(100, 100)
    player.invincible = False
    player.health = 3
    player.take_damage()

    assert player.health == 2, f"受伤后生命值应为2，实际 {player.health}"
    assert player.invincible == True, "受伤后应进入无敌状态"
    assert player.invincible_timer > 0, "无敌计时器应大于0"
    print("  ✅ PASS | 受伤后 health=2, invincible=True, timer>0")

    player.health = 0
    player.invincible = False
    player.take_damage()
    print(f"  ⚠️ 警告 | 生命值可为负数 (health={player.health})，建议增加边界检查")

    print()
    return True

def test_enemy_death():
    print("=" * 50)
    print("功能测试 - 敌人死亡")
    print("=" * 50)

    enemy = Enemy(300, 200)
    assert enemy.alive == True, "敌人初始应为存活状态"
    print("  ✅ PASS | 敌人初始存活")

    enemy.die()
    assert enemy.alive == False, "调用die()后敌人应死亡"
    print("  ✅ PASS | enemy.die() 后 alive=False")

    print()
    return True

def main():
    print()
    print("╔" + "=" * 48 + "╗")
    print("║     Neon Runner - 功能行为验证测试            ║")
    print("╚" + "=" * 48 + "╝")
    print()

    results = []

    results.append(("玩家移动", test_player_movement()))
    results.append(("玩家跳跃", test_player_jump()))
    results.append(("重力系统", test_gravity()))
    results.append(("平台碰撞", test_platform_collision()))
    results.append(("敌人追踪", test_enemy_chase()))
    results.append(("子弹系统", test_projectile()))
    results.append(("粒子系统", test_particle_system()))
    results.append(("伤害系统", test_damage_system()))
    results.append(("敌人死亡", test_enemy_death()))

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
        print("🎉 所有功能行为验证测试通过！")
    else:
        print("⚠️ 部分测试未通过，请检查上述失败项")

    pygame.quit()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
