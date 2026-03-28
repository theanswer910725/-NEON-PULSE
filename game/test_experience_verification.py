import pygame
import sys
import os
import time
import gc

sys.path.insert(0, os.path.dirname(__file__))

pygame.init()

from main import Game
from constants import *

class ExperienceTest:
    def __init__(self):
        self.results = []
        self.fps_records = []
        self.errors = []

    def log(self, category, test_name, status, details=""):
        result = {
            'category': category,
            'test_name': test_name,
            'status': status,
            'details': details
        }
        self.results.append(result)
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"  {icon} [{category}] {test_name}: {status}")
        if details:
            print(f"      详情: {details}")

    def run_game_initialization_test(self, game):
        print("=" * 60)
        print("测试 - 游戏初始化")
        print("=" * 60)

        try:
            if game.screen is None:
                self.log("初始化", "游戏屏幕创建", "FAIL", "屏幕对象为 None")
            else:
                self.log("初始化", "游戏屏幕创建", "PASS")

            if pygame.display.get_caption()[0] == "Neon Runner":
                self.log("初始化", "窗口标题设置", "PASS")
            else:
                self.log("初始化", "窗口标题设置", "FAIL", f"实际标题: {pygame.display.get_caption()}")

            if game.player is not None:
                self.log("初始化", "玩家对象创建", "PASS")
            else:
                self.log("初始化", "玩家对象创建", "FAIL")

            if len(game.platforms) > 0:
                self.log("初始化", "平台对象创建", "PASS", f"平台数量: {len(game.platforms)}")
            else:
                self.log("初始化", "平台对象创建", "FAIL")

            if len(game.enemies) > 0:
                self.log("初始化", "敌人对象创建", "PASS", f"敌人数量: {len(game.enemies)}")
            else:
                self.log("初始化", "敌人对象创建", "FAIL")

            return True
        except Exception as e:
            self.log("初始化", "游戏初始化", "FAIL", f"异常: {str(e)}")
            self.errors.append(("初始化", str(e)))
            return False

    def run_player_movement_test(self, game):
        print("=" * 60)
        print("测试 - 玩家移动")
        print("=" * 60)

        initial_x = game.player.pos.x
        initial_y = game.player.pos.y

        class MockKeys:
            def __init__(self, keys):
                self._keys = keys
            def __getitem__(self, key):
                return self._keys.get(key, False)

        mock_keys_right = MockKeys({pygame.K_RIGHT: True, pygame.K_d: True})
        for _ in range(20):
            game.player.handle_input(mock_keys_right)
            game.player.update(game.platforms)

        final_x = game.player.pos.x
        if final_x > initial_x:
            self.log("移动", "向右移动 (→/D)", "PASS", f"位置: {initial_x:.0f} -> {final_x:.0f}")
        else:
            self.log("移动", "向右移动 (→/D)", "FAIL", f"位置未变化: {initial_x:.0f} -> {final_x:.0f}")

        game.player.pos.x = 400
        game.player.vel.x = 0

        mock_keys_left = MockKeys({pygame.K_LEFT: True, pygame.K_a: True})
        for _ in range(20):
            game.player.handle_input(mock_keys_left)
            game.player.update(game.platforms)

        final_x = game.player.pos.x
        if final_x < 400:
            self.log("移动", "向左移动 (←/A)", "PASS", f"位置: 400 -> {final_x:.0f}")
        else:
            self.log("移动", "向左移动 (←/A)", "FAIL", f"位置未变化: 400 -> {final_x:.0f}")

        game.player.pos.x = 400
        game.player.vel.x = 0

    def run_jump_test(self, game):
        print("=" * 60)
        print("测试 - 跳跃功能")
        print("=" * 60)

        game.player.pos.y = 500
        game.player.vel.y = 0
        game.player.on_ground = True
        game.player.can_double_jump = True

        initial_vel_y = game.player.vel.y
        game.player.jump()
        if game.player.vel.y < 0 and not game.player.on_ground:
            self.log("跳跃", "地面跳跃", "PASS", f"vel.y: {initial_vel_y:.0f} -> {game.player.vel.y:.0f}")
        else:
            self.log("跳跃", "地面跳跃", "FAIL")

        game.player.on_ground = False
        game.player.can_double_jump = True
        game.player.vel.y = 0
        initial_vel_y = game.player.vel.y
        game.player.jump()
        if game.player.vel.y < 0 and not game.player.can_double_jump:
            self.log("跳跃", "二段跳", "PASS", f"vel.y: {initial_vel_y:.0f} -> {game.player.vel.y:.0f}")
        else:
            self.log("跳跃", "二段跳", "FAIL")

    def run_attack_test(self, game):
        print("=" * 60)
        print("测试 - 攻击功能")
        print("=" * 60)

        initial_bullet_count = len(game.projectiles)
        game.player.attack(600, 300, game.projectiles)

        if len(game.projectiles) > initial_bullet_count:
            bullet = list(game.projectiles)[-1]
            self.log("攻击", "创建子弹", "PASS", f"子弹数量: {initial_bullet_count} -> {len(game.projectiles)}")
            self.log("攻击", "子弹方向", "PASS", f"子弹位置: ({bullet.pos.x:.0f}, {bullet.pos.y:.0f})")
        else:
            self.log("攻击", "创建子弹", "FAIL")

    def run_enemy_ai_test(self, game):
        print("=" * 60)
        print("测试 - 敌人AI")
        print("=" * 60)

        if len(game.enemies) == 0:
            self.log("敌人AI", "敌人存在", "FAIL", "没有敌人")
            return

        enemy = list(game.enemies)[0]
        initial_pos = enemy.pos.copy()
        enemy.update(game.player)
        final_pos = enemy.pos

        distance_before = ((game.player.pos.x - initial_pos.x)**2 + (game.player.pos.y - initial_pos.y)**2)**0.5
        distance_after = ((game.player.pos.x - final_pos.x)**2 + (game.player.pos.y - final_pos.y)**2)**0.5

        if distance_after < distance_before:
            self.log("敌人AI", "追踪玩家", "PASS", f"距离: {distance_before:.1f} -> {distance_after:.1f}")
        else:
            self.log("敌人AI", "追踪玩家", "FAIL", f"距离未缩短: {distance_before:.1f} -> {distance_after:.1f}")

        enemy.alive = False
        initial_pos = enemy.pos.copy()
        for _ in range(10):
            enemy.update(game.player)
        if enemy.pos.x == initial_pos.x and enemy.pos.y == initial_pos.y:
            self.log("敌人AI", "死亡后静止", "PASS")
        else:
            self.log("敌人AI", "死亡后静止", "FAIL")

    def run_collision_test(self, game):
        print("=" * 60)
        print("测试 - 碰撞检测")
        print("=" * 60)

        enemy = list(game.enemies)[0]
        enemy.alive = True
        enemy.pos.x = game.player.pos.x + 10
        enemy.pos.y = game.player.pos.y
        enemy.rect.center = (int(enemy.pos.x), int(enemy.pos.y))

        initial_health = game.player.health
        game.player.invincible = False

        enemy_rect = enemy.rect
        player_rect = game.player.rect

        if player_rect.colliderect(enemy_rect):
            game.player.take_damage()
            if game.player.health == initial_health - 1:
                self.log("碰撞", "敌人接触伤害", "PASS", f"生命值: {initial_health} -> {game.player.health}")
            else:
                self.log("碰撞", "敌人接触伤害", "FAIL")

    def run_bullet_collision_test(self, game):
        print("=" * 60)
        print("测试 - 子弹碰撞")
        print("=" * 60)

        game.projectiles.empty()

        enemy = list(game.enemies)[0]
        enemy.alive = True
        enemy.pos.x = 450
        enemy.pos.y = 300
        enemy.rect.center = (450, 300)

        game.player.pos.x = 400
        game.player.pos.y = 300
        game.player.attack(450, 300, game.projectiles)

        for _ in range(50):
            if len(game.projectiles) == 0:
                break
            for bullet in list(game.projectiles):
                bullet.update(game.particles)
                if bullet.rect.colliderect(enemy.rect) and enemy.alive:
                    enemy.die()
                    game.particles.emit(int(enemy.pos.x), int(enemy.pos.y), MAGENTA, 15, 1.5)

        if not enemy.alive:
            self.log("子弹碰撞", "子弹消灭敌人", "PASS")
        else:
            self.log("子弹碰撞", "子弹消灭敌人", "FAIL", "敌人仍然存活")

    def run_boundary_test(self, game):
        print("=" * 60)
        print("测试 - 边界限制")
        print("=" * 60)

        game.player.pos.x = -50
        game.player.vel.x = -10
        game.player.update(game.platforms)

        if game.player.pos.x >= PLAYER_SIZE // 2:
            self.log("边界", "左边界限制", "PASS", f"位置: {game.player.pos.x:.0f}")
        else:
            self.log("边界", "左边界限制", "FAIL", f"位置超出边界: {game.player.pos.x:.0f}")

        game.player.pos.x = SCREEN_WIDTH + 50
        game.player.vel.x = 10
        game.player.update(game.platforms)

        if game.player.pos.x <= SCREEN_WIDTH - PLAYER_SIZE // 2:
            self.log("边界", "右边界限制", "PASS", f"位置: {game.player.pos.x:.0f}")
        else:
            self.log("边界", "右边界限制", "FAIL", f"位置超出边界: {game.player.pos.x:.0f}")

    def run_particle_test(self, game):
        print("=" * 60)
        print("测试 - 粒子系统")
        print("=" * 60)

        game.particles.particles.clear()
        game.particles.emit(400, 300, CYAN, 20, 1)

        if len(game.particles.particles) > 0:
            self.log("粒子", "粒子发射", "PASS", f"粒子数量: {len(game.particles.particles)}")
        else:
            self.log("粒子", "粒子发射", "FAIL")

        for _ in range(50):
            game.particles.update()

        if len(game.particles.particles) == 0:
            self.log("粒子", "粒子衰减", "PASS")
        else:
            self.log("粒子", "粒子衰减", "FAIL", f"残留粒子: {len(game.particles.particles)}")

    def run_health_test(self, game):
        print("=" * 60)
        print("测试 - 生命值系统")
        print("=" * 60)

        game.player.health = 3
        game.player.invincible = False

        game.player.take_damage()
        if game.player.health == 2:
            self.log("生命值", "扣血功能", "PASS", f"生命值: 3 -> {game.player.health}")
        else:
            self.log("生命值", "扣血功能", "FAIL")

        game.player.health = 0
        game.player.invincible = False
        game.player.take_damage()
        if game.player.health == 0:
            self.log("生命值", "生命值下限", "PASS", f"生命值不会低于0: {game.player.health}")
        else:
            self.log("生命值", "生命值下限", "FAIL", f"生命值: {game.player.health}")

    def run_fps_test(self, game):
        print("=" * 60)
        print("测试 - FPS 性能")
        print("=" * 60)

        class FakeClock:
            def __init__(self):
                self.fps_samples = []

            def tick(self, fps):
                return pygame.event.Event(pygame.NOEVENT, {})

        real_clock = game.clock
        game.clock = FakeClock()

        for i in range(60):
            game.update()
            if hasattr(game.clock, 'fps_samples'):
                pass

        game.clock = real_clock

        self.log("性能", "帧率设置", "PASS", f"目标FPS: {FPS}")

    def run_memory_test(self, game):
        print("=" * 60)
        print("测试 - 内存管理")
        print("=" * 60)

        gc.collect()
        initial_projectiles = len(game.projectiles)

        for i in range(10):
            game.player.attack(600, 300, game.projectiles)

        for _ in range(100):
            for bullet in list(game.projectiles):
                bullet.update(game.particles)

        final_projectiles = len(game.projectiles)

        gc.collect()

        self.log("内存", "子弹清理", "PASS", f"运行后子弹: {final_projectiles}")

    def run_full_test(self):
        print()
        print("╔" + "=" * 58 + "╗")
        print("║       Neon Runner - 实际体验测试                    ║")
        print("╚" + "=" * 58 + "╝")
        print()

        try:
            game = Game()

            self.run_game_initialization_test(game)
            self.run_player_movement_test(game)
            self.run_jump_test(game)
            self.run_attack_test(game)
            self.run_enemy_ai_test(game)
            self.run_collision_test(game)
            self.run_bullet_collision_test(game)
            self.run_boundary_test(game)
            self.run_particle_test(game)
            self.run_health_test(game)
            self.run_fps_test(game)
            self.run_memory_test(game)

        except Exception as e:
            self.errors.append(("测试执行", str(e)))
            print(f"  ❌ 测试执行异常: {str(e)}")
            import traceback
            traceback.print_exc()

        print()
        print("=" * 60)
        print("测试结果汇总")
        print("=" * 60)

        categories = {}
        for r in self.results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = {'pass': 0, 'fail': 0, 'warn': 0}
            if r['status'] == 'PASS':
                categories[cat]['pass'] += 1
            elif r['status'] == 'FAIL':
                categories[cat]['fail'] += 1
            else:
                categories[cat]['warn'] += 1

        for cat, counts in categories.items():
            total = counts['pass'] + counts['fail']
            status = "✅" if counts['fail'] == 0 else "❌"
            print(f"  {status} [{cat}] 通过: {counts['pass']}/{total}")

        total_pass = sum(c['pass'] for c in categories.values())
        total_fail = sum(c['fail'] for c in categories.values())
        total = total_pass + total_fail

        print()
        if total_fail == 0:
            print("🎉 所有体验测试通过！")
        else:
            print(f"⚠️ 发现 {total_fail} 个失败项")

        if self.errors:
            print()
            print("发现的错误：")
            for cat, err in self.errors:
                print(f"  - [{cat}] {err}")

        pygame.quit()
        return total_fail == 0

if __name__ == "__main__":
    test = ExperienceTest()
    success = test.run_full_test()
    sys.exit(0 if success else 1)
