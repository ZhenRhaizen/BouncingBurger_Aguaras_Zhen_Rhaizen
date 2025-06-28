# 🍔 Bouncing Burger - Zhen Rhaizen

## 👨‍💻 Name:
**Zhen Rhaizen**

## 🎯 Project Description:
This is a 3D bouncing burger animation built using **Python**, **Tkinter**, and **OpenGL** (via `pyopengltk`). The burger moves smoothly around the screen, bouncing off window edges. When it hits a border, it reverses direction and the name text color changes randomly. Pressing the **spacebar** toggles pause and resume of the animation.

This project demonstrates:
- 🎮 Real-time animation with OpenGL and event-driven updates  
- 🔁 Bouncing collision with random color feedback  
- 🧠 Text rendering using `GLUT_STROKE_ROMAN`  
- ⏸ Pause/Resume behavior via spacebar key binding  
- 🪟 3D graphics rendered in a Tkinter-based OpenGL window  

---

## 🖼 Demo Preview (15-Second Video)
🎬 A 15-second demo video is included in this folder to showcase how the animation works.

---

## 💻 How to Run

### ✅ Option 1: Run the Python Script (Recommended for Source Viewers)

> Make sure you have **Python 3.6+** installed.

```bash
# 🧰 Step 1: Install Required Packages
pip install pyopengltk PyOpenGL

# ▶️ Step 2: Run the Script
python burger.py

# You will see a 3D bouncing burger inside a window.
# Press the spacebar to pause/resume the animation.
