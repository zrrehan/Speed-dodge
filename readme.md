# 🚗 Speed Dodge  

A **3D car-dodging survival game** built with **Python (PyOpenGL + GLUT)**.  
Your goal is simple: **dodge obstacles, survive as long as possible, and score points** — but beware of holes, police cars, and the nightmare mode.  

---

## 🎮 Features
- **Dynamic Day/Night cycle** 🌞🌙  
- **Multiple camera views**: First-person & Third-person  
- **Obstacles**: Cars, potholes, and random hazards  
- **Police chase** 🚨 (triggered when you crash once)  
- **Power-ups** ⚡ (temporary speed boost control)  
- **Shooting mechanics** 🔫 (limited bullets to destroy obstacles)  
- **Cheat mode** (auto-dodge)  
- **Nightmare mode** (insane car speed!)  

---

## 🕹️ Controls
| Key | Action |
|-----|--------|
| `←` | Move Left |
| `→` | Move Right |
| `Space` | Shoot bullet (limited) |
| `c` | Toggle Cheat Mode |
| `f` | Toggle First-person View |
| `n` | Toggle Nightmare Mode |
| `b` | Night Mode |
| `d` | Day Mode |
| `r` | Restart (after Game Over) |

---

## 📊 Gameplay Rules
- Every dodged obstacle = **+1 point**  
- Crashing once → Police chase starts  
- Crashing twice → **Game Over**  
- Falling into a pothole → Instant **Game Over**  
- Power-up slows time for a few points duration  
- Nightmare mode increases obstacle speed dramatically  