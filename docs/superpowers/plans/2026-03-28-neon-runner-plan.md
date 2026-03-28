# Neon Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个霓虹赛博风格的平台跳跃战斗游戏，支持双键控制、二段跳、追踪攻击和粒子特效

**Architecture:** 使用 Pygame 构建 2D 游戏，采用面向对象设计，游戏对象（玩家、敌人、平台、粒子）各自独立模块，通过主循环统一更新和渲染

**Tech Stack:** Python 3.x + Pygame

---

## 文件结构

```
game/
├── main.py          # 游戏入口、主循环、状态管理
├── constants.py     # 颜色/尺寸常量
├── player.py        # 玩家角色类
├── enemy.py         # 敌人类
├── platform.py      # 平台类
├── projectile.py    # 子弹类
├── particles.py     # 粒子系统
└── levels/
    └── level1.py    # 关卡数据
```

---

## 任务分解

### Task 1: 项目初始化与常量定义

**Files:**
- Create: `game/constants.py`
- Create: `game/levels/__init__.py`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p game/levels
touch game/levels/__init__.py
```

- [ ] **Step 2: 编写 constants.py**

```python
# 颜色定义 (R, G, B)
BLACK = (10, 10, 26)
DARK_BLUE = (26, 26, 58)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
NEON_BLUE = (0, 136, 255)
GOLD = (255, 215, 0)
PINK = (255, 0, 136)

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 重力常数
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -15
DOUBLE_JUMP_FORCE = -13

# 玩家属性
PLAYER_SIZE = 40
PLAYER_HEALTH = 3
INVINCIBILITY_TIME = 120  # 帧数

# 敌人属性
ENEMY_SIZE = 35
ENEMY_SPEED = 2

# 子弹属性
BULLET_SPEED = 10
BULLET_SIZE = 8
```

- [ ] **Step 3: Commit**

```bash
git add game/constants.py game/levels/__init__.py
git commit -m "feat: add constants and directory structure"
```

---

### Task 2: 基础游戏框架

**Files:**
- Create: `game/main.py`

- [ ] **Step 1: 编写 main.py 基础结构**

```python
import pygame
import sys
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
```

- [ ] **Step 2: 测试运行确保无报错**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 3: Commit**

```bash
git add game/main.py
git commit -m "feat: add basic game framework"
```

---

### Task 3: 玩家角色系统

**Files:**
- Create: `game/player.py`
- Modify: `game/main.py`

- [ ] **Step 1: 编写 player.py**

```python
import pygame
from pygame.math import Vector2
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2)
        pygame.draw.circle(self.image, CYAN, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2, 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.on_ground = False
        self.can_double_jump = True
        self.health = PLAYER_HEALTH
        self.invincible = False
        self.invincible_timer = 0
        self.jump_particles = None
        
    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
            
    def jump(self):
        if self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False
            self.can_double_jump = True
        elif self.can_double_jump:
            self.vel.y = DOUBLE_JUMP_FORCE
            self.can_double_jump = False
            
    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 15:
            self.vel.y = 15
            
    def update(self, platforms):
        self.apply_gravity()
        self.pos += self.vel
        self.rect.center = (self.pos.x, self.pos.y)
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        self.check_platform_collision(platforms)
        
    def check_platform_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0 and self.rect.bottom > platform.rect.top:
                    self.pos.y = platform.rect.top - PLAYER_SIZE//2
                    self.vel.y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                    
    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = INVINCIBILITY_TIME
            
    def draw(self, surface):
        if self.invincible and self.invincible_timer % 10 < 5:
            return
        surface.blit(self.image, self.rect)
```

- [ ] **Step 2: 更新 main.py 集成玩家**

```python
# 在 Game.__init__ 中添加
self.player = Player(100, 300)
self.platforms = pygame.sprite.Group()

# 在 Game.update 中添加
self.player.handle_input(pygame.key.get_pressed())
self.player.update(self.platforms)

# 在 Game.draw 中添加
self.player.draw(self.screen)
```

- [ ] **Step 3: 测试玩家移动和跳跃**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 4: Commit**

```bash
git add game/player.py game/main.py
git commit -m "feat: add player movement and jumping"
```

---

### Task 4: 平台系统

**Files:**
- Create: `game/platform.py`
- Modify: `game/main.py`, `game/levels/level1.py`

- [ ] **Step 1: 编写 platform.py**

```python
import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((26, 26, 46))
        pygame.draw.rect(self.image, NEON_BLUE, (0, 0, width, 3))
        pygame.draw.rect(self.image, NEON_BLUE, (0, 0, 3, height))
        pygame.draw.rect(self.image, NEON_BLUE, (width-3, 0, 3, height))
        pygame.draw.rect(self.image, NEON_BLUE, (0, height-3, width, 3))
        self.rect = self.image.get_rect(x=x, y=y)
```

- [ ] **Step 2: 创建 level1.py 关卡数据**

```python
import pygame
import platform
from constants import *

def load_level():
    platforms = pygame.sprite.Group()
    level_data = [
        (0, 550, 800, 50),
        (100, 450, 150, 20),
        (300, 400, 150, 20),
        (500, 350, 150, 20),
        (200, 280, 150, 20),
        (400, 200, 150, 20),
        (50, 150, 150, 20),
        (600, 480, 150, 20),
    ]
    for x, y, w, h in level_data:
        platforms.add(platform.Platform(x, y, w, h))
    return platforms
```

- [ ] **Step 3: 更新 main.py 加载关卡**

```python
from levels.level1 import load_level

# 在 Game.__init__ 中替换
self.platforms = load_level()
```

- [ ] **Step 4: 测试平台碰撞**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 5: Commit**

```bash
git add game/platform.py game/levels/level1.py game/main.py
git commit -m "feat: add platform system and level design"
```

---

### Task 5: 粒子系统

**Files:**
- Create: `game/particles.py`
- Modify: `game/main.py`

- [ ] **Step 1: 编写 particles.py**

```python
import pygame
import random
from constants import *

class Particle:
    def __init__(self, x, y, color, speed_multiplier=1):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 5) * speed_multiplier
        self.vel = pygame.math.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.color = color
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.size = random.randint(2, 5)
        
    def update(self):
        self.pos += self.vel
        self.vel *= 0.95
        self.life -= 1
        
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        color = (*self.color[:3], alpha) if len(self.color) == 4 else self.color
        if self.life > 0:
            pygame.draw.circle(surface, color[:3], (int(self.pos.x), int(self.pos.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, color, count=10, speed=1):
        import math
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed))
            
    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
                
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
```

- [ ] **Step 2: 更新 main.py 添加粒子系统**

```python
from particles import ParticleSystem

# 在 Game.__init__ 中添加
self.particles = ParticleSystem()

# 在 Game.update 中添加
self.particles.update()

# 在 Game.draw 中添加
self.particles.draw(self.screen)

# 在跳跃时发射粒子（修改 player.jump）
# 在落地时发射粒子
```

- [ ] **Step 3: 测试粒子效果**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 4: Commit**

```bash
git add game/particles.py game/main.py
git commit -m "feat: add particle system"
```

---

### Task 6: 敌人系统

**Files:**
- Create: `game/enemy.py`
- Modify: `game/main.py`

- [ ] **Step 1: 编写 enemy.py**

```python
import pygame
import math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (ENEMY_SIZE//2, ENEMY_SIZE//2), ENEMY_SIZE//2)
        pygame.draw.circle(self.image, MAGENTA, (ENEMY_SIZE//2, ENEMY_SIZE//2), ENEMY_SIZE//2, 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True
        
    def update(self, player):
        if not self.alive:
            return
        dx = player.pos.x - self.pos.x
        dy = player.pos.y - self.pos.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.pos.x += (dx / dist) * ENEMY_SPEED
            self.pos.y += (dy / dist) * ENEMY_SPEED
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
    def die(self):
        self.alive = False
        
    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
```

- [ ] **Step 2: 更新 main.py 添加敌人**

```python
from enemy import Enemy

# 在 Game.__init__ 中添加
self.enemies = pygame.sprite.Group()
self.enemies.add(Enemy(600, 200))
self.enemies.add(Enemy(400, 100))

# 在 Game.update 中添加
for e in self.enemies:
    e.update(self.player)
    
# 在 Game.draw 中添加
for e in self.enemies:
    e.draw(self.screen)
```

- [ ] **Step 3: 测试敌人追踪**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 4: Commit**

```bash
git add game/enemy.py game/main.py
git commit -m "feat: add enemy system with chase AI"
```

---

### Task 7: 子弹与攻击系统

**Files:**
- Create: `game/projectile.py`
- Modify: `game/main.py`, `game/player.py`

- [ ] **Step 1: 编写 projectile.py**

```python
import pygame
import math
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vel = pygame.math.Vector2(
                (dx / dist) * BULLET_SPEED,
                (dy / dist) * BULLET_SPEED
            )
        else:
            self.vel = pygame.math.Vector2(BULLET_SPEED, 0)
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CYAN, (BULLET_SIZE//2, BULLET_SIZE//2), BULLET_SIZE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.trail_timer = 0
        
    def update(self, particles):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.trail_timer += 1
        if self.trail_timer % 3 == 0 and particles:
            particles.emit(int(self.pos.x), int(self.pos.y), CYAN, 2, 0.3)
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
```

- [ ] **Step 2: 更新 player.py 添加攻击方法**

```python
def attack(self, target_x, target_y, projectiles):
    from projectile import Projectile
    projectiles.add(Projectile(self.pos.x, self.pos.y, target_x, target_y))
```

- [ ] **Step 3: 更新 main.py 处理攻击**

```python
# 在 Game.update 中添加攻击检测
for bullet in self.projectiles:
    bullet.update(self.particles)
    for enemy in self.enemies:
        if bullet.rect.colliderect(enemy.rect) and enemy.alive:
            enemy.die()
            self.particles.emit(int(enemy.pos.x), int(enemy.pos.y), MAGENTA, 15, 1.5)
            bullet.kill()

# 在 Game.draw 中绘制子弹
for bullet in self.projectiles:
    bullet.draw(self.screen)
```

- [ ] **Step 4: 测试攻击系统**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 5: Commit**

```bash
git add game/projectile.py game/player.py game/main.py
git commit -m "feat: add projectile attack system"
```

---

### Task 8: 碰撞检测与伤害系统

**Files:**
- Modify: `game/main.py`, `game/player.py`

- [ ] **Step 1: 更新 main.py 添加碰撞伤害**

```python
# 在 Game.update 中，玩家与敌人碰撞后调用 take_damage
for enemy in self.enemies:
    if enemy.alive and self.player.rect.colliderect(enemy.rect):
        self.player.take_damage()
        if self.player.health <= 0:
            print("Game Over")
```

- [ ] **Step 2: 测试伤害和无敌帧**

```bash
cd e:/trae-demo && python game/main.py
```

- [ ] **Step 3: Commit**

```bash
git add game/main.py game/player.py
git commit -m "feat: add damage and invincibility system"
```

---

### Task 9: UI与视觉效果增强

**Files:**
- Modify: `game/main.py`

- [ ] **Step 1: 添加血量显示**

```python
def draw_ui(self):
    font = pygame.font.Font(None, 36)
    for i in range(self.player.health):
        x = 20 + i * 35
        pygame.draw.circle(self.screen, PINK, (x + 12, 30), 12)
        pygame.draw.circle(self.screen, WHITE, (x + 12, 30), 8)
```

- [ ] **Step 2: 添加屏幕震动效果**

```python
# 在 constants.py 中添加
SCREEN_SHAKE_INTENSITY = 5

# 在 main.py 中添加震动逻辑
self.screen_shake = 0

# 修改 draw 方法
def draw(self):
    if self.screen_shake > 0:
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        self.screen.fill(BLACK)
        # 绘制时应用偏移
        self.screen_shake -= 1
    else:
        self.screen.fill(BLACK)
```

- [ ] **Step 3: 添加背景网格**

```python
def draw_background(self):
    self.screen.fill(BLACK)
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(self.screen, DARK_BLUE, (0, y), (SCREEN_WIDTH, y), 1)
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(self.screen, DARK_BLUE, (x, 0), (x, SCREEN_HEIGHT), 1)
```

- [ ] **Step 4: Commit**

```bash
git add game/main.py game/constants.py
git commit -m "feat: add UI and visual effects"
```

---

### Task 10: 整合测试与验收

**Files:**
- Modify: `game/main.py`

- [ ] **Step 1: 完整测试所有功能**

```bash
cd e:/trae-demo && python game/main.py
```

验收清单检查：
- [ ] 方向键和AD键均能控制移动
- [ ] 二段跳功能正常
- [ ] 攻击能消灭敌人
- [ ] 霓虹视觉效果明显
- [ ] 粒子特效完整
- [ ] 3个生命值UI显示
- [ ] 敌人死亡动画播放

- [ ] **Step 2: 最终 Commit**

```bash
git add -A
git commit -m "feat: complete Neon Runner game"
```

---

## 执行方式

**请选择执行方式：**

1. **Subagent-Driven (推荐)** - 每个任务由独立子代理执行，任务间有审核，快迭代
2. **Inline Execution** - 在当前会话中按批次执行任务，带检查点
