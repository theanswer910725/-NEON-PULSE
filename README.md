# ⚡ NEON RUNNER ⚡

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║  ███╗   ██╗███████╗ ██████╗ ███╗   ██╗                      ║
    ║  ████╗  ██║██╔════╝██╔═══██╗████╗  ██║                      ║
    ║  ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║                      ║
    ║  ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║                      ║
    ║  ██║ ╚████║███████╗╚██████╔╝██║ ╚████║                      ║
    ║  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝                      ║
    ║              // CYBERDECK PROTOCOL //                       ║
    ╚═══════════════════════════════════════════════════════════════╝
```

> 🎮 赛博朋克风格平台跳跃游戏 | Pygame 构建

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 简介

**NEON RUNNER** 是一款快节奏的赛博朋克平台跳跃游戏。玩家控制一名霓虹战士，在数字虚空中与成群的敌人战斗。游戏包含二段跳机制、弹幕攻击、粒子效果以及合成波风格的视觉效果。

---

## ✨ 特色功能

| 图标 | 功能 | 描述 |
|------|------|------|
| 🌟 | **赛博朋克美学** | 霓虹配色、发光效果、扫描线和网格背景 |
| 🎮 | **流畅操控** | 响应式移动，支持二段跳 |
| 💥 | **战斗系统** | 鼠标点击发射弹幕，伴随屏幕震动反馈 |
| 📈 | **动态难度** | 随分数提升，敌人刷新率增加 |
| ✨ | **粒子效果** | 爆炸、轨迹和悬浮粒子 |
| 🔮 | **视觉打磨** | 脉冲发光、标题 glitch 效果、角落 UI 框架 |

---

## 🎮 操作说明

| 按键 | 功能 |
|------|------|
| `←` `→` 或 `A` `D` | 左右移动 |
| `SPACE` | 跳跃 / 二段跳 |
| `鼠标左键` | 攻击（发射弹幕） |
| `ESC` | 退出游戏 |

---

## 🚀 安装指南

### 环境要求

- Python 3.7 或更高版本
- pip (Python 包管理器)

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/theanswer910725/-NEON-PULSE.git
cd -NEON-PULSE

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行游戏
cd game
python main.py
```

---

## 📁 项目结构

```
├── game/
│   ├── main.py          # 游戏主循环和逻辑
│   ├── player.py        # 玩家类，移动和战斗
│   ├── enemy.py         # 敌人 AI 和行为
│   ├── platform.py      # 平台渲染
│   ├── projectile.py    # 弹幕类
│   ├── particles.py     # 粒子系统
│   ├── constants.py     # 游戏常量和配色
│   └── levels/          # 关卡数据（预留）
├── docs/                # 设计文档和测试计划
├── requirements.txt     # Python 依赖
└── README.md            # 本文件
```

---

## 🎯 游戏玩法

```
┌─────────────────────────────────────┐
│  ❤️ 生命值: 3 点 (显示为护盾条)      │
│  💎 得分: 每击败一个敌人 +100 分      │
│  ⚡ 难度: 分数越高，敌人刷新越快      │
│  🎯 目标: 尽可能存活更长时间！        │
└─────────────────────────────────────┘
```

---

## 🎨 色彩系统

| 颜色名称 | 色值 | 用途 |
|----------|------|------|
| 🟦 青色 | `#00FFFF` | 玩家发光、UI 边框 |
| 🟪 品红 | `#FF00FF` | 分数显示、爆炸效果 |
| 🟣 霓虹紫 | `#B400FF` | 网格线、悬浮粒子 |
| 🟥 危险红 | `#FF003C` | 伤害指示器 |

---

## 🧪 开发测试

```bash
cd game
python -m pytest test_functional_verification.py
python -m pytest test_experience_verification.py
```

---

## 📜 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

```
    ⚡ NEON RUNNER // CYBERDECK v2.0 ⚡
    © 2026 All Rights Reserved.
```
